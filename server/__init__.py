import os
from datetime import timedelta

from flask import Flask
from flask_apispec import FlaskApiSpec

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec


app = Flask(__name__)
app.template_folder = os.path.join('static', 'templates')
app.config['SECRET_KEY'] = os.urandom(20).hex()
app.config['USE_PERMANENT_SESSION'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='server',
        version='v_1.3',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})
docs = FlaskApiSpec()


from . import errors_handler
from .index import index

from .category import *
from .task import *
from .file import *


app.register_blueprint(task_blueprint, url_prefix="/task")
app.register_blueprint(category_blueprint, url_prefix="/category")
app.register_blueprint(file_blueprint, url_prefix="/file")

docs.register(index)
docs.init_app(app)

__version__ = "0.1"
