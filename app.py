from flask import Flask
import api


def create_app():
    """Application factory, used to create application
    """
    app = Flask(__name__)
    app.config.from_object('config.py')
    register_blueprints(app)

    return app


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.blueprint)


if __name__ == '__main__':
    app = create_app()
    app.run()
