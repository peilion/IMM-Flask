from flask import Blueprint
from flask_restful import Api

from api.resources import UserResource


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(UserResource, '/users/<int:user_id>')
