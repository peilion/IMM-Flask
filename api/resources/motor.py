from flask_restful import reqparse, Resource
from base.basic_base import Session
from models.declarative_models import Motor, Rotor, Stator, Bearing, User
from sqlalchemy.orm import joinedload
from serializer.asset_serializer import EquipGroupSchema, MotorSchema, RotorSchema, StatorSchema, BearingSchema, \
    MotorStatuStatisticSchema
# from base.automap_base import Base
from models import retrieve_model
from flasgger import swag_from

motor_parser = reqparse.RequestParser()
motor_parser.add_argument(
    'filter_by',
    location='args', required=False, type=str,
)


class EquipGroupDetail(Resource):
    @swag_from('docs/equip_group/get.yaml')
    def get(self, id):
        motor = Session.query(Motor). \
            options(joinedload(Motor.rotors),
                    joinedload(Motor.stators),
                    joinedload(Motor.bearings)). \
            filter_by(id=id). \
            one()
        return EquipGroupSchema().dump(motor)[0]


class EquipGroupList(Resource):
    @swag_from('docs/equip_group/list.yaml')
    def get(self):
        motors = Session.query(Motor). \
            options(joinedload(Motor.rotors),
                    joinedload(Motor.stators),
                    joinedload(Motor.bearings)). \
            all()
        return EquipGroupSchema().dump(motors, many=True)


class MotorDetail(Resource):
    @swag_from('docs/motor/get.yaml')
    def get(self, id):
        motor = Session.query(Motor).filter_by(id=id).one()
        return MotorSchema().dump(motor)


class MotorList(Resource):
    @swag_from('docs/motor/list.yaml')
    def get(self):
        args = motor_parser.parse_args()
        if args['filter_by'] == 'statu':
            data = retrieve_model.get_statu_statistic()
            return MotorStatuStatisticSchema().dump(data, many=False)
        else:
            motors = Session.query(Motor.name, Motor.sn, Motor.statu, Motor.lr_time, Motor.id, Motor.health_indicator,
                                   User.name.label('admin')). \
                join(User).all()
            return MotorSchema().dump(motors, many=True)


class RotorDetail(Resource):
    def get(self, id):
        """
        Rotor info
        ---
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the related motor,try 1~3
            type: string
         """
        rotors = Session.query(Rotor).filter_by(motor_id=id).all()
        return RotorSchema().dump(rotors, many=True)


class StatorDetail(Resource):
    def get(self, id):
        """
        Stator info
        ---
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the related motor,try 1~3
            type: string
         """
        stators = Session.query(Stator).filter_by(motor_id=id).all()
        return StatorSchema().dump(stators)


class BearingDetail(Resource):
    def get(self, id):
        """
        Bearing info
        ---
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the related motor,try 1~3
            type: string
        """
        bearings = Session.query(Bearing).filter_by(motor_id=id).all()
        return BearingSchema().dump(bearings, many=True)
