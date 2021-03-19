from os import path, getcwd

from flask import send_from_directory
from flask_jwt_extended import jwt_required

from server import app
from server import DB_session


@app.route("/")
@jwt_required()
def index():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'index.html')


@app.route('/login')
def login():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'login.html')
    # TODO-add login.html


@app.route('/register')
def register():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'register.html')
    # TODO-add register.html


@app.route('/recovery')
def recovery():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'recovery.html')
    # TODO-add recover.html


@app.teardown_appcontext
def shutdown_session(exception=None):
    DB_session.remove()


def session_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            DB_session.commit()
            return result
        except Exception as e:
            DB_session.rollback()
            raise e

    return wrapper
