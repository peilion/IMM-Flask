#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger, \
    ForeignKey, Float, DateTime, func, Text, LargeBinary
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db_config import Base
import datetime
from sqlalchemy_utils.types.choice import ChoiceType

table_args = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8'
}


class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)

    __table_args__ = table_args


class Manufacturer(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
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
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'))
    manufacturer = relationship('Manufacturer', back_populates='assets')
    health_indicator = Column(Float, default=85)
    lr_time = Column(DateTime, nullable=True)
    cr_time = Column(DateTime, nullable=True, default=func.now())
    md_time = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    equip_type = Column(ChoiceType(TYPES))
    memo = Column(Text, nullable=True)

    __table_args__ = table_args


class Motor(Asset, Base):
    phase_number = Column(SmallInteger, nullable=True, default=3)
    pole_pairs_number = Column(SmallInteger, nullable=True, default=2)
    turn_number = Column(SmallInteger, nullable=True, default=50)
    rated_voltage = Column(Float, nullable=True, default=220)
    rated_speed = Column(Float, nullable=True, default=5000)
    admin_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    admin = relationship('User', back_populates='motors')


class Bearing(Asset, Base):
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
    motor_id = Column(Integer, ForeignKey('motor.id'), nullable=True)
    motor = relationship('Motor', back_populates='rotors')
    length = Column(Float, nullable=True)
    outer_diameter = Column(Float, nullable=True)
    inner_diameter = Column(Float, nullable=True)
    slot_number = Column(Integer, nullable=True)


class Stator(Asset, Base):
    motor_id = Column(Integer, ForeignKey('motor.id'), nullable=True)
    motor = relationship('Motor', back_populates='stators')
    length = Column(Float, nullable=True)
    outer_diameter = Column(Float, nullable=True)
    inner_diameter = Column(Float, nullable=True)
    slot_number = Column(Integer, nullable=True)


class CurrentsPack(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'currentspack_%d' % table_index
        ModelClass = CurrentsPack._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='curentspack_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                time=Column(DateTime, default=func.now()),
                motor_id=Column(Integer, ForeignKey('motor.id'), nullable=False),
                sampling_tate=Column(Integer, nullable=True),
                rpm=Column(SmallInteger, default=3000),

                motor=relationship('Motor', back_populates='packs'),
                uphase=relationship('uphase_%d' % table_index, back_populates='pack', uselist=False),
                vphase=relationship('vphase_%d' % table_index, back_populates='pack', uselist=False),
                wphase=relationship('wphase_%d' % table_index, back_populates='pack', uselist=False),
                ufeature=relationship('ufeature_%d' % table_index, back_populates='pack', uselist=False),
                vfeature=relationship('vfeature_%d' % table_index, back_populates='pack', uselist=False),
                wfeature=relationship('wfeature_%d' % table_index, back_populates='pack', uselist=False),
                symcomponent=relationship('symcomponent_%d' % table_index, back_populates='pack', uselist=False),

                __table_args__=table_args
            ))
            CurrentsPack._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class Uphase(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'uphase_%d' % table_index
        ModelClass = Uphase._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='uphase_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                signal=Column(LargeBinary, nullable=False),
                frequency=Column(Float, default=0),
                amplitude=Column(Float, default=0),
                initial_phase=Column(Float, default=0),
                pack_id=Column(Integer, ForeignKey('curentspack_{0}.id'.format(table_index))),

                pack=relationship('currentspack_%d' % table_index, back_populates='uphase'),

                __table_args__=table_args
            ))
            Uphase._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class Vphase(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'vphase_%d' % table_index
        ModelClass = Vphase._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='vphase_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                signal=Column(LargeBinary, nullable=False),
                frequency=Column(Float, default=0),
                amplitude=Column(Float, default=0),
                initial_phase=Column(Float, default=0),
                pack_id=Column(Integer, ForeignKey('curentspack_{0}.id'.format(table_index))),

                pack=relationship('currentspack_%d' % table_index, back_populates='vphase'),

                __table_args__=table_args
            ))
            Vphase._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class Wphase(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'wphase_%d' % table_index
        ModelClass = Wphase._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='vphase_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                signal=Column(LargeBinary, nullable=False),
                frequency=Column(Float, default=0),
                amplitude=Column(Float, default=0),
                initial_phase=Column(Float, default=0),
                pack_id=Column(Integer, ForeignKey('curentspack_{0}.id'.format(table_index))),

                pack=relationship('currentspack_%d' % table_index, back_populates='wphase'),

                __table_args__=table_args
            ))
            Wphase._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class Ufeature(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'ufeature_%d' % table_index
        ModelClass = Ufeature._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='ufeature_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                rms=Column(Float, default=0),
                thd=Column(Float, default=0),
                harmonics=Column(LargeBinary, default=0),
                max_current=Column(Float, default=0),
                min_current=Column(Float, default=0),
                fbrb=Column(LargeBinary, nullable=True),

                pack_id=Column(Integer, ForeignKey('curentspack_{0}.id'.format(table_index))),

                pack=relationship('currentspack_%d' % table_index, back_populates='wphase'),

                __table_args__=table_args
            ))
            Ufeature._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class Vfeature(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'vfeature_%d' % table_index
        ModelClass = Vfeature._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='vfeature_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                rms=Column(Float, default=0),
                thd=Column(Float, default=0),
                harmonics=Column(LargeBinary, default=0),
                max_current=Column(Float, default=0),
                min_current=Column(Float, default=0),
                fbrb=Column(LargeBinary, nullable=True),

                pack_id=Column(Integer, ForeignKey('curentspack_{0}.id'.format(table_index))),

                pack=relationship('currentspack_%d' % table_index, back_populates='wphase'),

                __table_args__=table_args
            ))
            Vfeature._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class Wfeature(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'wfeature_%d' % table_index
        ModelClass = Wfeature._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='wfeature_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                rms=Column(Float, default=0),
                thd=Column(Float, default=0),
                harmonics=Column(LargeBinary, default=0),
                max_current=Column(Float, default=0),
                min_current=Column(Float, default=0),
                fbrb=Column(LargeBinary, nullable=True),

                pack_id=Column(Integer, ForeignKey('curentspack_{0}.id'.format(table_index))),

                pack=relationship('currentspack_%d' % table_index, back_populates='wphase'),

                __table_args__=table_args
            ))
            Wfeature._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class SymComponent(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'symcomponent_%d' % table_index
        ModelClass = SymComponent._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='symcomponent_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                n_rms=Column(Float, default=0),
                p_rms=Column(Float, default=0),
                z_rms=Column(Float, default=0),
                imbalance=Column(Float, default=0),

                pack_id=Column(Integer, ForeignKey('curentspack_{0}.id'.format(table_index))),

                pack=relationship('currentspack_%d' % table_index, back_populates='symcomponent'),

                __table_args__=table_args
            ))
            SymComponent._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class WarningLog(Base):
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
    id = Column(Integer, primary_key=True)
    cr_time = Column(DateTime, nullable=True, default=func.now())
    description = Column(Text, nullable=False)

    __table_args__ = table_args
