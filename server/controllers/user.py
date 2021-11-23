from flask import Blueprint, request, jsonify, redirect, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError

from server.errors.exc import InvalidSchema
from server.services.user import UserService, UserSchema, UserResponse

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


class UserController:
    @staticmethod
    @user_blueprint.route('/login', methods=['POST'])
    def login() -> Response:
        # try:
        schema = UserSchema(only=('mail', 'password')).load(request.json)
        user: UserResponse = UserService.login(schema)

        access_token = AuthSystem.get_access_token(identity=user['id'], role=user['role']['name'], refresh=True)
        refresh_token = AuthSystem.get_refresh_token(identity=user['id'])

        return jsonify(access_token=access_token, refresh_token=refresh_token)

        # additional_claims = {'role': user.role.name}
        # access_token = create_access_token(identity=user, additional_claims=additional_claims, fresh=True)
        # refresh_token = create_refresh_token(identity=user)
        # except ValidationError as e:
        #     raise InvalidSchema(e.args[0])

    @staticmethod
    @user_blueprint.route('/register', methods=['POST'])
    def register() -> Response:
        try:
            schema = UserSchema(only=('mail', 'password')).load(request.json)
            user: UserResponse = UserService.create(schema)
            # UserRepository.send_confirm(user)  TODO
            # html = email_service.html_confirm_registration(id=user.id, email=user.email)
            # email_service.send_message.delay(subject="Confirm Email", emails=[user.email], html=html)
            return redirect('/login')
        except ValidationError as e:
            raise InvalidSchema(e.args[0])

    @staticmethod
    @user_blueprint.route('/logout', methods=['POST'])
    @jwt_required()
    def logout() -> Response:
        jti = get_jwt()["jti"]
        AuthSystem.deactivate(jti=jti)
        # jwt_redis_blocklist.set(jti, "", ex=Config.JWT_ACCESS_TOKEN_EXPIRES)
        return jsonify(success=True)

    @staticmethod
    @user_blueprint.route('/recovery')
    def recovery() -> Response:
        pass

    @staticmethod
    @user_blueprint.route('/profile')
    def get_profile() -> Response:
        pass

    @staticmethod
    @user_blueprint.route('/profile', methods=['PUT'])
    @jwt_required(fresh=True)
    def change_profile() -> Response:
        user = get_jwt_identity()
        try:
            schema = UserSchema(only=('password', 'mail')).load(request.json)
            schema['id'] = user.id
            response: UserResponse = UserService.edit(schema)
            return jsonify(response)
        except ValidationError as e:
            raise InvalidSchema(e.args[0])


class TokenController:
    @staticmethod
    @user_blueprint.route('/refresh', methods=['GET', 'POST'])
    @jwt_required(refresh=True)
    def refresh() -> Response:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return jsonify(access_token=access_token)

    @staticmethod
    @user_blueprint.route('/confirm_email/<uuid:token>')
    def confirm_email(token):
        schema = UserSchema(only=('uuid', )).load({'uuid': token})
        UserService.confirm_email(schema)
        # id = mail_redis_tokenlist.get(token)
        # if id is None:
        #     raise ForbiddenOperation()
        # user_service.confirm_email(id)
        # mail_redis_tokenlist.delete(token)
        return redirect('/')


# @user_blueprint.route('/refresh', methods=['GET', 'POST'])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#     access_token = create_access_token(identity=identity, fresh=False)
#     return jsonify(access_token=access_token)
#
#
# @user_blueprint.route('/login', methods=['POST'])
# def login():
#     try:
#         schema = UserSchema(only=('mail', 'password')).load(request.json)
#     except ValidationError as e:
#         raise InvalidSchema(e.args[0])
#
#     user = user_service.login(schema)
#     additional_claims = {'role': user.role.name}
#     access_token = create_access_token(identity=user, additional_claims=additional_claims, fresh=True)
#     refresh_token = create_refresh_token(identity=user)
#     return jsonify(access_token=access_token, refresh_token=refresh_token)
#
#
# @user_blueprint.route('/register', methods=['POST'])
# def register():
#     try:
#         schema = UserSchema(only=('mail', 'password')).load(request.json)
#     except ValidationError as e:
#         raise InvalidSchema(e.args[0])
#
#     user = user_service.create_account(**schema)
#     html = email_service.html_confirm_registration(id=user.id, email=user.email)
#     email_service.send_message.delay(subject="Confirm Email", emails=[user.email], html=html)
#     return redirect('/login')
#
#
# @user_blueprint.route('/logout', methods=['POST'])
# @jwt_required()
# def logout():
#     jti = get_jwt()["jti"]
#     jwt_redis_blocklist.set(jti, "", ex=Config.JWT_ACCESS_TOKEN_EXPIRES)
#     return jsonify(msg="Access token revoked")
#
#
# @user_blueprint.route('/recovery')
# def recovery():
#     pass
#
#
# @user_blueprint.route('/profile', methods=['PUT'])
# @jwt_required(fresh=True)
# def change_profile():
#     user = get_jwt_identity()
#     try:
#         schema = UserSchema(only=('password', 'mail')).load(request.json)
#     except ValidationError as e:
#         raise InvalidSchema(e.args[0])
#     user = user_service.change_profile(user, schema)
#     return user


# @user_blueprint.route('/admin/users/')
# @admin_required(BaseConfig.admin_roles)
# def get_all():
#     users = user_service.get_all()
#     return serialize_user(users, many=True)
#
#
# @user_blueprint.route('/admin/user/', methods=['POST'])
# @admin_required(BaseConfig.owner_roles)
# def create():
#     try:
#         schema = UserSchema(only=('login', 'mail', 'password', 'role')).load(request.json)
#     except ValidationError as e:
#         raise InvalidSchema(e.args[0])
#     return user_service.create_account(**schema)
#
#
# @user_blueprint.route('/admin/user/', methods=['PUT'])
# @admin_required(BaseConfig.owner_roles)
# def update():
#     try:
#         schema = UserSchema().load(request.json)
#     except ValidationError as e:
#         raise InvalidSchema(e.args[0])
#     user_service.UserRepository.update(schema)
#
#
# @user_blueprint.route('/admin/user/', methods=['DELETE'])
# @admin_required(BaseConfig.owner_roles)
# def delete():
#     try:
#         id = UserSchema(only=('id',)).load(request.json)['id']
#     except ValidationError as e:
#         raise InvalidSchema(e.args[0])
#     return user_service.delete_account(id)
