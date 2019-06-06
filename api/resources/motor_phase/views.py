from flask_restful import reqparse, Resource, inputs
from flasgger import swag_from
from models import retrieve_model
from models.sharding_models import Feature, Uphase, Vphase, Wphase
from base.basic_base import Session
from serializer.data_serializer import PhaseSchema

phase_parser = reqparse.RequestParser()
phase_parser.add_argument('newest', location='args', required=False, type=inputs.boolean)
phase_parser.add_argument('pack_id', location='args', required=False, type=int)


class MotorUphaseSignal(Resource):
    model_factory = Uphase

    @swag_from('get.yaml')
    def get(self, id):
        phase = self.model_factory.model(motor_id=id)
        args = phase_parser.parse_args()
        if args['newest'] == True:
            session = Session()
            data = session.query(phase.wave).order_by(phase.id.desc()).first()
            session.close()
            return PhaseSchema(only=('wave',)).dump(data)
        elif args['pack_id']:
            session = Session()
            data = session.query(phase.wave).filter_by(pack_id=args['pack_id']).first()
            session.close()
            return PhaseSchema(only=('wave',)).dump(data)
        else:
            return 400


class MotorUphaseParas(Resource):
    model_factory = Uphase

    @swag_from('get.yaml')
    def get(self, id):
        phase = self.model_factory.model(motor_id=id)
        args = phase_parser.parse_args()
        if args['newest'] == True:
            session = Session()
            data = session. \
                query(phase.frequency, phase.amplitude, phase.initial_phase). \
                order_by(phase.id.desc()). \
                first()
            session.close()
            return PhaseSchema(only=('frequency', 'amplitude', 'initial_phase',)).dump(data)
        elif args['pack_id']:
            session = Session()
            data = session. \
                query(phase.frequency, phase.amplitude, phase.initial_phase). \
                filter_by(pack_id=args['pack_id']). \
                first()
            session.close()
            return PhaseSchema(only=('frequency', 'amplitude', 'initial_phase',)).dump(data)
        else:
            return 400


class MotorVphaseSignal(MotorUphaseSignal):
    model_factory = Vphase


class MotorVphaseParas(MotorUphaseParas):
    model_factory = Vphase


class MotorWphaseSignal(MotorUphaseSignal):
    model_factory = Wphase


class MotorWphaseParas(MotorUphaseParas):
    model_factory = Wphase


class MotorThreephaseSignal(Resource):

    @swag_from('get.yaml')
    def get(self, id):
        uphase = Uphase.model(motor_id=id)
        vphase = Vphase.model(motor_id=id)
        wphase = Wphase.model(motor_id=id)

        args = phase_parser.parse_args()

        session = Session()
        data = \
            session.query(uphase.wave.label('u'), vphase.wave.label('v'), wphase.wave.label('w')). \
                join(vphase, vphase.pack_id == uphase.pack_id). \
                join(wphase, wphase.pack_id == uphase.pack_id). \
                filter_by(pack_id=args['pack_id']).first()
        session.close()

        return PhaseSchema(only=('u', 'v', 'w')).dump(data)
