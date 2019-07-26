from flask_restful import Resource, inputs
from base.basic_base import Session
from models.declarative_models import Bearing
from serializer.asset_serializer import BearingSchema
from flasgger import swag_from
from flask_restful import reqparse
from utils.costume_input_fields import localtime

parser = reqparse.RequestParser()
parser.add_argument('lr_time', location='args', required=False, type=localtime)
parser.add_argument('info', location='args', required=False, type=inputs.boolean)


class BearingDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        args = parser.parse_args()
        if args['info']:
            session = Session()
            bearings = session.query(Bearing.inner_race_diameter, Bearing.inner_race_width,
                                     Bearing.outter_race_diameter,
                                     Bearing.outter_race_width, Bearing.roller_diameter, Bearing.roller_number,
                                     Bearing.contact_angle).filter_by(motor_id=id).all()
            return BearingSchema().dump(bearings, many=True)
        else:
            session = Session()
            bearings = session.query(Bearing).filter_by(motor_id=id).all()
            session.close()

            return BearingSchema().dump(bearings, many=True)

    @swag_from('put.yaml')
    def patch(self, id):
        args = parser.parse_args()
        session = Session()
        session.query(Bearing).filter(Bearing.id == id).update({'lr_time': args['lr_time']})
        Session.commit()
        session.close()

        return {'message': 'Success'}


class BearingInfo(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        session = Session()
        bearings = session.query(Bearing.inner_race_diameter, Bearing.inner_race_width,
                                 Bearing.outter_race_diameter,
                                 Bearing.outter_race_width, Bearing.roller_diameter, Bearing.roller_number,
                                 Bearing.contact_angle).filter_by(id=id).one()
        return BearingSchema().dump(bearings)
