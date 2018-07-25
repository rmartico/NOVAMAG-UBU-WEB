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
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms import validators

from persistence.database_access_object import ATOMS

class AdvancedSearchForm(Form):

    compound_space_group_min = IntegerField("Compound space group min.", [validators.NumberRange(min=1, max=230, message='Min. number out of range')], default=1)
    compound_space_group_max = IntegerField("Compound space group", [validators.NumberRange(min=1, max=230, message='Max. number out of range')], default=230)

    saturation_magnetization_min = DecimalField("Saturation magnetization min",  [validators.NumberRange(min=0, max=100, message='Min. saturation out of range')], default=0, places=2)
    saturation_magnetization_max = DecimalField("Saturation magnetization", [validators.NumberRange(min=0, max=100, message='Max. saturation out of range')], default=100, places=2)

    unit_cell_formation_enthalpy_min = DecimalField("Unit cell formation enthalpy min.", [validators.NumberRange(min=-1000, max=1000, message='Min. enthalpy out of range')], default=-1000, places=2)
    unit_cell_formation_enthalpy_max = DecimalField("Unit cell formation enthalpy", [validators.NumberRange(min=-1000, max=1000, message='Max. enthalpy out of range')], default=1000, places=2)

    atomic_species = StringField("Atomic species")

    species_count = IntegerField("Species count", [validators.NumberRange(min=0, max=10, message='Number out of range')], default=2)

    stechiometry_value_min = DecimalField("Stoichiometry percentage min",  [validators.NumberRange(min=0, max=1, message='Min. number out of range')], default=0)
    stechiometry_value_max = DecimalField("Stoichiometry percentage",  [validators.NumberRange(min=0, max=1, message='Min. number out of range')], default=1)

    submit = SubmitField("Submit")

    stechiometry_atom = SelectField('Stoichiometry atom', coerce=str, choices =  [ (atom.symbol, atom.symbol) for atom in ATOMS], default='Fe')


