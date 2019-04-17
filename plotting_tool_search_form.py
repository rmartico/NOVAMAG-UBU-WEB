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

from flask_wtf import Form
from wtforms import StringField, SubmitField, DecimalField, SelectField, BooleanField

from persistence.database_access_object import ATOMS

# Define the set ot values in select field for X and Y axis...
AXIS_CHOICES = {'atom_volume' : 'Atom Volume', # Column(Numeric(9, 4)
                'stoichiometry' : 'Stoichiometry', # In Molecule as Column(String(30)... WARNING NOT NUMERIC
                'compound_space_group' : 'Compound Space Group', # Column(SmallInteger)
                'atomic_formation_enthalpy' :  'Atomic Formation Enthalpy', # Column(Numeric(11, 7)
                'atomic_energy' : 'Atomic Energy', # Column(Numeric(10, 7))
                'saturation_magnetization' : 'Saturation Magnetization', # Column(Numeric(6, 3)
                'magnetocrystalline_anisotropy_constants' : 'First Magnetocrystalline Anisotropy Constant K1', # WARNING Column(JSON)
                'curie_temperature' : 'Curie Temperature', # Column(Numeric(8, 3))
                'anisotropy_field' : 'Anisostropy Field', # Column(Numeric(6, 3)
                'remanence' : 'Remanence', # Column(Numeric(6, 3)
                'coercivity' : 'Coercivity', # Column(Numeric(6, 3)
                'energy_product' : 'Energy Product', # Column(Numeric(8, 3)
                'domain_wall_width' : 'Domain Wall Width', # Column(Numeric(7, 3)
                'exchange_stiffness' : 'Exchange Stiffness' # Column(Numeric(7, 3)
                }
list_choices = [p for p in AXIS_CHOICES.items()]
list_choices.sort()
# End

class PlottingToolSearchForm(Form):

    x_axis = SelectField('X-Axis', coerce=str, choices=list_choices)
    y_axis = SelectField('Y-Axis', coerce=str, choices=list_choices) #choices=[(atom.symbol, atom.symbol) for atom in ATOMS])

    element1 = SelectField('Element 1', coerce=str, choices = [ (atom.symbol, atom.symbol) for atom in ATOMS], default='Fe')
    element2 = SelectField('Element 2', coerce=str, choices=[(atom.symbol, atom.symbol) for atom in ATOMS], default='Ge')

    submit = SubmitField("Plot")




