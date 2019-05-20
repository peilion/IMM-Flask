from flask_restful import Resource
from base.basic_base import Session
from models.declarative_models import Bearing
from serializer.asset_serializer import BearingSchema
from flasgger import swag_from


class BearingDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        bearings = Session.query(Bearing).filter_by(motor_id=id).all()
        return BearingSchema().dump(bearings, many=True)
