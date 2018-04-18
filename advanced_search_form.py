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

    stechiometry_value_min = DecimalField("Stoichoimetry percentage min",  [validators.NumberRange(min=0, max=1, message='Min. number out of range')], default=0)
    stechiometry_value_max = DecimalField("Stoichoimetry percentage",  [validators.NumberRange(min=0, max=1, message='Min. number out of range')], default=1)

    submit = SubmitField("Submit")

    stechiometry_atom = SelectField('Stoichoimetry atom', coerce=str, choices =  [ (atom.symbol, atom.symbol) for atom in ATOMS], default='Fe')


