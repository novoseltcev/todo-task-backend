from flask import Blueprint, request, jsonify, redirect, send_from_directory
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from marshmallow import ValidationError

from server import Config
from server.jwt_auth import jwt_redis_blocklist, admin_required, owner_required
from server.errors.exc import InvalidSchema
from server.user import service as user_service
from server.user.serializer import serialize_user
from server.user.service import UserSchema
from server.role.service import RoleRepository


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
    user_role = RoleRepository.get_by_id(user.id_role)
    additional_claims = {'role': user_role.name}
    access_token = create_access_token(identity=user, additional_claims=additional_claims, fresh=True)
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
    jwt_redis_blocklist.set(jti, "", ex=Config.JWT_ACCESS_TOKEN_EXPIRES)
    return jsonify(msg="Access token revoked")


@user_blueprint.route(prefix + 'recovery')
def recovery():
    pass

#
# @user_blueprint.route(prefix + 'profile')
# @jwt_required()
# def profile():
#     user = get_jwt_identity()
#     account = user_service.get_profile(user)
#     return account


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


@user_blueprint.route('/admin/users/')
@admin_required()
def get_all():
    users = user_service.get_all()
    return serialize_user(users, many=True)


@user_blueprint.route('/admin' + prefix, methods=['POST'])
@owner_required()
def create():
    try:
        schema = UserSchema(only=('login', 'email', 'password')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    return user_service.create_account(**schema)


@user_blueprint.route('/admin' + prefix, methods=['PUT'])
@owner_required()
def update():
    try:
        schema = UserSchema().load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])
    user_service.UserRepository.update(schema)


@user_blueprint.route('/admin' + prefix, methods=['DELETE'])
@owner_required()
def delete():
    try:
        id = UserSchema(only=('id',)).load(request.json)['id']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    return user_service.delete_account(id)

