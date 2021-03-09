from flask import Blueprint, request, jsonify, redirect, url_for

from marshmallow import ValidationError

from server.errors.exc import InvalidSchema
from server.user import service as user_service
from server.user.service import UserSchema


user_blueprint = Blueprint('user', __name__)
prefix = '/user/'


@user_blueprint.route(prefix, methods=['POST'])
def login():
    try:
        schema = UserSchema().load(request.json)
    except ValidationError:
        raise InvalidSchema()

    password = schema['password']
    auth_method = UserSchema.get_auth_method(schema)

    if user_service.login(password=password, auth_method=auth_method):
        return redirect(url_for('index'))

    return jsonify(), 400


@user_blueprint.route(prefix, methods=['DELETE'])
def sign_out():
    try:
        schema = UserSchema(only=('id',)).load(request.json)
    except ValidationError:
        raise InvalidSchema()

    id = schema['id']
    user = user_service.get_profile(id=id)
    sign_out(user)
    return redirect(url_for('login'))


@user_blueprint.route(prefix + 'register', methods=['POST'])
def register():
    try:
        schema = UserSchema().load(request.json)
    except ValidationError:
        raise InvalidSchema()

    user = user_service.create_account(**schema)
    if user is None:
        return jsonify(), 400
    # login_user(user[0])
    return redirect(url_for('index'))
