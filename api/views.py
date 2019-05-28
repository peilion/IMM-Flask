from flask import Blueprint
from flask_restful import Api
from api.resources import UserResource, EquipGroupList, EquipGroupDetail, MotorDetail, RotorDetail, StatorDetail, \
    BearingDetail, MotorList, MotorFeature, MotorWarningList, MotorWarning, ServerStatu, MotorWphaseSignal, \
    MotorWphaseParas, MotorVphaseSignal, MotorVphaseParas, MotorUphaseSignal, MotorUphaseParas, MotorPackList, \
    MotorPackDetail, MotorPackDQAnalysis, MotorPackHarmonic

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(UserResource, '/login/', '/user/info/')
api.add_resource(EquipGroupDetail, '/equipgroup/<string:id>/')
api.add_resource(EquipGroupList, '/equipgroup/')
api.add_resource(MotorDetail, '/motor/<string:id>/')
api.add_resource(RotorDetail, '/motor/<string:id>/rotor/')
api.add_resource(StatorDetail, '/motor/<string:id>/stator/')
api.add_resource(BearingDetail, '/motor/<string:id>/bearing/')
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

api.add_resource(MotorPackList, '/motor/<int:id>/packs/')
api.add_resource(MotorPackDetail, '/motor/<int:id>/pack/')

api.add_resource(MotorPackDQAnalysis, '/motor/<int:id>/pack/<int:pack_id>/dq/')
api.add_resource(MotorPackHarmonic, '/motor/<int:id>/pack/<int:pack_id>/harmonics/')

# @blueprint.route('/register')
# def hello_world():
#     treejson = {'name': 'Induction Motor Monitoring Platform', 'children': []}
#     for motor in Session.query(Motor.id, Motor.name).all():
#         treejson['children'].append({'name': motor.name,
#                                      'children': []})
#         for bearing in Session.query(Bearing.name).filter_by(motor_id=motor.id).all():
#             treejson['children'][-1]['children'].append({'name': bearing.name})
#         for rotor in Session.query(Rotor.name).filter_by(motor_id=motor.id).all():
#             treejson['children'][-1]['children'].append({'name': rotor.name})
#         for stator in Session.query(Stator.name).filter_by(motor_id=motor.id).all():
#             treejson['children'][-1]['children'].append({'name': stator.name})
#     return jsonify(treejson)