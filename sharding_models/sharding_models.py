#!/usr/bin/env python
# -*- coding: utf-8 -*-
# these model are used to get
from sqlalchemy import Column, Integer, BigInteger, SmallInteger, \
    ForeignKey, Float, DateTime, func, LargeBinary
from sqlalchemy.orm import relationship
from models import table_args
from db_config import Base


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