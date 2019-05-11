from flask_restful import reqparse, Resource
from serializer.data_serializer import TrendSchema
from models import RetrieveModel
from flask import jsonify
from migrations.base import Session
from models.declarative_models import WarningLog
from sqlalchemy.orm import joinedload

trend_parser = reqparse.RequestParser()
trend_parser.add_argument(
    'timeafter',
    location='args', required=False, type=str,
)
trend_parser.add_argument(
    'timebefore',
    location='args', required=False, type=str,
)

trend_parser.add_argument(
    'feature',
    location='args', required=True, type=str,
    help='At least one feature indicator should be given, try one of [rms, max, min, thd, imbalance]'
)


class MotorTrend(Resource):
    def get(self, id):
        """
        Motor feature trend
        ---
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the related motor,try 1~3
            type: int
            default: 2
          - in: query
            name: feature
            required: true
            description: chose one or more of [rms, max_current, min_current, thd, imbalance,harmonics,fbrb,n_rms,p_rms,z_rms]
            type: array
            enum: ['rms', 'max_current', 'min_current', 'thd', 'imbalance','n_rms','p_rms','z_rms']

          - in: query
            name: timeafter
            required: true
            description: Start time, pattern:2016-01-01 00:00:00
            type: string
            formatter: date-time
            default: 2016-01-01 00:00:00
          - in: query
            name: timebefore
            required: true
            description: End time, pattern:2016-05-01 00:00:00
            type: string
            formatter: date-time
            """
        args = trend_parser.parse_args()
        result = RetrieveModel.get_motor_trend(id, args)
        dic = {}
        for row in result:
            for key, value in row.items():
                if key == 'time':
                    dic.setdefault(key, []).append(str(value))
                else:
                    dic.setdefault(key, []).append(value)

        return dic


warning_parser = reqparse.RequestParser()
warning_parser.add_argument(
    'isgroup',
    location='args', required=False, type=bool
)


class MotorWarning(RetrieveModel):
    def get(self, id):
        args = warning_parser.parse_args()

