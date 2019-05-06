#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils.types.choice import ChoiceType
from models.sharding_models import *
from db_config import Base
from db_config import table_args

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    __table_args__ = table_args


class Manufacturer(Base):
    __tablename__ = 'manufacturer'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    telephone = Column(String(30), nullable=True)
    user = relationship('asset', back_populates="manufacturer")

    __table_args__ = table_args


class Asset(object):
    """Base class is a 'mixin'.
    Guidelines for declarative mixins is at:
    http://www.sqlalchemy.org/docs/orm/extensions/declarative.html#mixin-classes
    """

    TYPES = [(0, 'Motor'),
             (1, 'Bearing'),
             (2, 'Rotor'),
             (3, 'Stator'),
             ]

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    sn = Column(String(128), unique=True)
    health_indicator = Column(Float, default=85)
    lr_time = Column(DateTime, nullable=True)
    cr_time = Column(DateTime, nullable=True, default=func.now())
    md_time = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    equip_type = Column(ChoiceType(TYPES))
    memo = Column(Text, nullable=True)

    @declared_attr
    def manufacturer_id(cls):
        return Column(Integer, ForeignKey('manufacturer.id'))

    @declared_attr
    def manufacturer(cls):
        return relationship('Manufacturer', back_populates='assets')

    __table_args__ = table_args


class Motor(Asset, Base):
    __tablename__ = 'motor'
    phase_number = Column(SmallInteger, nullable=True, default=3)
    pole_pairs_number = Column(SmallInteger, nullable=True, default=2)
    turn_number = Column(SmallInteger, nullable=True, default=50)
    rated_voltage = Column(Float, nullable=True, default=220)
    rated_speed = Column(Float, nullable=True, default=5000)
    admin_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    admin = relationship('User', back_populates='motors')


class Bearing(Asset, Base):
    __tablename__ = 'bearing'

    motor_id = Column(Integer, ForeignKey('motor.id'), nullable=True)
    motor = relationship('Motor', back_populates='bearings')
    inner_race_diameter = Column(Float, nullable=True)
    inner_race_width = Column(Float, nullable=True)
    outter_race_diameter = Column(Float, nullable=True)
    outter_race_width = Column(Float, nullable=True)
    roller_diameter = Column(Float, nullable=True)
    roller_number = Column(SmallInteger, nullable=True)
    contact_angle = Column(Float, nullable=True)


class Rotor(Asset, Base):
    __tablename__ = 'rotor'

    motor_id = Column(Integer, ForeignKey('motor.id'), nullable=True)
    motor = relationship('Motor', back_populates='rotors')
    length = Column(Float, nullable=True)
    outer_diameter = Column(Float, nullable=True)
    inner_diameter = Column(Float, nullable=True)
    slot_number = Column(Integer, nullable=True)


class Stator(Asset, Base):
    __tablename__ = 'stator'

    motor_id = Column(Integer, ForeignKey('motor.id'), nullable=True)
    motor = relationship('Motor', back_populates='stators')
    length = Column(Float, nullable=True)
    outer_diameter = Column(Float, nullable=True)
    inner_diameter = Column(Float, nullable=True)
    slot_number = Column(Integer, nullable=True)


class WarningLog(Base):
    __tablename__ = 'warninglog'

    SEVERITIES = [(0, 'Attention'),
                  (1, 'Serious'),
                  ]
    id = Column(Integer, primary_key=True)
    cr_time = Column(DateTime, nullable=True, default=func.now())
    description = Column(Text, nullable=False)
    severity = Column(ChoiceType(SEVERITIES))

    motor_id = Column(Integer, ForeignKey('motor.id'))
    motor = relationship('Motor', back_populates='warningLogs')

    __table_args__ = table_args


class MonthlyRecord(Base):
    __tablename__ = 'monthlyrecord'

    id = Column(Integer, primary_key=True)
    cr_time = Column(DateTime, nullable=True, default=func.now())
    description = Column(Text, nullable=False)

    __table_args__ = table_args


for i in range(1, 4):
    CurrentsPackModel = CurrentsPack.model(motor_id=i)
    UphaseModel = Uphase.model(motor_id=i)
    VphaseModel = Vphase.model(motor_id=i)
    WphaseModel = Wphase.model(motor_id=i)
    UfeatureModel = Ufeature.model(motor_id=i)
    VfeatureModel = Vfeature.model(motor_id=i)
    WfeatureModel = Wfeature.model(motor_id=i)
    SymCompModel = SymComponent.model(motor_id=i)
