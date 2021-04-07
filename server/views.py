import os

from flask import send_from_directory, Blueprint
from flask_jwt_extended import jwt_required

from server import sqlalchemy_session

view_blueprint = Blueprint('views', __name__)

template_folder = os.path.join(os.getcwd(), 'server', 'static', 'templates')


@view_blueprint.route("/")
# @jwt_required()
def index():
    return send_from_directory(template_folder, 'index.html')


@view_blueprint.route('/login')
def login():
    return send_from_directory(template_folder, os.path.join('auth', 'login.html'))


@view_blueprint.route('/register')
def register():
    return send_from_directory(template_folder, os.path.join('auth', 'register.html'))  # TODO-add register.html


@view_blueprint.route('/recovery')
def recovery():
    return send_from_directory(template_folder, os.path.join('auth', 'recovery.html'))  # TODO-add recover.html


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
