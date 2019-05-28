from flask_restful import Resource
from flasgger import swag_from
from base.basic_base import Session
from models.declarative_models import Motor, Bearing, Rotor, Stator
from sqlalchemy.orm import joinedload
from serializer.asset_serializer import EquipGroupSchema
from flask_restful import reqparse, inputs

equipgroup_parser = reqparse.RequestParser()
equipgroup_parser.add_argument('iftree', location='args', required=False,
                               type=inputs.boolean)  # use bool directly make this arg always true.


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
        args = equipgroup_parser.parse_args()
        if args['iftree']:
            treejson = {'name': 'Induction Motor Monitoring Platform', 'children': []}
            for motor in Session.query(Motor.id, Motor.name).all():
                treejson['children'].append({'name': motor.name,
                                             'children': []})
                for bearing in Session.query(Bearing.name).filter_by(motor_id=motor.id).all():
                    treejson['children'][-1]['children'].append({'name': bearing.name})
                for rotor in Session.query(Rotor.name).filter_by(motor_id=motor.id).all():
                    treejson['children'][-1]['children'].append({'name': rotor.name})
                for stator in Session.query(Stator.name).filter_by(motor_id=motor.id).all():
                    treejson['children'][-1]['children'].append({'name': stator.name})
            return treejson, 200
        else:
            motors = Session. \
                query(Motor). \
                options(joinedload(Motor.rotors),
                        joinedload(Motor.stators),
                        joinedload(Motor.bearings)). \
                all()
            return EquipGroupSchema().dump(motors, many=True)
