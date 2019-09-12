from flask_restful import reqparse, Resource, inputs
from flasgger import swag_from
from models import retrieve_model
from models.sharding_models import Feature, ElectricalData
from base.basic_base import Session
from serializer.data_serializer import FeatureSchema
import time
from urllib import parse
from sqlalchemy.orm import load_only, joinedload
from models.declarative_models import Motor

trend_parser = reqparse.RequestParser()
trend_parser.add_argument('timeafter', location='args', required=False, type=str)
trend_parser.add_argument('timebefore', location='args', required=False, type=str)
trend_parser.add_argument('feature', location='args', required=False, type=str,
                          help='At least one feature indicator should be given, try one of [rms, max, min, thd, imbalance]'
                          )
trend_parser.add_argument('newest', location='args', required=False, type=inputs.boolean)


class MotorFeature(Resource):

    def query_with_daterange(self):
        session = Session()
        data = session.query(self.feature, self.elecdata.time)
        for item in self.columns:
            data = data.options(load_only(item))  # query the given columns only
        data = data.join(self.elecdata, self.feature.data_id == self.elecdata.id)
        data = data.filter(self.elecdata.time >= self.args['timeafter'],
                           self.elecdata.time <= self.args['timebefore']).all()
        session.close()
        dic = {}
        keys = data[0].keys()
        for row in data:
            for key in keys:
                if key == 'time':
                    dic.setdefault(key, []).append(str(getattr(row, key)))
                else:
                    for column in self.columns:
                        dic.setdefault(column, []).append(getattr(getattr(row, key), column))
        return dic

    def query_last(self):
        session = Session()
        data = session.query(self.feature)
        for item in self.columns:
            data = data.options(load_only(item))
        data = data.order_by(self.feature.id.desc()).first()  # query 1
        equip_info = session.query(Motor.name, Motor.sn, Motor.health_indicator).filter(
            Motor.id == self.id).one()  # query 2
        session.close()
        result = {**data.__dict__, **equip_info._asdict()}

        return FeatureSchema().dump(result)

    @swag_from('get.yaml')
    def get(self, id):
        self.id = id
        self.args = trend_parser.parse_args()
        self.columns = self.args['feature'].split(',')
        self.feature = Feature.model(motor_id=id)
        self.elecdata = ElectricalData.model(motor_id=id)

        meth_name = 'query_with_daterange' if (
                self.args['timeafter'] is not None or self.args['timebefore'] is not None) else 'query_last'
        meth = getattr(self, meth_name, None)
        return meth()
