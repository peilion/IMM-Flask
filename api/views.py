from flask import Blueprint, jsonify
from flask_restful import Api

from api.resources import UserResource, EquipGroupList, EquipGroupDetail, MotorDetail, RotorDetail, StatorDetail, \
    BearingDetail, MotorList, MotorFeature, MotorWarningList, MotorWarning, ServerStatu, MotorWphaseSignal, \
    MotorWphaseParas, MotorVphaseSignal, MotorVphaseParas, MotorUphaseSignal, MotorUphaseParas, MotorPackList, \
    MotorPackDetail, MotorPackDQAnalysis, MotorPackHarmonic, MotorPackEnvelope, BearingInfo, RotorInfo, StatorInfo, \
    MotorPackSymAnalysis,MotorThreephaseSignal

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(UserResource, '/login/', '/user/info/')
api.add_resource(EquipGroupDetail, '/equipgroup/<string:id>/')
api.add_resource(EquipGroupList, '/equipgroup/')
api.add_resource(MotorDetail, '/motor/<string:id>/')

api.add_resource(RotorDetail, '/motor/<string:id>/rotor/')
api.add_resource(RotorInfo, '/rotor/<string:id>/')

api.add_resource(StatorDetail, '/motor/<string:id>/stator/')
api.add_resource(StatorInfo, '/stator/<string:id>/')

api.add_resource(BearingDetail, '/motor/<string:id>/bearing/')
api.add_resource(BearingInfo, '/bearing/<string:id>/')

api.add_resource(MotorList, '/motor/')
api.add_resource(MotorFeature, '/motor/<int:id>/feature/')
api.add_resource(MotorWarningList, '/motor/warning/')
api.add_resource(MotorWarning, '/motor/<int:id>/warning/')
api.add_resource(ServerStatu, '/server/statu/')

api.add_resource(MotorWphaseSignal, '/motor/<int:id>/wsignal/')
api.add_resource(MotorWphaseParas, '/motor/<int:id>/wpara/')
api.add_resource(MotorVphaseSignal, '/motor/<int:id>/vsignal/')
api.add_resource(MotorVphaseParas, '/motor/<int:id>/vpara/')
api.add_resource(MotorUphaseSignal, '/motor/<int:id>/usignal/')
api.add_resource(MotorUphaseParas, '/motor/<int:id>/upara/')
api.add_resource(MotorThreephaseSignal, '/motor/<int:id>/tsignal/')

api.add_resource(MotorPackList, '/motor/<int:id>/packs/')
api.add_resource(MotorPackDetail, '/motor/<int:id>/pack/')

api.add_resource(MotorPackDQAnalysis, '/motor/<int:id>/pack/<int:pack_id>/dq/')
api.add_resource(MotorPackHarmonic, '/motor/<int:id>/pack/<int:pack_id>/harmonics/')
api.add_resource(MotorPackEnvelope, '/motor/<int:id>/pack/<int:pack_id>/envelope/')
api.add_resource(MotorPackSymAnalysis, '/motor/<int:id>/pack/<int:pack_id>/sym/')
# @blueprint.route('/motor/<int:id>/pack/')
# from flask.json import jsonify
# from processing.signals import dq0_transform, threephase_deserialize, fftransform
# from models.sharding_models import CurrentsPack, Uphase, Vphase, Wphase, Feature
# from models.declarative_models import Motor
# from base.basic_base import Session
# from serializer.data_serializer import PackSchema, FeatureSchema, EnvelopeSchema
# import numpy as np
# import json
# def hello_world(id):
#     pack = CurrentsPack.model(motor_id=id)
#     uphase = Uphase.model(motor_id=id)
#     vphase = Vphase.model(motor_id=id)
#     wphase = Wphase.model(motor_id=id)
#     import time
#     x = time.time()
#     session = Session()
#     data = session. \
#         query(pack.id, pack.time, pack.rpm, Motor.name, Motor.statu, Motor.sn,
#               uphase.wave.label('usignal'), vphase.wave.label('vsignal'), wphase.wave.label('wsignal'),
#               uphase.amplitude.label('uamp'), vphase.amplitude.label('vamp'), wphase.amplitude.label('wamp'),
#               uphase.frequency.label('ufreq'), vphase.frequency.label('vfreq'), wphase.frequency.label('wfreq'),
#               uphase.initial_phase.label('uip'), vphase.initial_phase.label('vip'),
#               wphase.initial_phase.label('wip')). \
#         join(Motor, Motor.id == pack.motor_id). \
#         join(uphase, uphase.pack_id == pack.id). \
#         join(vphase, vphase.pack_id == pack.id). \
#         join(wphase, wphase.pack_id == pack.id). \
#         order_by(pack.id.desc()). \
#         first()
#     session.close()
#     data = data._asdict()
#     data['usignal'] = np.fromstring(data['usignal'], dtype=np.float32)
#     data['vsignal'] = np.fromstring(data['vsignal'], dtype=np.float32)
#     data['wsignal'] = np.fromstring(data['wsignal'], dtype=np.float32)
#
#     data['ufft'] = np.around(fftransform(data['usignal']), decimals=3)
#     data['vfft'] = np.around(fftransform(data['vsignal']), decimals=3)
#     data['wfft'] = np.around(fftransform(data['wsignal']), decimals=3)
#     PackSchema().dump(data)
#     x = time.time() - x
#     return json.dumps(PackSchema().dump(data).data)
