from flask_restful import reqparse, Resource, inputs
from flasgger import swag_from
from models import retrieve_model
from models.sharding_models import Feature, ElectricalData
from base.basic_base import Session
from serializer.data_serializer import FeatureSchema
import time
from urllib import parse
from sqlalchemy.orm import load_only,joinedload
from models.declarative_models import Motor

trend_parser = reqparse.RequestParser()
trend_parser.add_argument('timeafter', location='args', required=False, type=str)
trend_parser.add_argument('timebefore', location='args', required=False, type=str)
trend_parser.add_argument('feature', location='args', required=False, type=str,
                          help='At least one feature indicator should be given, try one of [rms, max, min, thd, imbalance]'
                          )
trend_parser.add_argument('newest', location='args', required=False, type=inputs.boolean)


class MotorFeature(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        args = trend_parser.parse_args()
        columns = args['feature'].split(',')
        feature = Feature.model(motor_id=id)
        elecdata = ElectricalData.model(motor_id=id)
        session = Session()


        if args['timeafter'] is not None or args['timebefore'] is not None:
            data = session.query(feature, elecdata.time)
            for item in columns:
                data = data.options(load_only(item))  # query the given columns only
            data = data.join(elecdata,feature.data_id==elecdata.id)
            data = data.filter(elecdata.time>=args['timeafter'],elecdata.time<=args['timebefore']).all()
            session.close()
            dic = {}
            keys = data[0].keys()
            for row in data:
                for key in keys:
                    if key == 'time':
                        dic.setdefault(key, []).append(str(getattr(row,key)))
                    else:
                        for column in columns:
                            dic.setdefault(column, []).append(getattr(getattr(row,key),column))
            return dic

        elif args['newest'] is True:
            data = session.query(feature)
            for item in columns:
                data = data.options(load_only(item))
            data = data.order_by(feature.id.desc()).first() # query 1

            equip_info = session.query(Motor.name,Motor.sn, Motor.health_indicator).filter(Motor.id==id).one() # query 2

            session.close()

            result = {**data.__dict__,**equip_info._asdict()}

            return FeatureSchema().dump(result)

        else:
            return {'Error message': 'Unproper query'}, 400