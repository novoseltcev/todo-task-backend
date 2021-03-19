from flask import Blueprint, request, jsonify, redirect, send_from_directory
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from marshmallow import ValidationError

from server import config
from server.jwt_auth import jwt_redis_blocklist
from server.errors.exc import InvalidSchema
from server.user import service as user_service
from server.user.service import UserSchema


user_blueprint = Blueprint('user', __name__)
prefix = '/user/'


@user_blueprint.route(prefix + 'refresh', methods=['GET', 'POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()

    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


@user_blueprint.route(prefix + 'login', methods=['POST'])
def login():
    try:
        schema = UserSchema(only=('login', 'password')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    user = user_service.login(schema)
    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@user_blueprint.route(prefix + 'register', methods=['POST'])
def register():
    try:
        schema = UserSchema(only=('login', 'email', 'password')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    user_service.create_account(**schema)
    return redirect('/login')


@user_blueprint.route(prefix + 'logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=config.JWT_ACCESS_TOKEN_EXPIRES)
    return jsonify(msg="Access token revoked")


@user_blueprint.route(prefix + 'recovery')
def recovery():
    pass


@user_blueprint.route(prefix + 'profile')
@jwt_required()
def profile():
    user = get_jwt_identity()
    account = user_service.get_profile(user)
    return account


@user_blueprint.route(prefix + 'profile', methods=['PUT'])
@jwt_required(fresh=True)
def change_profile():
    user = get_jwt_identity()
    try:
        schema = UserSchema(only=('password', 'email')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])
    user = user_service.change_profile(user, schema)
    return user
