from flask_restful import Resource
from base.basic_base import Session
from models.declarative_models import Stator
from serializer.asset_serializer import StatorSchema
from flasgger import swag_from
from flask_restful import reqparse
from fields.motor_fields import localtime
parser = reqparse.RequestParser()
parser.add_argument('lr_time', location='args', required=False, type=localtime)


class StatorDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        session = Session()
        stators = session.query(Stator).filter_by(motor_id=id).all()
        session.close()
        return StatorSchema().dump(stators, many=True)

    @swag_from('put.yaml')
    def patch(self, id):
        args = parser.parse_args()
        session = Session()
        session.query(Stator).filter(Stator.id == id).update({'lr_time': args['lr_time']})
        session.commit()
        session.close()

        return {'message': 'Success'}