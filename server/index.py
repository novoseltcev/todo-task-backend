from os import path, getcwd

from flask import send_from_directory

from . import app
from . import DB_session


@app.route("/")
def index():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'index.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    DB_session.remove()

