from flask_restful import Resource


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

    def get(self):
        """
        User token api
        ---
        responses:
          200:
            description: A token contains user roles,avatar,name and introduction etc. Since the api hasn't been finished, it returns same data for all requests
         """
        return self.userMap['admin']

    def post(self):
        return self.userMap['admin']
