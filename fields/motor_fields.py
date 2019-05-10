from flask_restful import fields

rotor_detail_fields = {
    'length': fields.Float,
    'outer_diameter': fields.Float,
    'inner_diameter': fields.Float,
    'slot_number': fields.Integer
}

rotor_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'sn': fields.String,
    'health_indicator': fields.Float,
    'lr_time': fields.datetime,
    'memo': fields.String,
    'detail': fields.Nested(rotor_detail_fields)
}

bearing_detail_fields = {
    'inner_race_diameter': fields.Float,
    'inner_race_width': fields.Float,
    'outter_race_diameter': fields.Float,
    'outter_race_width': fields.Float,
    'roller_diameter': fields.Float,
    'roller_number': fields.Integer,
    'contact_angle': fields.Float,
}

bearing_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'sn': fields.String,
    'health_indicator': fields.Float,
    'lr_time': fields.datetime,
    'memo': fields.String,
    'detail': fields.Nested(bearing_detail_fields)
}

stator_detail_fields = {
    'length': fields.Float,
    'outer_diameter': fields.Float,
    'inner_diameter': fields.Float,
    'slot_number': fields.Integer
}

stator_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'sn': fields.String,
    'health_indicator': fields.Float,
    'lr_time': fields.datetime,
    'memo': fields.String,
    'detail': fields.Nested(stator_detail_fields)
}

motor_detail_fields = {
    'phase_number': fields.Integer,
    'pole_pairs_number': fields.Integer,
    'turn_number': fields.Integer,
    'rated_voltage': fields.Float,
    'rated_speed': fields.Float,
}

motor_fields = {
    'id': fields.Integer,
    'statu': fields.String,
    'name': fields.String,
    'sn': fields.String,
    'health_indicator': fields.Float,
    'lr_time': fields.datetime,
    'memo': fields.String,
    'detail': fields.Nested(motor_detail_fields),
    'rotors': fields.List(rotor_fields),
    'bearings': fields.List(bearing_fields),
    'stators': fields.List(stator_fields),
}


