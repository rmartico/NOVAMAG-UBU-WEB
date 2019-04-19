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
Transformation of letter to text. See constraints check in, in database script.
'''
from urllib import quote_plus
import json
import re

angstrom = u'\u00C5ngstr\u00F6m'
angstrom_cubic = u'\u00C5ngstr\u00F6m'u'\u00B3'
mega_joule_per_cubic_meters = u'MJ/m\u00B3'
kilo_joule_per_cubic_meters = u'KJ/m\u00B3'

# Subindex characters for stoichoimetry legend in charts
left_parenthesis_sub = u"\u208D"
right_parenthesis_sub = u'\u208E'
minus_sub = u'\u208B'
one_sub = u'\u2081'
x_sub = u'\u2093'
one_minus_x_sub = left_parenthesis_sub + one_sub + minus_sub + x_sub + right_parenthesis_sub
# examplo (1-x) and (x) but in subindex



def extract_json_value(json_array, index):
    # type: (JSON, int) -> str
    """
    Extract the index value in a JSON array.

    :param json_array: JSON array
    :type json_array: JSON
    :param index: index
    :type index: int
    :return: text with value
    :rtype: str
    """
    print("Tipo de json_array")
    if json_array != None:
        print(json_array)
        print(type(json_array))
        values = json.load(json_array)
        print("Tipo de values")
        print(type(values))
        return values[index]
    else:
        return None

def parse_url(attached_file):
    # type: (AttachedFile) -> str
    """
    Escape characters in path to download file.

    :param attached_file: AttachedFile
    :type attached_file: str
    :return: parsed url
    :rtype: str
    """
    url = str(attached_file.mafid) + "&" + attached_file.file_name
    return url


def transform_list(list):
    # type: (list[str]) -> str
    """
    Parse list to string without 'u' character at the beginning of the text.

    :param list: list
    :type list: list[str]
    :return: string wihtout u character at the beginning of each name
    :rtype: str
    """
    text = None
    if list is not None:
        text = '['
        for item in list:
            if (type(item) is str):
                text += str(item)
                text += ' , '
            else: # TODO duplicate else code....
                text += str(item)
                text += ' , '
        if len(list) > 0:
            text = text[0:-3]
        text += ']'
    return text

def transform_type(text):
    # type: (str) -> str
    """
    Translate a letter experiment to its complete type name.

    :param text: str
    :type text: str
    :return: long text
    :rtype: str
    """
    try:
        dict = {'T' : 'Theory', 'E' : 'Experiment'}
        return dict[text]
    except:
        return result_uknown()

def transform_anisotropy_energy_type(text):
    # type: (str) -> str
    """
    Translate the anisotropy energy letter to its complete type name.

    :param text: str
    :type text: str
    :return: long text
    :rtype: str
    """
    try:
        dict = { 'U' : 'Uniaxial', 'C': 'Cubic', 'P' : 'Planar'}
        return dict[text]
    except:
        return result_uknown()

def transform_kind_of_anisotropy(text):
    # type: (str) -> str
    """
    Translate the kind of anisotropy letter to its complete type name.

    :param text: str
    :type text: str
    :return: long text
    :rtype: str
    """
    try:
        dict = {'A': 'Easy axis', 'P': 'Easy plane', 'C': 'Easy cone'}
        return dict[text]
    except:
        return result_uknown()

def result_uknown():
    # type: () -> str
    """
    Translate to the default text 'None'.

    :return: 'None' text
    :rtype: str
    """
    return 'None'

def unit_translate(value, unit):
    #type: (object,str) -> str
    """
    Adds the unit to the value

    :param value: value
    :type value: object
    :param unit: unit
    :type unit: str
    :return: concatenated text
    :rtype: str
    """
    if value == None:
        return 'None'
    else:
        text = str(value)
        if len(text) > 0: #
            text = text.encode('ascii', 'ignore')
            return str(text) + ' (' + unit + ')'
        else: #if len of text is zero show None
            return 'None'

# For Plotting Tool Chart
# Define the set ot values in select field for X and Y axis...
AXIS_CHOICES = {'atom_volume' :  [ 'Atom Volume', '(' + angstrom_cubic + '/Atom)'], # Column(Numeric(9, 4)
                'stechiometry' : ['Stoichiometry', '(at.%)'], # In Molecule as Column(String(30)... WARNING NOT NUMERIC
                'compound_space_group' : [ 'Compound Space Group', '' ], # Column(SmallInteger)
                'atomic_formation_enthalpy' : [ 'Atomic Formation Enthalpy', '(eV/Atom)' ], # Column(Numeric(11, 7)
                'atomic_energy' :  [ 'Atomic Energy', '(eV/Atom)' ], # Column(Numeric(10, 7))
                'saturation_magnetization' : [ 'Saturation Magnetization', '(Tesla)' ], # Column(Numeric(6, 3)
                'magnetocrystalline_anisotropy_constants' : [ 'First Magnetocrystalline Anisotropy Constant K' + one_sub, '(' + mega_joule_per_cubic_meters + ')'], # WARNING Column(JSON)
                'curie_temperature' : [ 'Curie Temperature', '(Kelvin)' ], # Column(Numeric(8, 3))
                'anisotropy_field' : [ 'Anisostropy Field','(Tesla)' ],# Column(Numeric(6, 3)
                'remanence' : [ 'Remanence', '(Tesla)' ], # Column(Numeric(6, 3)
                'coercivity' : [ 'Coercivity', '(Tesla)' ], # Column(Numeric(6, 3)
                'energy_product' : [ 'Energy Product', '(' + kilo_joule_per_cubic_meters +')'], # Column(Numeric(8, 3)
                'domain_wall_width' : [ 'Domain Wall Width', '(nanometer)' ], # Column(Numeric(7, 3)
                'exchange_stiffness' : [ 'Exchange Stiffness', 'PJ/m' ] # Column(Numeric(7, 3)
                }

def stoichiometry_calculate_axis_values(list_items, elements):
    #type: (list[Item]) -> list[float]
    """
    Calculate the column with values for stoichiometry with the current ordered elements.

    :param list_items: list of items
    :type list_items: list[Item]
    :param elements: ordered list with the two elements
    :type elements: list[str]
    :return: list of stoichiometry x value calculated as x = m/(n+m)
    :rtype: list[float]
    """
    values = list()
    # Compile regular expressions...
    proc_element1 = re.compile(r'^.*' + elements[0] + '(0.\d*).*$')
    proc_element2 = re.compile(r'^.*' + elements[1] + '(0.\d*).*$')

    # Extract values for each tiem
    for item in list_items:
        # e.g., given Al n Fe n then where x = m / (n+m) (see documentation in mail of PNC - 18 april 2019)
        valueN = extract_stoichiometry_value(item.molecule.stechiometry, proc_element1);
        valueM = extract_stoichiometry_value(item.molecule.stechiometry, proc_element2);
        x = valueM / (valueN + valueM)
        values.append(x)
    return values

def extract_stoichiometry_value(stoichiometry, proc):
    # type: (str, parser) -> float
    """
    Calculate the stoichiometry value for an element in the formula

    :param stoichiometry : stoichiometry
    :type stoichiometry: str
    :param element: element
    :type element: str
    :param proc : regular expression compiler
    :type proc: parser
    :return: stoichiometry value of the element
    :rtype: float
    """
    result = proc.match(stoichiometry)
    if result != None and len(result.groups()) > 0: # should happen always
        value = float(result.group(1))
        return value
    else:
        return 0.0 # BAD VALUE

if __name__ == '__main__':
    object = ' '
    print(unit_translate(object,'texto'))