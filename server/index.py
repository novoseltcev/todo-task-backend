from flask import session
from . import app
from .local import response
from .initialize_db import DB_session
from .category.service import get_categories


@app.route("/")
def index():
    return response(**get_categories(), code=200)


@app.teardown_appcontext
def shutdown_session(exception=None):
    DB_session.remove()


@app.before_request
def check_session():
    if 'current_category' not in session:
        session['current_category'] = 1
        session.modified = True
