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
from persistence.transform_basic_tables import AXIS_CHOICES

# extract tuples with (key, descriptor) for list choices (not including units
list_choices = [(p[0], p[1][0]) for p in AXIS_CHOICES.items()]
list_choices.sort()
# End

class PlottingToolSearchForm(Form):

    x_axis = SelectField('X-Axis', coerce=str, choices=list_choices, default='atom_volume')
    y_axis = SelectField('Y-Axis', coerce=str, choices=list_choices, default='atomic_formation_enthalpy') #choices=[(atom.symbol, atom.symbol) for atom in ATOMS])

    element1 = SelectField('Element 1', coerce=str, choices = [ (atom.symbol, atom.symbol) for atom in ATOMS], default='Fe')
    element2 = SelectField('Element 2', coerce=str, choices=[(atom.symbol, atom.symbol) for atom in ATOMS], default='Ta')

    submit = SubmitField("Plot")




