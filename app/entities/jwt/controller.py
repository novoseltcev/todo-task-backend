from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, JWTManager

from app.rest_lib.controller import Controller
from app.utils.schemas import AuthSchema

from .service import JWTService, Tokens
from .schema import JWTSchema
from app.models import User

jwt = JWTManager(current_app)


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    return JWTService().check_revoke(jti=jwt_payload["jti"])


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    JWTService().delete_expired_token(jti=jwt_payload['jti'])
    return jsonify(msg='Token has been expired')


class JWTController(Controller):
    service: JWTService

    def __init__(self):
        super().__init__(service=JWTService())

    def post(self):
        auth_data = AuthSchema().load(self.json)
        tokens: Tokens = self.service.create_tokens(auth_data)
        print(tokens)
        return jsonify(
            data=JWTSchema().dump(tokens)
        ), 201

    @jwt_required(refresh=True)
    def put(self):
        self.auth_service.load_user(get_jwt_identity())
        tokens: Tokens = self.service.refresh_access_token(user=self.user, refresh_jti=get_jwt()['jti'])
        return jsonify(
            data=JWTSchema(only=('access_token',)).dump(tokens)
        ), 201

    @jwt_required(verify_type=False)
    def delete(self):
        self.service.revoke_token(get_jwt()['jti'])
        return jsonify(), 204
