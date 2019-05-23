from flask_restful import reqparse, Resource, inputs
from flasgger import swag_from
from models import retrieve_model
from models.sharding_models import Feature, Uphase
from base.basic_base import Session
from serializer.data_serializer import FeatureSchema

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
        if args['timeafter'] is not None or args['timebefore'] is not None:
            result = retrieve_model.get_motor_trend(id, args)
            dic = {}
            for row in result:
                for key, value in row.items():
                    if key == 'time':
                        dic.setdefault(key, []).append(str(value))
                    else:
                        dic.setdefault(key, []).append(value)
            return dic
        elif args['newest'] is True:
            feature = Feature.model(motor_id=id)
            uphase = Uphase.model(motor_id=id)
            data = Session. \
                query(feature.urms, feature.vrms, feature.wrms, feature.n_rms, feature.p_rms, uphase.frequency). \
                join(uphase, feature.pack_id == uphase.pack_id). \
                order_by(feature.id.desc()).first()
            return FeatureSchema().dump(data).data

        else:
            return {'Error message': 'Unproper query'}, 400
