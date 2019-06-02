from flask_restful import reqparse, Resource, inputs
from flasgger import swag_from
from processing.signals import dq0_transform, threephase_deserialize, fftransform
from models.sharding_models import CurrentsPack, Uphase, Vphase, Wphase, Feature
from models.declarative_models import Motor
from base.basic_base import Session
from serializer.data_serializer import PackSchema, FeatureSchema, EnvelopeSchema
import numpy as np
from serializer.data_serializer import Blob
from scipy import signal
from flask.json import jsonify
pack_parser = reqparse.RequestParser()
pack_parser.add_argument('timeafter', location='args', required=False, type=str)
pack_parser.add_argument('timebefore', location='args', required=False, type=str)
pack_parser.add_argument('pack_id', location='args', required=False, type=int)
pack_parser.add_argument('newest', location='args', required=False, type=inputs.boolean)


class MotorPackList(Resource):
    @swag_from('list.yaml')
    def get(self, id):
        args = pack_parser.parse_args()
        pack = CurrentsPack.model(motor_id=id)
        session = Session()
        data = session. \
            query(pack.id, pack.time, pack.rpm).filter(pack.time.between(args['timeafter'], args['timebefore'])). \
            all()
        session.close()
        return PackSchema(only=('id', 'time', 'rpm')).dump(data, many=True).data


class MotorPackDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        args = pack_parser.parse_args()
        pack = CurrentsPack.model(motor_id=id)
        uphase = Uphase.model(motor_id=id)
        vphase = Vphase.model(motor_id=id)
        wphase = Wphase.model(motor_id=id)

        if args['newest']:
            import time
            x = time.time()
            session = Session()
            data = session. \
                query(pack.id, pack.time, pack.rpm, Motor.name, Motor.statu, Motor.sn,
                      uphase.wave.label('usignal'), vphase.wave.label('vsignal'), wphase.wave.label('wsignal'),
                      uphase.amplitude.label('uamp'), vphase.amplitude.label('vamp'), wphase.amplitude.label('wamp'),
                      uphase.frequency.label('ufreq'), vphase.frequency.label('vfreq'), wphase.frequency.label('wfreq'),
                      uphase.initial_phase.label('uip'), vphase.initial_phase.label('vip'),
                      wphase.initial_phase.label('wip')). \
                join(Motor, Motor.id == pack.motor_id). \
                join(uphase, uphase.pack_id == pack.id). \
                join(vphase, vphase.pack_id == pack.id). \
                join(wphase, wphase.pack_id == pack.id). \
                order_by(pack.id.desc()). \
                first()
            session.close()
            data = data._asdict()
            data['usignal'] = np.fromstring(data['usignal'], dtype=np.float32)
            data['vsignal'] = np.fromstring(data['vsignal'], dtype=np.float32)
            data['wsignal'] = np.fromstring(data['wsignal'], dtype=np.float32)

            data['ufft'] = np.around(fftransform(data['usignal']), decimals=3)
            data['vfft'] = np.around(fftransform(data['vsignal']), decimals=3)
            data['wfft'] = np.around(fftransform(data['wsignal']), decimals=3)
            PackSchema().dump(data)
            x = time.time()-x
            return PackSchema().dump(data)

        elif args['pack_id']:
            session = Session()
            data = session.query(pack.id, pack.time, pack.rpm).filter_by(id=args['pack_id']).first()
            session.close()
            return PackSchema().dump(data).data


class MotorPackDQAnalysis(Resource):

    @swag_from('als.yaml')
    def get(self, id, pack_id):
        uphase = Uphase.model(motor_id=id)
        vphase = Vphase.model(motor_id=id)
        wphase = Wphase.model(motor_id=id)
        session = Session()
        data = session. \
            query(uphase.wave.label('u'), vphase.wave.label('v'), wphase.wave.label('w')). \
            join(vphase, vphase.pack_id == uphase.pack_id). \
            join(wphase, wphase.pack_id == uphase.pack_id). \
            filter_by(pack_id=pack_id).one()
        session.close()
        u, v, w = threephase_deserialize(data.u, data.v, data.w)

        d, q = dq0_transform(u, v, w)
        return {
            'd': Blob.myserialize(d),
            'q': Blob.myserialize(q),
            'd_rms': float(np.sqrt(np.dot(d, d) / d.size)),
            'q_rms': float(np.sqrt(np.dot(q, q) / d.size))
        }


class MotorPackHarmonic(Resource):

    @swag_from('als.yaml')
    def get(self, id, pack_id):
        uphase = Uphase.model(motor_id=id)
        vphase = Vphase.model(motor_id=id)
        wphase = Wphase.model(motor_id=id)

        feature = Feature.model(motor_id=id)
        session = Session()

        data = session. \
            query(uphase.wave.label('u'), vphase.wave.label('v'), wphase.wave.label('w'),
                  feature.uharmonics, feature.uthd,
                  feature.vharmonics, feature.vthd,
                  feature.wharmonics, feature.wthd). \
            join(vphase, vphase.pack_id == uphase.pack_id). \
            join(wphase, wphase.pack_id == uphase.pack_id). \
            join(feature, feature.pack_id == uphase.pack_id). \
            filter_by(pack_id=pack_id).one()
        session.close()

        data = data._asdict()
        data['ufft'] = np.around(fftransform(np.fromstring(data['u'], dtype=np.float32)), decimals=3)
        data['vfft'] = np.around(fftransform(np.fromstring(data['v'], dtype=np.float32)), decimals=3)
        data['wfft'] = np.around(fftransform(np.fromstring(data['w'], dtype=np.float32)), decimals=3)

        return FeatureSchema().dump(data)


class MotorPackEnvelope(Resource):

    @swag_from('als.yaml')
    def get(self, id, pack_id):
        uphase = Uphase.model(motor_id=id)
        vphase = Vphase.model(motor_id=id)
        wphase = Wphase.model(motor_id=id)
        session = Session()
        data = session.query(uphase.wave.label('u'), vphase.wave.label('v'), wphase.wave.label('w')). \
            join(vphase, vphase.pack_id == uphase.pack_id). \
            join(wphase, wphase.pack_id == uphase.pack_id). \
            filter_by(pack_id=pack_id).one()
        session.close()
        data = data._asdict()
        for key in ['u', 'v', 'w']:
            data[key] = np.fromstring(data[key], dtype=np.float32)
            data[key + 'envelope'] = np.abs(signal.hilbert(data[key])[1024:1024 + 4096])
            data[key + 'fft'] = np.around(fftransform(signal.detrend(data[key + 'envelope'])), decimals=3)
            data[key] = data[key][1024:1024 + 4096]
        return EnvelopeSchema().dump(data)
