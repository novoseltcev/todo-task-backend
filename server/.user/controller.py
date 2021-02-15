from flask import Blueprint, request
from flask_login import LoginManager

from . import service as svc

manager = LoginManager()
user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/sign-in')
def sign_in():
    json = request.json
    # login = json['login']
    # password = json['password']
    # svc.login(login, password)
    return 'ЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ'


@user_blueprint.route('/sign-out')
def sign_out():
    pass
    # svc.logout()


@user_blueprint.route('/register')
def register():
    pass


@user_blueprint.route('/profile')
def profile():
    pass
