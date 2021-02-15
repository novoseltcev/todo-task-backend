import os
from datetime import timedelta

from flask import Flask

from .category import category_blueprint
from .task import task_blueprint
from .file import file_blueprint


app = Flask(__name__)
app.template_folder = "static/templates"

app.config['SECRET_KEY'] = os.urandom(20).hex()
app.config['USE_PERMANENT_SESSION'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)

app.register_blueprint(task_blueprint, url_prefix="/task")
app.register_blueprint(category_blueprint, url_prefix="/category")
app.register_blueprint(file_blueprint, url_prefix="/file")
