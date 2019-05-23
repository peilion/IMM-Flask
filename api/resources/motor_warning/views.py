from flask_restful import reqparse, Resource
from sqlalchemy import func
from base.basic_base import Session
from models.declarative_models import WarningLog, Motor
from serializer.data_serializer import WarningSchema
from flasgger import swag_from
from flask_restful import inputs
from models import retrieve_model


warning_parser = reqparse.RequestParser()
warning_parser.add_argument('group_by', location='args', required=False,
                            type=str)  # use bool directly make this arg always true.
warning_parser.add_argument('limit', location='args', required=False, type=int)


class MotorWarningList(Resource):
    @swag_from('list.yaml')
    def get(self):
        args = warning_parser.parse_args()
        if args['group_by'] == 'motor':
            data = Session. \
                query(Motor.name, func.count(WarningLog.motor_id)). \
                join(Motor). \
                group_by(Motor.name).all()
            return data
        if args['group_by'] == 'date':
            data = retrieve_model.get_warning_calendar()
            return data
        else:
            data = Session. \
                query(Motor.name, WarningLog.cr_time, WarningLog.description, WarningLog.severity). \
                join(Motor). \
                order_by(WarningLog.cr_time.desc()). \
                slice(0, args['limit']).all()
            return WarningSchema().dump(data, many=True).data


class MotorWarning(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        data = Session.query(Motor.name, WarningLog.cr_time, WarningLog.description, WarningLog.severity). \
            join(Motor). \
            filter(WarningLog.motor_id == id).all()
        return WarningSchema().dump(data, many=True).data
