from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required

from marshmallow import ValidationError

from server.errors.exc import InvalidSchema
from server.user import service as user_service
from server.user.service import UserSchema


user_blueprint = Blueprint('user', __name__)
prefix = '/user/'


@user_blueprint.route(prefix + 'login', methods=['POST'])
def login():
    try:
        schema = UserSchema(only=('login', 'password')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    token = user_service.login(schema)
    return jsonify(access_token=token)


@user_blueprint.route(prefix + 'register', methods=['POST'])
def register():
    try:
        schema = UserSchema(only=('login', 'email', 'password')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    token = user_service.create_account(**schema)
    return jsonify(access_token=token)
