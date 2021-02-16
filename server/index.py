from flask import session
from .app import app
from .initialize_db import DB_session
from .task.service import rerender_page


@app.route("/")
def get_page():
    return rerender_page()


@app.teardown_appcontext
def shutdown_session(exception=None):
    DB_session.remove()


@app.before_request
def check_session():
    if 'current_category' not in session:
        session['current_category'] = 1
