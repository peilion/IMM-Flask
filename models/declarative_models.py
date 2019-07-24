#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, SmallInteger, \
    ForeignKey, Float, DateTime, func
from sqlalchemy import String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.choice import ChoiceType

from base.basic_base import Base
from db_config import table_args


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    motors = relationship('Motor', back_populates='admin')

    __table_args__ = table_args


class Manufacturer(Base):
    __tablename__ = 'manufacturer'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    telephone = Column(String(30), nullable=True)

    __table_args__ = table_args


class Asset(object):
    """Base class is a 'mixin'.
    Guidelines for declarative mixins is at:
    http://www.sqlalchemy.org/docs/orm/extensions/declarative.html#mixin-classes
    """

    TYPES = [('0', 'Motor'),
             ('1', 'Bearing'),
             ('2', 'Rotor'),
             ('3', 'Stator'),
             ]
    STATUS = [
        ('0', 'Excellent'),
        ('1', 'Good'),
        ('2', 'Moderate'),
        ('3', 'Poor'),
        ('4', 'Offline'),
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
    statu = Column(ChoiceType(STATUS))

    @declared_attr
    def manufacturer_id(cls):
        return Column(Integer, ForeignKey('manufacturer.id'))

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
    bearings = relationship('Bearing', back_populates='motor')
    rotors = relationship('Rotor', back_populates='motor')
    stators = relationship('Stator', back_populates='motor')
    warninglogs = relationship('WarningLog', back_populates='motor')


class Bearing(Asset, Base):
    __tablename__ = 'bearing'

    motor_id = Column(Integer, ForeignKey('motor.id'), nullable=True)
    inner_race_diameter = Column(Float, nullable=True)
    inner_race_width = Column(Float, nullable=True)
    outter_race_diameter = Column(Float, nullable=True)
    outter_race_width = Column(Float, nullable=True)
    roller_diameter = Column(Float, nullable=True)
    roller_number = Column(SmallInteger, nullable=True)
    contact_angle = Column(Float, nullable=True)

    bpfi = Column(Float, nullable=True)
    bpfo = Column(Float, nullable=True)
    bsf = Column(Float, nullable=True)
    ftf = Column(Float, nullable=True)

    motor = relationship('Motor', back_populates='bearings')


class Rotor(Asset, Base):
    __tablename__ = 'rotor'

    motor_id = Column(Integer, ForeignKey('motor.id'), nullable=True)
    length = Column(Float, nullable=True)
    outer_diameter = Column(Float, nullable=True)
    inner_diameter = Column(Float, nullable=True)
    slot_number = Column(Integer, nullable=True)

    motor = relationship('Motor', back_populates='rotors')


class Stator(Asset, Base):
    __tablename__ = 'stator'

    motor_id = Column(Integer, ForeignKey('motor.id'), nullable=True)
    length = Column(Float, nullable=True)
    outer_diameter = Column(Float, nullable=True)
    inner_diameter = Column(Float, nullable=True)
    slot_number = Column(Integer, nullable=True)

    motor = relationship('Motor', back_populates='stators')


class WarningLog(Base):
    __tablename__ = 'warninglog'

    SEVERITIES = [('0', 'Attention'),
                  ('1', 'Serious'),
                  ]
    id = Column(Integer, primary_key=True)
    cr_time = Column(DateTime, nullable=True, default=func.now())
    description = Column(Text, nullable=False)
    severity = Column(ChoiceType(SEVERITIES))

    motor_id = Column(Integer, ForeignKey('motor.id'))
    motor = relationship('Motor', back_populates='warninglogs')

    __table_args__ = table_args


class MonthlyRecord(Base):
    __tablename__ = 'monthlyrecord'
    __table_args__ = table_args

    id = Column(Integer, primary_key=True)
    cr_time = Column(DateTime, nullable=True, default=func.now())
    description = Column(Text, nullable=False)



class StatorEvalStd(Base):
    __tablename__ = 'stator_evaluate_standard'
    __table_args__ = table_args

    id = Column(Integer, primary_key=True)
    i_imbalance_lv1 = Column(Float, default=2)
    i_imbalance_lv2 = Column(Float, default=4)
    i_imbalance_lv3 = Column(Float, default=10)

    u_imbalance_lv1 = Column(Float, default=2)
    u_imbalance_lv2 = Column(Float, default=4)
    u_imbalance_lv3 = Column(Float, default=10)

    irms_imbalance_lv1 = Column(Float, default=2)
    irms_imbalance_lv2 = Column(Float, default=4)
    irms_imbalance_lv3 = Column(Float, default=10)

    har3_lv1 = Column(Float, default=0.5)
    har3_lv2 = Column(Float, default=1)
    har3_lv3 = Column(Float, default=2)

    uz_type = Column(SmallInteger,default=1) # 0:额定报警 1:零序/正序报警, 针对绝缘故障
    uz_imbalance_lv1 = Column(Float, default=2)
    uz_imbalance_lv2 = Column(Float, default=4)
    uz_imbalance_lv3 = Column(Float, default=10)

    iz_type = Column(SmallInteger,default=1) # 0:额定报警 1:零序/正序报警，针对单相接地
    iz_imbalance_lv1 = Column(Float, default=2)
    iz_imbalance_lv2 = Column(Float, default=4)
    iz_imbalance_lv3 = Column(Float, default=10)

    md_time = Column(DateTime, default=func.now(), onupdate=func.now())


class RotorEvalStd(Base):
    __tablename__ = 'rotor_evaluate_standard'
    __table_args__ = table_args

    id = Column(Integer, primary_key=True)
    slip = Column(Float,default=0.006)
    sideband_lv1 = Column(Float,default=0.2)
    sideband_lv2 = Column(Float, default=1.58)
    sideband_lv3 = Column(Float, default=3.16)

    md_time = Column(DateTime, default=func.now(), onupdate=func.now())

class BearingEvalStd(Base):
    __tablename__ = 'bearing_evaluate_standard'
    __table_args__ = table_args

    id = Column(Integer, primary_key=True)

    bpfi_lv1 = Column(Float, default=0.5)
    bpfi_lv2 = Column(Float, default=1.0)
    bpfi_lv3 = Column(Float, default=2.0)

    bsf_lv1 = Column(Float, default=0.5)
    bsf_lv2 = Column(Float, default=1.0)
    bsf_lv3 = Column(Float, default=2.0)

    bpfo_lv1 = Column(Float, default=0.5)
    bpfo_lv2 = Column(Float, default=1.0)
    bpfo_lv3 = Column(Float, default=2.0)

    ftf_lv1 = Column(Float, default=0.5)
    ftf_lv2 = Column(Float, default=1.0)
    ftf_lv3 = Column(Float, default=2.0)

    har5_lv1 = Column(Float, default=0.5)
    har5_lv2 = Column(Float, default=1.0)
    har5_lv3 = Column(Float, default=2.0)

    md_time = Column(DateTime, default=func.now(), onupdate=func.now())

class PowerEvalStd(Base):
    __tablename__ = 'power_evaluate_standard'
    __table_args__ = table_args

    id = Column(Integer, primary_key=True)

    i_imbalance_lv1 = Column(Float, default=2)
    i_imbalance_lv2 = Column(Float, default=4)
    i_imbalance_lv3 = Column(Float, default=10)

    u_imbalance_lv1 = Column(Float, default=2)
    u_imbalance_lv2 = Column(Float, default=4)
    u_imbalance_lv3 = Column(Float, default=10)

    uthd_lv1 = Column(Float,default=4/3)
    uthd_lv2 = Column(Float, default=8/3)
    uthd_lv3 = Column(Float, default=4)

    ithd_lv1 = Column(Float,default=4/3)
    ithd_lv2 = Column(Float, default=8/3)
    ithd_lv3 = Column(Float, default=4)

    uhar_odd_lv1 = Column(Float, default=3.2/3)
    uhar_odd_lv2 = Column(Float, default=3.2*2/3)
    uhar_odd_lv3 = Column(Float, default=3.2)

    uhar_even_lv1 = Column(Float, default=0.5)
    uhar_even_lv2 = Column(Float, default=1.0)
    uhar_even_lv3 = Column(Float, default=1.5)

    power_factor_lv1 = Column(Float, default=0.8)
    power_factor_lv2 = Column(Float, default=0.6)
    power_factor_lv3 = Column(Float, default=0.4)

    md_time = Column(DateTime, default=func.now(), onupdate=func.now())
