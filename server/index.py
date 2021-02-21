from os import path, getcwd

from flask import session, send_from_directory

from . import app
from .initialize_db import DB_session


@app.route("/")
def index():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'new_index.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    DB_session.remove()


@app.before_request
def check_session():
    if 'current_category' not in session:
        session['current_category'] = 1
        session.modified = True
