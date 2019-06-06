from marshmallow import Schema, fields, pprint
import numpy as np
from models.declarative_models import WarningLog, Motor
from json import dump


class Blob(fields.Field):
    """
    Read only blob field
    """

    def _serialize(self, value, attr, obj, **kwargs):
        return [round(float(item), 3) for item in np.fromstring(value, dtype=np.float32)]

    @staticmethod
    def myserialize(value):
        return [round(float(item), 3) for item in np.fromstring(value, dtype=np.float32)]


class Array(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        return [round(float(item), 3) for item in value]

    @staticmethod
    def static_serialize(value):
        return [round(float(item), 3) for item in value]


class FeatureSchema(Schema):
    urms = fields.Float()
    vrms = fields.Float()
    wrms = fields.Float()
    uthd = fields.Float()
    vthd = fields.Float()
    wthd = fields.Float()
    uharmonics = Blob(dump_only=True)
    vharmonics = Blob(dump_only=True)
    wharmonics = Blob(dump_only=True)
    ufbrb = Blob(dump_only=True)
    vfbrb = Blob(dump_only=True)
    wfbrb = Blob(dump_only=True)
    umax_current = fields.Float()
    vmax_current = fields.Float()
    wmax_current = fields.Float()
    umin_current = fields.Float()
    vmin_current = fields.Float()
    wmin_current = fields.Float()
    n_rms = fields.Float()
    p_rms = fields.Float()
    z_rms = fields.Float()
    imbalance = fields.Float()
    frequency = fields.Float()
    ufft = Array(dump_only=True)
    vfft = Array(dump_only=True)
    wfft = Array(dump_only=True)


class WarningSchema(Schema):
    name = fields.String()
    description = fields.String()
    cr_time = fields.DateTime()
    severity = fields.Method("severity_mapper")

    @staticmethod
    def severity_mapper(obj):
        return obj.severity.value


class PhaseSchema(Schema):
    frequency = fields.Float()
    amplitude = fields.Float()
    initial_phase = fields.Float()
    wave = Blob(dump_only=True)
    u = Blob(dump_only=True)
    v = Blob(dump_only=True)
    w = Blob(dump_only=True)


class PackSchema(Schema):
    time = fields.DateTime()
    rpm = fields.Integer()
    id = fields.Integer()
    name = fields.String()
    sn = fields.String()
    statu = fields.Method("statu_mapper")
    ufft = Array(dump_only=True)
    vfft = Array(dump_only=True)
    wfft = Array(dump_only=True)
    usignal = Array(dump_only=True)
    vsignal = Array(dump_only=True)
    wsignal = Array(dump_only=True)
    uamp = fields.Float()
    vamp = fields.Float()
    wamp = fields.Float()
    ufreq = fields.Float()
    vfreq = fields.Float()
    wfreq = fields.Float()
    uip = fields.Float()
    vip = fields.Float()
    wip = fields.Float()
    sampling_rate = fields.Integer()

    @staticmethod
    def statu_mapper(obj):
        return obj['statu'].value


class EnvelopeSchema(Schema):
    ufft = Array(dump_only=True)
    vfft = Array(dump_only=True)
    wfft = Array(dump_only=True)
    u = Array(dump_only=True)
    v = Array(dump_only=True)
    w = Array(dump_only=True)
    uenvelope = Array(dump_only=True)
    venvelope = Array(dump_only=True)
    wenvelope = Array(dump_only=True)
