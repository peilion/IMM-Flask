from marshmallow import Schema, fields


class RotorStandardSchema(Schema):
    slip = fields.Float()
    sideband_lv1 = fields.Float()
    sideband_lv2 = fields.Float()
    sideband_lv3 = fields.Float()
    md_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')


class StatorStandardSchema(Schema):
    i_imbalance_lv1 = fields.Float()
    i_imbalance_lv2 = fields.Float()
    i_imbalance_lv3 = fields.Float()

    u_imbalance_lv1 = fields.Float()
    u_imbalance_lv2 = fields.Float()
    u_imbalance_lv3 = fields.Float()

    irms_imbalance_lv1 = fields.Float()
    irms_imbalance_lv2 = fields.Float()
    irms_imbalance_lv3 = fields.Float()

    har3_lv1 = fields.Float()
    har3_lv2 = fields.Float()
    har3_lv3 = fields.Float()

    uz_type = fields.Int()
    uz_imbalance_lv1 = fields.Float()
    uz_imbalance_lv2 = fields.Float()
    uz_imbalance_lv3 = fields.Float()

    iz_type = fields.Int()
    iz_imbalance_lv1 = fields.Float()
    iz_imbalance_lv2 = fields.Float()
    iz_imbalance_lv3 = fields.Float()

    md_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')


class BearingStandardSchema(Schema):
    bpfi_lv1 = fields.Float()
    bpfi_lv2 = fields.Float()
    bpfi_lv3 = fields.Float()
    bsf_lv1 = fields.Float()
    bsf_lv2 = fields.Float()
    bsf_lv3 = fields.Float()
    bpfo_lv1 = fields.Float()
    bpfo_lv2 = fields.Float()
    bpfo_lv3 = fields.Float()
    ftf_lv1 = fields.Float()
    ftf_lv2 = fields.Float()
    ftf_lv3 = fields.Float()
    har5_lv1 = fields.Float()
    har5_lv2 = fields.Float()
    har5_lv3 = fields.Float()

    md_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')


class PowerStandardSchema(Schema):
    i_imbalance_lv1 = fields.Float()
    i_imbalance_lv2 = fields.Float()
    i_imbalance_lv3 = fields.Float()

    u_imbalance_lv1 = fields.Float()
    u_imbalance_lv2 = fields.Float()
    u_imbalance_lv3 = fields.Float()

    uthd_lv1 = fields.Float()
    uthd_lv2 = fields.Float()
    uthd_lv3 = fields.Float()

    ithd_lv1 = fields.Float()
    ithd_lv2 = fields.Float()
    ithd_lv3 = fields.Float()

    uhar_odd_lv1 = fields.Float()
    uhar_odd_lv2 = fields.Float()
    uhar_odd_lv3 = fields.Float()

    uhar_even_lv1 = fields.Float()
    uhar_even_lv2 = fields.Float()
    uhar_even_lv3 = fields.Float()

    power_factor_lv1 = fields.Float()
    power_factor_lv2 = fields.Float()
    power_factor_lv3 = fields.Float()

    md_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
