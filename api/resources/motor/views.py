from flask_restful import Resource, reqparse, inputs
from flasgger import swag_from
from base.basic_base import Session
from models.declarative_models import Motor, User
from serializer.asset_serializer import MotorSchema, MotorStatuStatisticSchema, MotorCompStatisticSchema
from models import retrieve_model
from utils.costume_input_fields import localtime

motor_parser = reqparse.RequestParser()
motor_parser.add_argument('group_by', location='args', required=False, type=str)
motor_parser.add_argument('comp_stat', location='args', required=False, type=inputs.boolean)
motor_parser.add_argument('lr_time', location='args', required=False, type=localtime)
motor_parser.add_argument('info', location='args', required=False, type=inputs.boolean)


class MotorDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        args = motor_parser.parse_args()
        if args['info']:
            session = Session()
            motor = session.query(Motor.phase_number, Motor.pole_pairs_number, Motor.turn_number,
                                  Motor.rated_voltage, Motor.rated_speed).filter_by(id=id).one()
            return MotorSchema().dump(motor)
        else:
            session = Session()
            motor = session.query(Motor.id, Motor.name, Motor.health_indicator, Motor.lr_time, Motor.sn, Motor.memo,
                                  Motor.statu).filter_by(id=id).one()
            session.close()
            return MotorSchema().dump(motor)

    @swag_from('put.yaml')
    def patch(self, id):
        args = motor_parser.parse_args()
        session = Session()
        session.query(Motor).filter(Motor.id == id).update({'lr_time': args['lr_time']})
        session.commit()
        session.close()
        return {'message': 'Success'}


class MotorList(Resource):
    @swag_from('list.yaml')
    def get(self):
        args = motor_parser.parse_args()
        if args['group_by'] == 'statu':
            data = retrieve_model.get_statu_statistic()
            return MotorStatuStatisticSchema().dump(data, many=False)
        elif args['group_by'] == 'comps':
            data = retrieve_model.get_comp_statistic()
            return MotorCompStatisticSchema().dump(data, many=True)
        else:
            session = Session()
            motors = session.query(Motor.name, Motor.sn, Motor.statu, Motor.lr_time, Motor.id, Motor.health_indicator,
                                   User.name.label('admin')). \
                join(User).all()
            session.close()
            return MotorSchema().dump(motors, many=True)
