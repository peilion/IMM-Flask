from flask_restful import Resource
from flasgger import swag_from
from base.basic_base import Session
from models.declarative_models import Motor
from sqlalchemy.orm import joinedload
from serializer.asset_serializer import EquipGroupSchema


class EquipGroupDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        motor = Session.query(Motor). \
            options(joinedload(Motor.rotors),
                    joinedload(Motor.stators),
                    joinedload(Motor.bearings)). \
            filter_by(id=id). \
            one()
        return EquipGroupSchema().dump(motor)[0]


class EquipGroupList(Resource):
    @swag_from('list.yaml')
    def get(self):
        motors = Session.query(Motor). \
            options(joinedload(Motor.rotors),
                    joinedload(Motor.stators),
                    joinedload(Motor.bearings)). \
            all()
        return EquipGroupSchema().dump(motors, many=True)
