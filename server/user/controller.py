from flask import Blueprint, request, jsonify, redirect
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from marshmallow import ValidationError

from server import mail_redis_tokenlist, Config
from server.jwt_auth import jwt_redis_blocklist, admin_required
from server.errors.exc import InvalidSchema, ForbiddenOperation
from server.user import service as user_service
from server.user.serializer import serialize_user
from server.user.service import UserSchema
from server.async_tasks import email


user_blueprint = Blueprint('user', __name__)
prefix = '/user/'


@user_blueprint.route(prefix + 'refresh', methods=['GET', 'POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()

    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


@user_blueprint.route('/login', methods=['POST'])
def login():
    try:
        schema = UserSchema(only=('email', 'password')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    user = user_service.login(schema)
    additional_claims = {'role': user.role.name}
    access_token = create_access_token(identity=user, additional_claims=additional_claims, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@user_blueprint.route('/register', methods=['POST'])
def register():
    try:
        schema = UserSchema(only=('email', 'password')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    user = user_service.create_account(**schema)
    email.confirm_registration.delay(serialize_user(user))
    return redirect('/login')


@user_blueprint.route(prefix + 'logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=Config.JWT_ACCESS_TOKEN_EXPIRES)
    return jsonify(msg="Access token revoked")


@user_blueprint.route('/recovery')
def recovery():
    pass

#
# @user_blueprint.route(prefix + 'profile')
# @jwt_required()
# def profile():
#     user = get_jwt_identity()
#     account = user_service.get_profile(user)
#     return account


@user_blueprint.route(prefix + 'confirm_email/<string:token>')
def confirm(token):
    id = mail_redis_tokenlist.get(token)
    if id is None:
        raise ForbiddenOperation()

    user_service.confirm_email(id)
    mail_redis_tokenlist.delete(token)
    return redirect('/')


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
@admin_required('owner', 'admin')
def get_all():
    users = user_service.get_all()
    return serialize_user(users, many=True)


@user_blueprint.route('/admin' + prefix, methods=['POST'])
@admin_required('owner')
def create():
    try:
        schema = UserSchema(only=('login', 'email', 'password', 'role')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    return user_service.create_account(**schema)


@user_blueprint.route('/admin' + prefix, methods=['PUT'])
@admin_required('owner')
def update():
    try:
        schema = UserSchema().load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])
    user_service.UserRepository.update(schema)


@user_blueprint.route('/admin' + prefix, methods=['DELETE'])
@admin_required('owner')
def delete():
    try:
        id = UserSchema(only=('id',)).load(request.json)['id']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    return user_service.delete_account(id)
