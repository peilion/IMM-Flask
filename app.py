from flask import Flask
import api
from flasgger import Swagger, swag_from
from flask_cors import CORS
import os
from extensions import cache
import numpy as np
import scipy

app = Flask(__name__)
app.config.from_object('config')
CORS(app, supports_credentials=True)
swagger = Swagger(app, template_file=os.path.join(os.getcwd(), 'api', 'resources', 'template.yaml'))
app.register_blueprint(api.views.blueprint)
cache.init_app(app)

if __name__ == '__main__':

    app.run()
