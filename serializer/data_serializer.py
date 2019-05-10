from marshmallow import Schema, fields, pprint
import numpy as np


class Blob(fields.Field):
    """
    Read only blob field
    """

    def _serialize(self, value, attr, obj, **kwargs):
        return np.fromstring(value, dtype=np.float32)


class TrendSchema(Schema):
    time = fields.Method('marsh_with_datetime_list')
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

    @staticmethod
    def statu_mapper(obj):
        return obj.statu.value