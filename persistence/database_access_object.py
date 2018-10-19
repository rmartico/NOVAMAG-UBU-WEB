#     Copyright (C) 2017-2018 UBU-ICCRAM-ADMIRABLE-NOVAMAG-GA686056
#     http://crono.ubu.es/novamag
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with UBU-ICCRAM-ADMIRABLE-NOVAMAG-GA686056  see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>.

'''
Database functions.
'''

from persistence.novamag_entities_v08 import Item, AttachedFile, Author, Atom, Molecule, Composition
from persistence.parser_search_query import parse_with_and, replace_minus_by_ampersand
from sqlalchemy import cast, Float
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
import re

# Global variables
SessionMaker = None
ATOMS = None

# Routines
def set_session_maker(session_maker):
    # type: (SessionMaker) -> None
    """
    Set the current global session DB maker.

    :param session_maker: session maker
    :type session_maker: SessionMaker
    """
    global SessionMaker # avoid the shadowing of the global variable
    SessionMaker = session_maker

def init_atoms():
    # type: () -> list[Atom]
    """
    Initialize the list of atomic symbols.

    :return: session_maker: session maker
    :rtype: list[Atom]
    """
    global ATOMS # avoid the shadowing of the global variable
    if ATOMS is None:
        ATOMS = query_atoms().all()
    return ATOMS

def query_items_by_advanced_search(form):
    # type: (form) -> list[Item]
    """
    Query the material features using the data of the form.

    :param form data
    :type form: form
    :return: items containing ALL the filters
    :rtype: list[Item]
    """
    session = SessionMaker()
    try:
        query = session.query(Item).join(Molecule).join(Composition)
        # 1
        query = query.filter(Item.compound_space_group >= form.compound_space_group_min.data)
        query = query.filter(Item.compound_space_group <= form.compound_space_group_max.data)
        # 2
        query = query.filter(Item.saturation_magnetization >= form.saturation_magnetization_min.data)
        query = query.filter(Item.saturation_magnetization <= form.saturation_magnetization_max.data)

        #3 first magnetocrystalline anisotropy constants
        apply_filter_k1 = form.apply_filter_k1.data

        if apply_filter_k1: # if the user wants to apply the filter
            query = query.filter(Item.magnetocrystalline_anisotropy_constants[0].astext.cast(DOUBLE_PRECISION) >= form.magnetocrystalline_anisotropy_constant_k1_min.data)
            query = query.filter(Item.magnetocrystalline_anisotropy_constants[0].astext.cast(DOUBLE_PRECISION) <= form.magnetocrystalline_anisotropy_constant_k1_max.data)

        # 4
        query = query.filter(Item.unit_cell_formation_enthalpy >= form.unit_cell_formation_enthalpy_min.data)
        query = query.filter(Item.unit_cell_formation_enthalpy <= form.unit_cell_formation_enthalpy_max.data)
        # 5
        # two solutions: regular expressions or using symbol...
        # we collect the symbols in the filter
        atoms = parse_with_and(form.atomic_species.data)
        # this step is deferred to the function filter_items_with_regular_expression at the end of the method
        # 6
        if form.species_count.data is not None:
            query = query.filter(Item.species_count == form.species_count.data)
        # 7
        # composition percentage...
        symbol = form.stechiometry_atom.data
        percentage_min = form.stechiometry_value_min.data
        percentage_max = form.stechiometry_value_max.data
        query = query.filter(Composition.symbol == symbol)
        query = query.filter(Composition.numb_of_occurrences >= float(percentage_min))
        query = query.filter(Composition.numb_of_occurrences <= float(percentage_max))

        # ORDER BY
        query = query.filter(Item.confidential.is_(False)).order_by(Item.atomic_formation_enthalpy)# only public order by atomic formation enthallpy

        # again step 5 filter using regular expression with the atoms previously collected
        return filter_items_with_regular_expression(query.all(), atoms)
    finally:
        session.close()

def filter_items_with_regular_expression(items, atoms):
    # type: (list, list) -> list
    '''
    Filter the list of items containing in its formula the atoms.

    :param items: items
    :param atoms: atoms
    :return: list of items with atoms
    '''
    new_list = list()
    for item in items:
        count = 0
        for atom in atoms:
            pattern = '^(' + atom + '[A-Z0-9].*|.*' + atom + '[A-Z0-9]+.*|.*' + atom + '[0-9]*)$'
            if re.match(pattern, item.formula) != None:
                count = count + 1
        if count == len(atoms): # match all the atoms
            new_list.append(item)
    return new_list


def str_to_bool(text):
    # type: (str) -> bool
    '''
    Convert a text to bool.

    :param text: text
    :return: true if the text is 'True', false in other case
    '''
    if text == 'True':
         return True
    else:
        return False


def query_items_by_advanced_search_with_query_string(dict):
    # type: (dict) -> list[Item]
    """
    Queries the material features using the data of a dictionary in search query.

    :param dictionary form data
    :type dict: dict
    :return: items containing ALL the filters
    :rtype: list[Item]
    """
    session = SessionMaker()
    try:
        # TODO duplicated code (see query_items_by_advanced_search)
        #query = session.query(Item)
        query = session.query(Item).join(Molecule).join(Composition)
        # 1
        query = query.filter(Item.compound_space_group >= dict['compound_space_group_min'])
        query = query.filter(Item.compound_space_group <= dict['compound_space_group_max'])
        # 2
        query = query.filter(Item.saturation_magnetization >= dict['saturation_magnetization_min'])
        query = query.filter(Item.saturation_magnetization <= dict['saturation_magnetization_max'])

        # 3
        apply_filter_k1 = str_to_bool(dict['apply_filter_k1'])

        if apply_filter_k1:  # if the user wants to apply the filter
            query = query.filter(Item.magnetocrystalline_anisotropy_constants[0].astext.cast(DOUBLE_PRECISION) >= dict['magnetocrystalline_anisotropy_constant_k1_min'])
            query = query.filter(Item.magnetocrystalline_anisotropy_constants[0].astext.cast(DOUBLE_PRECISION) <= dict['magnetocrystalline_anisotropy_constant_k1_max'])

        # 4
        query = query.filter(Item.unit_cell_formation_enthalpy >= dict['unit_cell_formation_enthalpy_min'])
        query = query.filter(Item.unit_cell_formation_enthalpy <= dict['unit_cell_formation_enthalpy_max'])
        # 5
        text_atoms = replace_minus_by_ampersand(dict['atomic_species'])
        atoms = parse_with_and(text_atoms)
        # this step is deferred at the end of the method
        # collect the atoms to filter using regular expression
        # 6
        if dict['species_count'] is not None:
            query = query.filter(Item.species_count == dict['species_count'])
        # 7
        # composition percentage...
        symbol = dict['stechiometry_atom']
        percentage_min = dict['stechiometry_value_min']
        percentage_max = dict['stechiometry_value_max']

        query = query.filter(Composition.symbol == symbol)
        query = query.filter(Composition.numb_of_occurrences >= float(percentage_min))
        query = query.filter(Composition.numb_of_occurrences <= float(percentage_max))

        query = query.filter(Item.confidential.is_(False)).order_by(Item.atomic_formation_enthalpy)# only public order by atomic formation enthallpy

        # again step 5 filter using regular expression with the atoms previously collected
        return filter_items_with_regular_expression(query.all(), atoms)
    finally:
        session.close()


def restore_unitcell_jpg(mafid):
    # type: (str) -> blob
    """
    Restore image for the current item.

    :param mafid: item mafid
    :param mafi: str
    :return: image
    :rtype: blob
    """
    session = SessionMaker()
    query = session.query(AttachedFile).filter(AttachedFile.mafid == mafid).filter(AttachedFile.file_name.like('%.png'))
    binary_large = None
    if query.count() > 0:
        binary_large = query[0].blob_content
    return binary_large

def restore_image(mafid, file_name):
    # type: (str, str) -> blob
    """
    Restore image for the current item.

    :param mafid: item mafid
    :type mafid: str
    :return: image
    :rtype: blob
    """
    session = SessionMaker()
    query = session.query(AttachedFile).filter(AttachedFile.mafid == mafid).filter(AttachedFile.file_name == file_name)
    binary_large = query[0].blob_content
    return binary_large

def query_attached_files_of_item( mafid):
    # type: (str) -> list[AttachedFile]
    """
    Query the attached files of current item.

    :param search_term_mafid: item mafid:
    :type mafid: str
    :return: attached files
    :rtype: list of AttachedFile
    """
    session = SessionMaker()
    try:
        query = session.query(AttachedFile).filter(AttachedFile.mafid==mafid)
        return query
    finally:
        session.close()

def query_authors_of_item(mafid):
    # type: (str) -> list[Author]
    """
    Query the attached files of current item.

    :param search_term_mafid: item mafid
    :type mafid: str
    :return: authors
    :rtype: list[Author]
    """
    session = SessionMaker()
    try:
        query = session.query(Author).join((Author, Item.authors)).filter(Item.mafid==mafid)
        return query
    finally:
        session.close()

def quey_items_by_formula(search_term):
    # type: (str) -> list[Item]
    """
    Query the material features of current material that contains the formula.

    :param search_term: text with formula
    :type search_term: str
    :return: items containing the formula
    :rtype: list[Item]
    """
    session = SessionMaker()
    try:
        # Regular expression searching the atom inside the formula
        patron = '^(' + search_term + '[A-Z0-9].*|.*' + search_term + '[A-Z0-9]+.*|.*' + search_term + '[0-9]*)$'
        query = session.query(Item).from_statement("SELECT * FROM ITEMS WHERE formula ~ '" + patron + "' AND confidential=false ORDER BY mafid")
        return query.all()
    finally:
        session.close()


def query_items_with_and(search_term):
    # type: (str) -> list[Item]
    """
    Query the material features of current material that contains all the atoms.

    :param search_term: text with one or several atoms
    :type search_term: str
    :return: items containing ALL the atoms in the search term
    :rtype: list[Item]
    """
    session = SessionMaker()
    try:
        atoms = parse_with_and(search_term)
        count  = 0
        for atom in atoms:
            # Regular expression searching the atom inside the formula
            patron = '^(' + atom + '[A-Z0-9].*|.*' + atom + '[A-Z0-9]+.*|.*' + atom + '[0-9]*)$'
            if count == 0:
                filtro = " formula ~ '" + patron + "'"
            else:
                count = count + 1
                filtro = filtro + " AND formula ~ '" + patron + "'"

        query = session.query(Item).from_statement("SELECT * FROM ITEMS WHERE " + filtro + " AND confidential=false ORDER BY mafid")
        return query.all()
    finally:
        session.close()

def query_item_features(mafid):
    # type: (str) -> Item
    """
    Query the material features of current material.

    :param mafid: id. of material
    :type mafid: str
    :return: material feature
    :rtype: Item
    """
    session = SessionMaker()
    try:
        list_item_features = session.query(Item).filter(Item.mafid == mafid).filter(Item.confidential.is_(False))
        # if the item is confidential (someone is trying to hack that item, the list will be empty
        # and next line raise and exception
        return list_item_features[0]
    finally:
        session.close()


def query_atoms():
    # type: () -> query
    """
    Query all the atoms.

    :return: query
    :rtype: query
    """
    session = SessionMaker()
    try:
        list = session.query(Atom).order_by(Atom.symbol)
        return list
    finally:
        session.close()

if __name__ == '__main__':
    print('Not yet implemented')
