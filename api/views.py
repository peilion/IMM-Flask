from flask import Blueprint
from flask_restful import Api
from api.resources import UserResource, EquipGroupList, EquipGroupDetail, MotorDetail, RotorDetail, StatorDetail, \
    BearingDetail, MotorList, MotorTrend,MotorWarning

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
api.add_resource(MotorTrend, '/motor/<int:id>/trend/')
api.add_resource(MotorWarning, '/motor/<int:id/warning>')