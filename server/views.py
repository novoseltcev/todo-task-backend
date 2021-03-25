from os import path, getcwd

from flask import send_from_directory
from flask_jwt_extended import jwt_required

from server import app
from server import sqlalchemy_session


@app.route("/")
# @jwt_required()
def index():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), 'index.html')


@app.route('/login')
def login():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'),  path.join('auth', 'login.html'))
    # TODO-add login.html


@app.route('/register')
def register():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), path.join('auth', 'register.html'))
    # TODO-add register.html


@app.route('/recovery')
def recovery():
    return send_from_directory(path.join(getcwd(), 'server', 'static', 'templates'), path.join('auth', 'recovery.html'))
    # TODO-add recover.html


@app.teardown_appcontext
def shutdown_session(exception=None):
    sqlalchemy_session.remove()


def session_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            sqlalchemy_session.commit()
            return result
        except Exception as e:
            sqlalchemy_session.rollback()
            raise e

    return wrapper
