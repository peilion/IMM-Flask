#!/usr/bin/env python
# -*- coding: utf-8 -*-
# these model are used to get
from sqlalchemy import Column, Integer, BigInteger, SmallInteger, \
    ForeignKey, Float, DateTime, func, LargeBinary
from sqlalchemy.orm import relationship
from db_config import table_args, SHARDING_NUMBER
from base.basic_base import Base


class ElectricalData(object):
    _mapper = {}

    @staticmethod
    def model(motor_id):
        table_index = motor_id % 3
        class_name = 'elecdata_%d' % table_index
        ModelClass = ElectricalData._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (Base,), dict(
                __module__=__name__,
                __name__=class_name,
                __tablename__='elecdata_%d' % table_index,
                id=Column(BigInteger, primary_key=True),
                time=Column(DateTime, default=func.now()),
                motor_id=Column(Integer, ForeignKey('motor.id'), nullable=False),
                rpm=Column(SmallInteger, nullable=True, default=3000),
                ucur=Column(LargeBinary, nullable=False),
                vcur=Column(LargeBinary, nullable=False),
                wcur=Column(LargeBinary, nullable=False),
                uvolt=Column(LargeBinary, nullable=False),
                vvolt=Column(LargeBinary, nullable=False),
                wvolt=Column(LargeBinary, nullable=False),
                # motor=relationship('Motor', back_populates='packs'),
                # uphase=relationship('uphase_%d' % table_index, back_populates='pack', uselist=False),
                # vphase=relationship('vphase_%d' % table_index, back_populates='pack', uselist=False),
                # wphase=relationship('wphase_%d' % table_index, back_populates='pack', uselist=False),
                # feature=relationship('feature_%d' % table_index, back_populates='pack', uselist=False),
                # symcomponent=relationship('symcomponent_%d' % table_index, back_populates='pack', uselist=False),

                __table_args__=table_args
            ))
            ElectricalData._mapper[class_name] = ModelClass
        cls = ModelClass
        return cls


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
                ufrequency=Column(Float, default=0),
                uamplitude=Column(Float, default=0),
                uinitial_phase=Column(Float, default=0),

                vrms=Column(Float, default=0),
                vthd=Column(Float, default=0),
                vharmonics=Column(LargeBinary, default=0),
                vmax_current=Column(Float, default=0),
                vmin_current=Column(Float, default=0),
                vfbrb=Column(LargeBinary, nullable=True),
                vfrequency=Column(Float, default=0),
                vamplitude=Column(Float, default=0),
                vinitial_phase=Column(Float, default=0),

                wrms=Column(Float, default=0),
                wthd=Column(Float, default=0),
                wharmonics=Column(LargeBinary, default=0),
                wmax_current=Column(Float, default=0),
                wmin_current=Column(Float, default=0),
                wfbrb=Column(LargeBinary, nullable=True),
                wfrequency=Column(Float, default=0),
                wamplitude=Column(Float, default=0),
                winitial_phase=Column(Float, default=0),

                n_rms=Column(Float, default=0),
                p_rms=Column(Float, default=0),
                z_rms=Column(Float, default=0),
                imbalance=Column(Float, default=0),

                health_indicator=Column(Float, default=85),

                data_id=Column(BigInteger, ForeignKey('elecdata_{0}.id'.format(table_index)), unique=True),

                # pack=relationship('currentspack_%d' % table_index, back_populates=cls.base_class_name),

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
    ElectricalDataModel = ElectricalData.model(motor_id=i)
    FeatureModel = Feature.model(motor_id=i)
