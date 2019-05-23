from marshmallow import Schema, fields, pprint
import numpy as np
from models.declarative_models import WarningLog,Motor
from json import dump


class Blob(fields.Field):
    """
    Read only blob field
    """

    def _serialize(self, value, attr, obj, **kwargs):
        return [round(float(item), 3) for item in np.fromstring(value, dtype=np.float32)]


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


class PackSchema(Schema):
    time = fields.DateTime()
    rpm = fields.Integer()
    id = fields.Integer()
