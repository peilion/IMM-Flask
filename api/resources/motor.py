from flask_restful import fields, marshal_with, reqparse, Resource
from migrations.base import Session
from models.declarative_models import Motor, Rotor, Stator, Bearing
from sqlalchemy.orm import joinedload
from serializer.asset_serializer import EquipGroupSchema, MotorSchema, RotorSchema, StatorSchema, BearingSchema, \
    MotorStatuStatisticSchema
from models import RetrieveModel

motor_parser = reqparse.RequestParser()
motor_parser.add_argument(
    'filter_by',
    location='args', required=False, type=str,
)


class EquipGroupDetail(Resource):

    def get(self, id):
        """
        Single Equipment group info
        ---
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the Equip gourp,try 1~3
            type: string
        responses:
          200:
            description: A brief description of the interested motor
         """
        motor = Session.query(Motor). \
            options(joinedload(Motor.rotors),
                    joinedload(Motor.stators),
                    joinedload(Motor.bearings)). \
            filter_by(id=id). \
            one()
        return EquipGroupSchema().dump(motor)[0]


class EquipGroupList(Resource):

    def get(self):
        """
        Equipment groups info List
        ---
        responses:
          200:
            description: A brief description of the interested equip group
         """
        motors = Session.query(Motor). \
            options(joinedload(Motor.rotors),
                    joinedload(Motor.stators),
                    joinedload(Motor.bearings)). \
            all()
        return EquipGroupSchema().dump(motors, many=True)


class MotorDetail(Resource):
    def get(self, id):
        """
        Single Equipment group info
        ---
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the motor,try 1~3
            type: string
         """
        motor = Session.query(Motor).filter_by(id=id).one()
        return MotorSchema().dump(motor)


class MotorList(Resource):
    def get(self):
        """
        Motor info list
        ---
        parameters:
          - in: query
            name: filter_by
            required: false
            description: field used for filter motor
            type: string
        """
        args = motor_parser.parse_args()
        if args['filter_by'] == 'statu':
            data = RetrieveModel.get_statu_statistic()
            return MotorStatuStatisticSchema().dump(data, many=False)
        else:
            motors = Session.query(Motor).all()
            return MotorSchema().dump(motors)


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


