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

import re

def parse_dict_to_query_string(dict):
    # type: (dict) -> str
    """
    Parses dict with query string to string

    :param dict: dictionary
    :type dict: dict
    :return: params as quey string with parameters
    :rtype: str
    """
    return \
        "compound_space_group_min=" + str(dict["compound_space_group_min"]) + \
        "&compound_space_group_max=" + str(dict["compound_space_group_max"]) + \
        "&saturation_magnetization_min=" + str(dict["saturation_magnetization_min"]) + \
        "&saturation_magnetization_max=" + str(dict["saturation_magnetization_max"]) + \
        "&unit_cell_formation_enthalpy_min=" + str(dict["unit_cell_formation_enthalpy_min"]) + \
        "&unit_cell_formation_enthalpy_max=" + str(dict["unit_cell_formation_enthalpy_max"]) + \
        "&atomic_species=" + dict["atomic_species"]+ \
        "&species_count=" + str(dict["species_count"]) + \
        "&stechiometry_atom=" + str(dict["stechiometry_atom"]) + \
        "&stechiometry_value_min=" + str(dict["stechiometry_value_min"]) + \
        "&stechiometry_value_max=" + str(dict["stechiometry_value_max"])

def parse_form_to_query_search(form):
    # type: (AdvancedSearchForm) -> str
    """
    Parses the text query search giving the list with ampersand characters betweeen parameters.

    :param form: form with advanced search
    :type form: AdvancedSearchForm
    :return: params as quey string
    :rtype: str
    """
    csg_mind = form.compound_space_group_min.data
    csg_maxd = form.compound_space_group_max.data
    smd_mind = form.saturation_magnetization_min.data
    smd_maxd = form.saturation_magnetization_max.data
    ucfe_mind = form.unit_cell_formation_enthalpy_min.data
    ucfe_maxd = form.unit_cell_formation_enthalpy_max.data
    asd = form.atomic_species.data
    scd = form.species_count.data
    sad = form.stechiometry_atom.data
    sv_mind = form.stechiometry_value_min.data
    sv_maxd = form.stechiometry_value_max.data

    return "compound_space_group_min=" + str(csg_mind) + "&compound_space_group_max=" + str(csg_maxd) + "&saturation_magnetization_min=" + str(smd_mind) + "&saturation_magnetization_max=" + str(smd_maxd) +\
        "&unit_cell_formation_enthalpy_min=" + str(ucfe_mind) + "&unit_cell_formation_enthalpy_max=" + str(ucfe_maxd) + "&atomic_species=" + replace_ampersand_by_minus(clean_spaces(asd)) + "&species_count=" + str(scd) + "&stechiometry_atom=" + str(sad) + \
        "&stechiometry_value_min=" + str(sv_mind) + "&stechiometry_value_max=" + str(sv_maxd)


def parse_with_and(text):
    # type: (str) -> list[str]
    """
    Parses the text query search giving the list between & character.

    :param text: text with search query
    :type text: str
    :return: atom list
    :rtype: list[str]
    """
    # first convert to lower and then capitalize
    text = correct_captitalized_letters(text)
    text = clean_spaces(text)
    text = text + "&"
    return re.findall('([A-Za-z]+)&', text)


def correct_captitalized_letters(text):
    # type: (str) -> str
    """
    Corrects capital letters at the beginning of the atom.

    :param text: text with search query
    :type text: str
    :return: text with capitalized atoms
    :rtype: string
    """
    return text.lower().title()


def contains_ampersand(text):
    # type: (str) -> str
    """
    Searchs for an ampersand.

    :param text: text with search query
    :type text: str
    :return: True if contains any ampersand
    :rtype: bool
    """
    return '&' in text


def replace_ampersand_by_minus(text):
    # type: (str) -> str
    """
    Replaces ampersand symbol by minus symbol in the query string.
    Note: problems parsing the query string, we need to replace the symbol inside a parameter.

    :param text: query search
    :type text: str
    :return: query search
    :rtype: str
    """
    return text.replace('&', '-')

def replace_minus_by_ampersand(text):
    # type: (str) -> str
    """
    Replaces minus symbol by ampersand symbol.
    Note: recover the original text.

    :param text: text
    :type test: str
    :return: text
    :rtype: str
    """
    return text.replace('-', '&')


def clean_spaces(text):
    # type: (str) -> str
    """
    Clean the white symbols in the string.

    :param text: text
    :type text: str
    :return: text without white symbols
    :rtype: str
    """
    return text.replace(' ','')


def has_only_one_atom(search_term, ATOMS_LIST):
    # type: (str, list[Atom]) -> bool
    """
    Checks if current search term contains only one atom.

    :param search_term: text with search query
    :type search_term: str
    :param ATOM_LIST: constant list of atoms
    :type ATOMS_LIST: list[Atom]
    :return: True if contains only one atom
    :rtype: bool
    """
    return search_term in ATOMS_LIST