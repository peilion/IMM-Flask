from marshmallow import Schema, fields, pprint


class UserSchema(Schema):
    name = fields.String()


class AssetSchema(Schema):
    id = fields.Integer()
    statu = fields.Method("statu_mapper")
    name = fields.Str()
    sn = fields.Str()
    health_indicator = fields.Float()
    lr_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    memo = fields.Str()
    admin = fields.Nested(UserSchema)

    @staticmethod
    def statu_mapper(obj):
        return obj.statu.value


class RotorSchema(AssetSchema):
    length = fields.Float()
    outer_diameter = fields.Float()
    inner_diameter = fields.Float()
    slot_number = fields.Integer()


class StatorSchema(RotorSchema):
    pass


class BearingSchema(AssetSchema):
    inner_race_diameter = fields.Float()
    inner_race_width = fields.Float()
    outter_race_diameter = fields.Float()
    outter_race_width = fields.Float()
    roller_diameter = fields.Float()
    roller_number = fields.Integer()
    contact_angle = fields.Float()


class MotorSchema(AssetSchema):
    phase_number = fields.Integer()
    pole_pairs_number = fields.Integer()
    turn_number = fields.Integer()
    rated_voltage = fields.Float()
    rated_speed = fields.Float()
    admin = fields.String()


class EquipGroupSchema(AssetSchema):
    rotors = fields.Nested(AssetSchema, many=True)
    stators = fields.Nested(AssetSchema, many=True)
    bearings = fields.Nested(AssetSchema, many=True)


# only=('id', 'statu', 'name', 'sn', 'health_indicator', 'lr_time', 'memo')


class MotorStatuStatisticSchema(Schema):
    excellent = fields.Integer(attribute='0', default=0)
    good = fields.Integer(attribute='1', default=0)
    moderate = fields.Integer(attribute='2', default=0)
    poor = fields.Integer(attribute='3', default=0)


class MotorCompStatisticSchema(Schema):
    name = fields.String()
    bearnings = fields.Integer(attribute='nb')
    stators = fields.Integer(attribute='ns')
    rotors = fields.Integer(attribute='nr')
