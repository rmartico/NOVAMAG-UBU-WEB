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


angstrom = u'\u00C5ngstr\u00F6m'
angstrom_cubic = u'\u00C5ngstr\u00F6m'u'\u00B3'

'''
Escape characters in path to download file.
'''
def parse_url(attached_file):
    url = str(attached_file.mafid) + "&" + attached_file.file_name
    return url

'''
Parse list to string without u character
'''
def transform_list(list):
    text = None
    if list is not None:
        text = '['
        for item in list:
            if (type(item) is str):
                text += str(item)
                text += ' , '
            else:
                text += str(item)
                text += ' , '
        if len(list) > 0:
            text = text[0:-3]
        text += ']'
    return text



def transform_type(text):
    # type: (str) -> str
    try:
        dict = {'T' : 'Theory', 'E' : 'Experiment'}
        return dict[text]
    except:
        return result_uknown()

def transform_anisotropy_energy_type(text):
    try:
        dict = { 'U' : 'Uniaxial', 'C': 'Cubic', 'P' : 'Planar'}
        return dict[text]
    except:
        return result_uknown()

def transform_kind_of_anisotropy(text):
    try:
        dict = {'A': 'Easy axis', 'P': 'Planar easy axis', 'C': 'Easy cone'}
        return dict[text]
    except:
        return result_uknown()

def result_uknown():
    return 'None'

def unit_translate(value, unit):
    if value == None:
        return 'None'
    else:
        text = str(value)
        text = text.encode('ascii', 'ignore')
        return str(text) + ' (' + unit + ')'

if __name__ == '__main__':
    object = ' '
    print(unit_translate(object,'texto'))