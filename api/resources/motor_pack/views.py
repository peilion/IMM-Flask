from flask_restful import reqparse, Resource, inputs
from flasgger import swag_from

from models.sharding_models import CurrentsPack
from base.basic_base import Session
from serializer.data_serializer import PackSchema

pack_parser = reqparse.RequestParser()
pack_parser.add_argument('timeafter', location='args', required=False, type=str)
pack_parser.add_argument('timebefore', location='args', required=False, type=str)
pack_parser.add_argument('pack_id', location='args', required=False, type=int)
pack_parser.add_argument('newest', location='args', required=False, type=inputs.boolean)


class MotorPackList(Resource):
    @swag_from('list.yaml')
    def get(self, id):
        args = pack_parser.parse_args()
        pack = CurrentsPack.model(motor_id=id)
        data = Session. \
            query(pack.id, pack.time, pack.rpm).filter(pack.time.between(args['timeafter'], args['timebefore'])). \
            all()
        return PackSchema().dump(data, many=True).data


class MotorPackDetail(Resource):
    @swag_from('get.yaml')
    def get(self, id):
        args = pack_parser.parse_args()
        pack = CurrentsPack.model(motor_id=id)

        if args['newest']:
            data = Session.query(pack.id, pack.time, pack.rpm).order_by(pack.id.desc()).first()
            return PackSchema().dump(data).data
        elif args['pack_id']:
            data = Session.query(pack.id, pack.time, pack.rpm).filter_by(id=args['pack_id']).first()
            return PackSchema().dump(data).data
