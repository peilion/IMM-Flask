from flask_restful import reqparse, Resource, inputs
from flasgger import swag_from
from processing.signals import dq0_transform, threephase_deserialize, fftransform, cal_symm, make_phase
from models.sharding_models import ElectricalData, Feature
from models.declarative_models import Motor
from base.basic_base import Session
from serializer.data_serializer import PackSchema, PackHarmonicSchema, EnvelopeSchema, Array
import numpy as np
from serializer.data_serializer import Blob
from scipy import signal


pack_parser = reqparse.RequestParser()
pack_parser.add_argument('timeafter', location='args', required=False, type=str)
pack_parser.add_argument('timebefore', location='args', required=False, type=str)
pack_parser.add_argument('pack_id', location='args', required=False, type=int)
pack_parser.add_argument('newest', location='args', required=False, type=inputs.boolean)


class MotorPackList(Resource):
    @swag_from('list.yaml')
    def get(self, id):
        args = pack_parser.parse_args()
        elecdata = ElectricalData.model(motor_id=id)
        session = Session()
        data = session. \
            query(elecdata.id, elecdata.time, elecdata.rpm).filter(
            elecdata.time.between(args['timeafter'], args['timebefore'])). \
            all()
        session.close()
        return PackSchema(only=('id', 'time', 'rpm')).dump(data, many=True).data


class MotorPackDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        args = pack_parser.parse_args()
        elecdata = ElectricalData.model(motor_id=id)
        feature = Feature.model(motor_id=id)
        if args['newest']:
            session = Session()

            q = session. \
                query(elecdata.id, elecdata.time, elecdata.rpm, Motor.name, Motor.statu, Motor.sn,
                      elecdata.ucur.label('usignal'), elecdata.vcur.label('vsignal'), elecdata.wcur.label('wsignal'),
                      feature.uamplitude.label('uamp'), feature.vamplitude.label('vamp'),
                      feature.wamplitude.label('wamp'),
                      feature.ufrequency.label('ufreq'), feature.vfrequency.label('vfreq'),
                      feature.wfrequency.label('wfreq'),
                      feature.uinitial_phase.label('uip'), feature.vinitial_phase.label('vip'),
                      feature.winitial_phase.label('wip')). \
                join(Motor, Motor.id == elecdata.motor_id). \
                join(feature, feature.data_id == elecdata.id). \
                order_by(elecdata.id.desc()). \
                first()
            session.close()

            data = q._asdict()

            data['usignal'] = np.fromstring(data['usignal'], dtype=np.float32)
            data['vsignal'] = np.fromstring(data['vsignal'], dtype=np.float32)
            data['wsignal'] = np.fromstring(data['wsignal'], dtype=np.float32)
            data['ufft'] = fftransform(data['usignal'])[:1000]
            data['vfft'] = fftransform(data['vsignal'])[:1000]
            data['wfft'] = fftransform(data['wsignal'])[:1000]

            axis = np.linspace(0, data['usignal'].size, int(data['usignal'].size / 2), endpoint=False)
            data['usignal'] = np.take(data['usignal'], axis.astype(np.int))
            data['vsignal'] = np.take(data['vsignal'], axis.astype(np.int))
            data['wsignal'] = np.take(data['wsignal'], axis.astype(np.int))

            return PackSchema().dump(data)

        elif args['pack_id']:
            session = Session()

            data = session. \
                query(elecdata.id, elecdata.time, elecdata.rpm, Motor.name, Motor.statu, Motor.sn). \
                join(Motor, Motor.id == elecdata.motor_id). \
                filter(elecdata.id == args['pack_id']). \
                first()
            data = data._asdict()
            session.close()

            return PackSchema().dump(data)


class MotorPackSymAnalysis(Resource):

    @swag_from('als.yaml')
    def get(self, id, pack_id):
        feature = Feature.model(motor_id=id)

        session = Session()
        data = session. \
            query(feature.ufrequency.label('ufrequency'), feature.vfrequency.label('vfrequency'),
                  feature.wfrequency.label('wfrequency'),
                  feature.uamplitude.label('uamplitude'), feature.vamplitude.label('vamplitude'),
                  feature.wamplitude.label('wamplitude'),
                  feature.uinitial_phase.label('uinitial_phase'), feature.vinitial_phase.label('vinitial_phase'),
                  feature.winitial_phase.label('winitial_phase')). \
            filter_by(data_id=pack_id).one()
        session.close()
        complex_list = []
        for item in ['u', 'v', 'w']:
            complex_phase, _ = make_phase(getattr(data, item + 'amplitude'),
                                          2 * np.pi * getattr(data, item + 'frequency'),
                                          getattr(data, item + 'initial_phase'), samples=1024, end_time=1024 / 20480)
            # Append to the list
            complex_list.append(complex_phase)

        (phaseA_pos, phaseB_pos, phaseC_pos,
         phaseA_neg, phaseB_neg, phaseC_neg,
         phaseZero) = cal_symm(complex_list[1],
                               complex_list[0],
                               complex_list[2])
        return {key: Array.static_serialize(value) for key, value in
                {'pAp_real': phaseA_pos.real, 'pAp_imag': phaseA_pos.imag,
                 'pBp_real': phaseB_pos.real, 'pBp_imag': phaseB_pos.imag,
                 'pCp_real': phaseC_pos.real, 'pCp_imag': phaseC_pos.imag,
                 'pAn_real': phaseA_neg.real, 'pAn_imag': phaseA_neg.imag,
                 'pBn_real': phaseB_neg.real, 'pBn_imag': phaseB_neg.imag,
                 'pCn_real': phaseC_neg.real, 'pCn_imag': phaseC_neg.imag,
                 'zero_real': phaseZero.real, 'zero_imag': phaseZero.imag, }.items()
                }


class MotorPackDQAnalysis(Resource):

    @swag_from('als.yaml')
    def get(self, id, pack_id):
        elecdata = ElectricalData.model(motor_id=id)

        session = Session()
        data = session. \
            query(elecdata.ucur.label('u'), elecdata.vcur.label('v'), elecdata.wcur.label('w')). \
            filter_by(id=pack_id).one()
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
        elecdata = ElectricalData.model(motor_id=id)
        feature = Feature.model(motor_id=id)

        session = Session()

        data = session. \
            query(elecdata.ucur.label('u'), elecdata.vcur.label('v'), elecdata.wcur.label('w'),
                  feature.uharmonics, feature.uthd,
                  feature.vharmonics, feature.vthd,
                  feature.wharmonics, feature.wthd). \
            join(feature, feature.data_id == elecdata.id). \
            filter_by(id=pack_id).one()
        session.close()

        data = data._asdict()
        data['ufft'] = np.around(fftransform(np.fromstring(data['u'], dtype=np.float32)), decimals=3)
        data['vfft'] = np.around(fftransform(np.fromstring(data['v'], dtype=np.float32)), decimals=3)
        data['wfft'] = np.around(fftransform(np.fromstring(data['w'], dtype=np.float32)), decimals=3)

        return PackHarmonicSchema().dump(data)


class MotorPackEnvelope(Resource):

    @swag_from('als.yaml')
    def get(self, id, pack_id):
        elecdata = ElectricalData.model(motor_id=id)

        session = Session()
        data = session.query(elecdata.ucur.label('u'), elecdata.vcur.label('v'), elecdata.wcur.label('w')). \
            filter_by(id=pack_id).one()
        session.close()
        data = data._asdict()
        for key in ['u', 'v', 'w']:
            data[key] = np.fromstring(data[key], dtype=np.float32)
            data[key + 'envelope'] = np.abs(signal.hilbert(data[key])[1024:1024 + 4096])
            data[key + 'fft'] = fftransform(signal.detrend(data[key + 'envelope']))
            data[key] = data[key][1024:1024 + 4096]
        return EnvelopeSchema().dump(data)
