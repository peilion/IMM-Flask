from flask_restful import Resource, inputs
from base.basic_base import Session
from models.declarative_models import Stator
from serializer.asset_serializer import StatorSchema
from flasgger import swag_from
from flask_restful import reqparse
from utils.costume_input_fields import localtime

parser = reqparse.RequestParser()
parser.add_argument('lr_time', location='args', required=False, type=localtime)
parser.add_argument('info', location='args', required=False, type=inputs.boolean)


class StatorDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        args = parser.parse_args()
        if args['info']:
            session = Session()
            stators = session.query(Stator.inner_diameter, Stator.length, Stator.outer_diameter,
                                    Stator.slot_number).filter_by(motor_id=id).all()
            return StatorSchema().dump(stators, many=True)
        else:
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


class StatorInfo(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        session = Session()
        stators = session.query(Stator.inner_diameter, Stator.length, Stator.outer_diameter,
                                Stator.slot_number).filter_by(id=id).one()
        session.close()
        return StatorSchema().dump(stators)
