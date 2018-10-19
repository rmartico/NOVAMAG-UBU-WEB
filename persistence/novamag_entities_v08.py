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

# coding: utf-8

# RMS Comment: this file is auotomatically generated with sqlacodegen.

from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()
metadata = Base.metadata


class Atom(Base):
    __tablename__ = 'atoms'
    __table_args__ = {'schema': 'public'}

    symbol = Column(String(2), primary_key=True)


class AttachedFile(Base):
    __tablename__ = 'attached_files'
    __table_args__ = (
        ForeignKeyConstraint(['file_type', 'is_text'], ['public.file_types.file_type', 'public.file_types.is_text']),
        {'schema': 'public'}
    )

    mafid = Column(ForeignKey('public.items.mafid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    file_name = Column(String(50), primary_key=True, nullable=False)
    file_type = Column(String(20), nullable=False)
    is_text = Column(Boolean, nullable=False)
    blob_content = Column(LargeBinary)
    info = Column(Text)

    file_type1 = relationship('FileType')
    item = relationship('Item')




class Composition(Base):
    __tablename__ = 'composition'
    __table_args__ = {'schema': 'public'}

    symbol = Column(ForeignKey('public.atoms.symbol'), primary_key=True, nullable=False)
    formula = Column(ForeignKey('public.molecules.formula'), primary_key=True, nullable=False)
    numb_of_occurrences = Column(Numeric(4, 3))

    molecule = relationship('Molecule')
    atom = relationship('Atom')


class FileType(Base):
    __tablename__ = 'file_types'
    __table_args__ = {'schema': 'public'}

    file_type = Column(String(20), primary_key=True, nullable=False, unique=True)
    is_text = Column(Boolean, primary_key=True, nullable=False)
    regexp = Column(String(50), nullable=False)




class Item(Base):
    __tablename__ = 'items'
    __table_args__ = (
        CheckConstraint("((type = 'E'::bpchar) AND (unit_cell_energy IS NULL) AND (interatomic_potentials_info IS NULL) AND (magnetic_free_energy IS NULL) AND (magnetic_free_energy_info IS NULL) AND (unit_cell_spin_polarization IS NULL) AND (magnetocrystalline_anisotropy_energy IS NULL) AND (exchange_integrals IS NULL) AND (exchange_info IS NULL)) OR (type = 'T'::bpchar)"),
        CheckConstraint('(anisotropy_field >= (0)::numeric) AND (anisotropy_field <= (100)::numeric)'),
        CheckConstraint('(coercivity >= (0)::numeric) AND (coercivity <= (100)::numeric)'),
        CheckConstraint('(compound_space_group >= 1) AND (compound_space_group <= 230)'),
        CheckConstraint('(curie_temperature >= (0)::numeric) AND (curie_temperature <= (10000)::numeric)'),
        CheckConstraint('(domain_wall_width >= (0)::numeric) AND (domain_wall_width <= (1000)::numeric)'),
        CheckConstraint('(energy_product >= (0)::numeric) AND (energy_product <= (10000)::numeric)'),
        CheckConstraint('(exchange_stiffness >= (0)::numeric) AND (exchange_stiffness <= (1000)::numeric)'),
        CheckConstraint("(magnetic_free_energy >= ('-100000'::integer)::numeric) AND (magnetic_free_energy <= (100000)::numeric)"),
        CheckConstraint('(magnetization_temperature >= (0)::numeric) AND (magnetization_temperature <= (100000)::numeric)'),
        CheckConstraint('(remanence >= (0)::numeric) AND (remanence <= (100)::numeric)'),
        CheckConstraint('(saturation_magnetization >= (0)::numeric) AND (saturation_magnetization <= (100)::numeric)'),
        CheckConstraint("(unit_cell_energy >= ('-100000'::integer)::numeric) AND (unit_cell_energy <= (100000)::numeric)"),
        CheckConstraint("(unit_cell_formation_enthalpy >= ('-1000'::integer)::numeric) AND (unit_cell_formation_enthalpy <= (1000)::numeric)"),
        CheckConstraint('(unit_cell_spin_polarization >= (0)::numeric) AND (unit_cell_spin_polarization <= (10000)::numeric)'),
        CheckConstraint('(unit_cell_volume >= (0)::numeric) AND (unit_cell_volume <= (100000)::numeric)'),
        CheckConstraint("anisotropy_energy_type = ANY (ARRAY['U'::bpchar, 'C'::bpchar, 'P'::bpchar])"),
        CheckConstraint("kind_of_anisotropy = ANY (ARRAY['A'::bpchar, 'P'::bpchar, 'C'::bpchar])"),
        CheckConstraint("type = ANY (ARRAY['E'::bpchar, 'T'::bpchar])"),
        {'schema': 'public'}
    )

    mafid = Column(Integer, primary_key=True, server_default=text("nextval('public.items_mafid_seq'::regclass)")) # RMS changed
    confidential = Column(Boolean, server_default=text("false"))
    type = Column(String(1), nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    summary = Column(Text)
    formula = Column(ForeignKey('public.molecules.formula'), nullable=False)
    production_info = Column(String(255))
    atomic_species = Column(String(255))
    species_count = Column(Integer)
    compound_space_group = Column(SmallInteger)
    lattice_system = Column(String(4))
    unit_cell_atom_count = Column(SmallInteger)
    unit_cell_volume = Column(Numeric(9, 4))
    atom_volume = Column(Numeric(9, 4))
    lattice_parameters = Column(JSON)
    lattice_angles = Column(JSON)
    atomic_positions = Column(JSON)
    crystal_info = Column(Text)
    unit_cell_energy = Column(Numeric(12, 7))
    atomic_energy = Column(Numeric(10, 7))
    unit_cell_formation_enthalpy = Column(Numeric(10, 6))
    atomic_formation_enthalpy = Column(Numeric(11, 7))
    energy_info = Column(Text)
    interatomic_potentials_info = Column(Text)
    magnetic_free_energy = Column(Numeric(11, 6))
    magnetic_free_energy_info = Column(Text)
    unit_cell_spin_polarization = Column(Numeric(11, 6))
    atomic_spin_specie = Column(JSON)
    saturation_magnetization = Column(Numeric(6, 3))
    magnetization_temperature = Column(Numeric(8, 3))
    magnetization_info = Column(Text)
    magnetocrystalline_anisotropy_energy = Column(JSON)
    anisotropy_energy_type = Column(String(1))
    magnetocrystalline_anisotropy_constants = Column(JSON)
    kind_of_anisotropy = Column(String(1))
    anisotropy_info = Column(String(255))
    exchange_integrals = Column(JSON)
    exchange_info = Column(Text)
    magnetic_order = Column(ForeignKey('public.magnetic_orders.magnetic_order'))
    curie_temperature = Column(Numeric(8, 3))
    curie_temperature_info = Column(Text)
    anisotropy_field = Column(Numeric(6, 3))
    remanence = Column(Numeric(6, 3))
    coercivity = Column(Numeric(6, 3))
    energy_product = Column(Numeric(8, 3))
    hysteresis_info = Column(Text)
    domain_wall_width = Column(Numeric(7, 3))
    domain_wall_info = Column(Text)
    exchange_stiffness = Column(Numeric(7, 3))
    exchange_stiffness_info = Column(Text)
    reference = Column(String(255))
    comments = Column(Text)

    molecule = relationship('Molecule', lazy='joined')  # RMS: Warning. To load molecule before showing stoichiometry
    magnetic_order1 = relationship('MagneticOrder')


class MagneticOrder(Base):
    __tablename__ = 'magnetic_orders'
    __table_args__ = {'schema': 'public'}

    magnetic_order = Column(String(20), primary_key=True)


class Molecule(Base):
    __tablename__ = 'molecules'
    __table_args__ = {'schema': 'public'}

    formula = Column(String(20), primary_key=True)
    stechiometry = Column(String(30), nullable=False)

# RMS moved t_authoring and Author to the end of the file...

t_authoring = Table(
    'authoring', metadata,
    Column('author', ForeignKey('public.authors.author'), primary_key=True, nullable=False),
    Column('mafid', ForeignKey('public.items.mafid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    schema='public'
)


class Author(Base):
    __tablename__ = 'authors'
    __table_args__ = {'schema': 'public'}

    author = Column(String(80), primary_key=True)

    items = relationship('Item', secondary=t_authoring, backref="authors") # RMS added backref="users"
    #users = relationship("User", secondary=user_group_association_table, backref="groups")