from flask_restful import Resource, reqparse
from flasgger import swag_from
from base.basic_base import Session
from models.declarative_models import Motor, User
from serializer.asset_serializer import MotorSchema, MotorStatuStatisticSchema
from models import retrieve_model

motor_parser = reqparse.RequestParser()
motor_parser.add_argument(
    'filter_by',
    location='args', required=False, type=str,
)


class MotorDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        motor = Session.query(Motor).filter_by(id=id).one()
        return MotorSchema().dump(motor)


class MotorList(Resource):
    @swag_from('list.yaml')
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
