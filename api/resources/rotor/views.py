from flask_restful import Resource, inputs
from base.basic_base import Session
from models.declarative_models import Rotor
from serializer.asset_serializer import RotorSchema
from flasgger import swag_from
from flask_restful import reqparse
from utils.costume_input_fields import localtime

parser = reqparse.RequestParser()
parser.add_argument('lr_time', location='args', required=False, type=localtime)
parser.add_argument('info', location='args', required=False, type=inputs.boolean)


class RotorDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        args = parser.parse_args()
        if args['info']:
            session = Session()
            rotors = session.query(Rotor.inner_diameter, Rotor.length, Rotor.outer_diameter,
                                   Rotor.slot_number).filter_by(motor_id=id).all()
            return RotorSchema().dump(rotors, many=True)
        else:
            session = Session()
            rotors = Session.query(Rotor).filter_by(motor_id=id).all()
            session.close()
            return RotorSchema().dump(rotors, many=True)

    @swag_from('put.yaml')
    def patch(self, id):
        args = parser.parse_args()
        session = Session()
        session.query(Rotor).filter(Rotor.id == id).update({'lr_time': args['lr_time']})
        session.commit()
        session.close()

        return {'message': 'Success'}


class RotorInfo(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        session = Session()
        rotors = session.query(Rotor.inner_diameter, Rotor.length, Rotor.outer_diameter,
                               Rotor.slot_number).filter_by(id=id).one()
        session.close()
        return RotorSchema().dump(rotors)
