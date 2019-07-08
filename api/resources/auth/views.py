from flask_restful import Resource
from flasgger import swag_from
from extensions import cache

class UserResource(Resource):
    userMap = {
        'admin': {
            'roles': ['admin'],
            'token': 'admin',
            'introduction': 'This is superuser',
            'avatar': 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2720094078,3198972262&fm=26&gp=0.jpg',
            'name': 'Super admin'
        }
    }

    # @cache.cached(timeout=50, key_prefix='user_token')
    @swag_from('get.yaml')
    def get(self):
        return self.userMap['admin']

    @swag_from('get.yaml')
    def post(self):
        return self.userMap['admin']

class UserLogout(Resource):
    @swag_from('post.yaml')
    def post(self):
        return 'success',200