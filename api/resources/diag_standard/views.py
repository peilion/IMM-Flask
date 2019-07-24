from flask_restful import Resource
from flasgger import swag_from
from base.basic_base import Session
from models.declarative_models import RotorEvalStd,StatorEvalStd,BearingEvalStd,PowerEvalStd
from serializer import standard_serializer
from flask_restful import reqparse, inputs
import abc

parser = reqparse.RequestParser()
parser.add_argument('newest',location='args',required=False,type=inputs.boolean)
parser.add_argument('id',location='args',required=False,type=int)

@abc.abstractmethod
class BasicStandardDetail(Resource):
    model = None # should be specified.
    serializer = None # should be specified.

    @swag_from('get.yaml')
    def get(self):
        args = parser.parse_args()

        session = Session()
        data = session.query(self.model)
        if args['newest']:
            data = data.order_by(self.model.id.desc()).first()
        elif args['id']:
            data = data.filter_by(id = args['id']).one()
        else:
            return {'message':'invalid query'},400
        session.close()
        return self.serializer().dump(data)

class RotorStandardDetail(BasicStandardDetail):
    model = RotorEvalStd
    serializer = standard_serializer.RotorStandardSchema

class StatorStandardDetail(BasicStandardDetail):
    model = StatorEvalStd
    serializer = standard_serializer.StatorStandardSchema

class BearingStandardDetail(BasicStandardDetail):
    model = BearingEvalStd
    serializer = standard_serializer.BearingStandardSchema

class PowerStandardDetail(BasicStandardDetail):
    model = PowerEvalStd
    serializer = standard_serializer.PowerStandardSchema