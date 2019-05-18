#!/usr/bin/env python
# -*- coding: utf-8 -*-
# these model are used to get
from sqlalchemy import Column, Integer, BigInteger, SmallInteger, \
    ForeignKey, Float, DateTime, func, LargeBinary
from sqlalchemy.orm import relationship
from db_config import table_args, SHARDING_NUMBER
from base.base import Base


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
                __tablename__='currentspack_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                time=Column(DateTime, default=func.now()),
                motor_id=Column(Integer, ForeignKey('motor.id'), nullable=False),
                sampling_rate=Column(Integer, nullable=True),
                rpm=Column(SmallInteger, default=3000),

                motor=relationship('Motor', back_populates='packs'),
                uphase=relationship('uphase_%d' % table_index, back_populates='pack', uselist=False),
                vphase=relationship('vphase_%d' % table_index, back_populates='pack', uselist=False),
                wphase=relationship('wphase_%d' % table_index, back_populates='pack', uselist=False),
                feature=relationship('feature_%d' % table_index, back_populates='pack', uselist=False),
                symcomponent=relationship('symcomponent_%d' % table_index, back_populates='pack', uselist=False),

                __table_args__=table_args
            ))
            CurrentsPack._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


class Uphase(object):
    _mapper = {}
    base_class_name = 'uphase'

    @classmethod
    def model(cls, motor_id):
        table_index = motor_id % SHARDING_NUMBER
        class_name = cls.base_class_name + '_%d' % table_index
        ModelClass = cls._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__=class_name,
                id=Column(BigInteger, primary_key=True),
                wave=Column(LargeBinary, nullable=False),
                frequency=Column(Float, default=0),
                amplitude=Column(Float, default=0),
                initial_phase=Column(Float, default=0),
                pack_id=Column(BigInteger, ForeignKey('currentspack_{0}.id'.format(table_index)),unique=True),

                pack=relationship('currentspack_%d' % table_index, back_populates=cls.base_class_name),

                __table_args__=table_args
            ))
            cls._mapper[class_name] = ModelClass
        mapper = ModelClass
        return mapper


class Vphase(Uphase):
    _mapper = {}
    base_class_name = 'vphase'


class Wphase(Uphase):
    _mapper = {}
    base_class_name = 'wphase'


class Feature(object):
    _mapper = {}
    base_class_name = 'feature'

    @classmethod
    def model(cls, motor_id):
        table_index = motor_id % SHARDING_NUMBER
        class_name = cls.base_class_name + '_%d' % table_index
        ModelClass = cls._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__=class_name,
                id=Column(BigInteger, primary_key=True),
                urms=Column(Float, default=0),
                uthd=Column(Float, default=0),
                uharmonics=Column(LargeBinary, default=0),
                umax_current=Column(Float, default=0),
                umin_current=Column(Float, default=0),
                ufbrb=Column(LargeBinary, nullable=True),

                vrms=Column(Float, default=0),
                vthd=Column(Float, default=0),
                vharmonics=Column(LargeBinary, default=0),
                vmax_current=Column(Float, default=0),
                vmin_current=Column(Float, default=0),
                vfbrb=Column(LargeBinary, nullable=True),

                wrms=Column(Float, default=0),
                wthd=Column(Float, default=0),
                wharmonics=Column(LargeBinary, default=0),
                wmax_current=Column(Float, default=0),
                wmin_current=Column(Float, default=0),
                wfbrb=Column(LargeBinary, nullable=True),

                n_rms=Column(Float, default=0),
                p_rms=Column(Float, default=0),
                z_rms=Column(Float, default=0),
                imbalance=Column(Float, default=0),

                pack_id=Column(BigInteger, ForeignKey('currentspack_{0}.id'.format(table_index)),unique=True),

                pack=relationship('currentspack_%d' % table_index, back_populates=cls.base_class_name),

                __table_args__=table_args
            ))
            cls._mapper[class_name] = ModelClass
        mapper = ModelClass
        return mapper


# class SymComponent(object):
#     _mapper = {}
#
#     @staticmethod
#     def model(motor_id):
#         table_index = motor_id % SHARDING_NUMBER
#         class_name = 'symcomponent_%d' % table_index
#         ModelClass = SymComponent._mapper.get(class_name, None)
#         if ModelClass is None:
#             ModelClass = type(class_name, (Base,), dict(
#                 __module__=__name__,
#                 __name__=class_name,
#                 __tablename__='symcomponent_%d' % table_index,
#                 id=Column(BigInteger, primary_key=True),
#
#
#                 pack_id=Column(BigInteger, ForeignKey('currentspack_{0}.id'.format(table_index))),
#
#                 pack=relationship('currentspack_%d' % table_index, back_populates='symcomponent'),
#
#                 __table_args__=table_args
#             ))
#             SymComponent._mapper[class_name] = ModelClass
#         cls = ModelClass
#         return cls


for i in range(1, 4):
    CurrentsPackModel = CurrentsPack.model(motor_id=i)
    UphaseModel = Uphase.model(motor_id=i)
    VphaseModel = Vphase.model(motor_id=i)
    WphaseModel = Wphase.model(motor_id=i)
    FeatureModel = Feature.model(motor_id=i)
