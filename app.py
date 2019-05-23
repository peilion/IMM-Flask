from flask import Flask
import api
from flasgger import Swagger, swag_from
from flask_cors import CORS
import os


def create_app():
    """Application factory, used to create application
    """
    app = Flask(__name__)
    app.config.from_object('config')
    swagger = Swagger(app, template_file=os.path.join(os.getcwd(), 'api', 'resources', 'template.yaml'))
    register_blueprints(app)
    CORS(app, supports_credentials=True)

    return app


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.blueprint)


if __name__ == '__main__':
    app = create_app()
    app.run()
