from flask_restful import Resource
from base.basic_base import Session
from models.declarative_models import Rotor
from serializer.asset_serializer import RotorSchema
from flasgger import swag_from


class RotorDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        rotors = Session.query(Rotor).filter_by(motor_id=id).all()
        return RotorSchema().dump(rotors, many=True)
