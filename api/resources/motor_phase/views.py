from flask_restful import reqparse, Resource, inputs
from flasgger import swag_from
from models import retrieve_model
from models.sharding_models import Feature, ElectricalData
from base.basic_base import Session
from serializer.data_serializer import PhaseSchema

phase_parser = reqparse.RequestParser()
phase_parser.add_argument('newest', location='args', required=False, type=inputs.boolean)
phase_parser.add_argument('pack_id', location='args', required=False, type=int)


class MotorUphaseSignal(Resource):
    phase = 'u'

    @swag_from('get.yaml')
    def get(self, id):
        elecdata = ElectricalData.model(motor_id=id)
        args = phase_parser.parse_args()
        if args['newest'] == True:
            session = Session()
            data = session.query(getattr(elecdata, self.phase + 'cur').label('wave')).order_by(
                elecdata.id.desc()).first()
            session.close()
            return PhaseSchema(only=('wave',)).dump(data)
        elif args['pack_id']:
            session = Session()
            data = session.query(getattr(elecdata, self.phase + 'cur').label('wave')).filter_by(
                id=args['pack_id']).first()
            session.close()
            return PhaseSchema(only=('wave',)).dump(data)
        else:
            return 400


class MotorUphaseParas(Resource):
    phase = 'u'

    @swag_from('get.yaml')
    def get(self, id):
        feature = Feature.model(motor_id=id)
        args = phase_parser.parse_args()
        if args['newest'] == True:
            session = Session()
            data = session. \
                query(getattr(feature, self.phase + 'frequency').label('frequency'),
                      getattr(feature, self.phase + 'amplitude').label('amplitude'),
                      getattr(feature, self.phase + 'initial_phase').label('initial_phase')). \
                order_by(feature.id.desc()). \
                first()
            session.close()
            return PhaseSchema(only=('frequency', 'amplitude', 'initial_phase',)).dump(data)
        elif args['pack_id']:
            session = Session()
            data = session. \
                query(getattr(feature, self.phase + 'frequency').label('frequency'),
                      getattr(feature, self.phase + 'amplitude').label('amplitude'),
                      getattr(feature, self.phase + 'initial_phase').label('initial_phase')). \
                filter_by(data_id=args['pack_id']). \
                first()
            session.close()
            return PhaseSchema(only=('frequency', 'amplitude', 'initial_phase',)).dump(data)
        else:
            return 400


class MotorVphaseSignal(MotorUphaseSignal):
    phase = 'v'


class MotorVphaseParas(MotorUphaseParas):
    phase = 'v'


class MotorWphaseSignal(MotorUphaseSignal):
    phase = 'w'


class MotorWphaseParas(MotorUphaseParas):
    phase = 'w'


class MotorThreephaseSignal(Resource):

    @swag_from('get.yaml')
    def get(self, id):
        elecdata = ElectricalData.model(motor_id=id)
        args = phase_parser.parse_args()

        session = Session()
        data = \
            session.query(elecdata.ucur.label('u'), elecdata.vcur.label('v'), elecdata.wcur.label('w')). \
                filter_by(id=args['pack_id']).one()
        session.close()

        return PhaseSchema(only=('u', 'v', 'w')).dump(data)
