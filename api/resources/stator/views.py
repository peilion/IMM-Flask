from flask_restful import Resource
from base.basic_base import Session
from models.declarative_models import Stator
from serializer.asset_serializer import StatorSchema
from flasgger import swag_from


class StatorDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        stators = Session.query(Stator).filter_by(motor_id=id).all()
        return StatorSchema().dump(stators, many=True)
