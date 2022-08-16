from datetime import timedelta, datetime as dt
from typing import NamedTuple

from flask import jsonify, current_app
from flask_jwt_extended import create_refresh_token, create_access_token, current_user, get_jwt, JWTManager


from app.config import config
from app.models import User
from app.rest_lib.services import Service
from app.entities.user.service import UserService

from .repository import JWTRepository, JWTToken

jwt = JWTManager(current_app)


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    return JWTService().check_revoke(token=jwt_payload["jti"])


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    JWTService().delete_expired_token(token=jwt_payload['jti'])
    return jsonify(msg='Token has been expired')


class Tokens(NamedTuple):
    access_token: JWTToken
    refresh_token: JWTToken = None


class JWTService(Service):
    repository: JWTRepository

    def __init__(
            self,
            repository: JWTRepository = JWTRepository(),
            user_service: UserService = UserService(),
            access_token_lifetime: timedelta = config.JWT_ACCESS_TOKEN_EXPIRES,
            refresh_token_lifetime: timedelta = config.JWT_REFRESH_TOKEN_EXPIRES
    ) -> None:
        super().__init__(repository=repository)
        self.user_service = user_service
        self.ACCESS_TOKEN_LIFETIME = access_token_lifetime
        self.REFRESH_TOKEN_LIFETIME = refresh_token_lifetime

    def check_revoke(self, token: str) -> bool:
        return self.repository.get_by_pk(token=token).revoked

    def create_tokens(self, auth_data: dict) -> Tokens:
        user = self.user_service.authorize(**auth_data)
        return Tokens(
            access_token=self._create_access_token(user=user, fresh=True),
            refresh_token=self._create_refresh_token(user=user)
        )

    def refresh_access_token(self) -> Tokens:
        return Tokens(
            access_token=self._create_access_token(user=current_user, fresh=False)
        )

    def _create_access_token(self, user: User, fresh: bool) -> JWTToken:
        return self.repository.insert(
            JWTToken(
                token=create_access_token(
                    identity=user,
                    additional_claims={
                        'role': user.role.name,
                        'status': user.status.name
                    },
                    expires_delta=self.ACCESS_TOKEN_LIFETIME,
                    fresh=fresh
                ),
                end_life=dt.now() + self.ACCESS_TOKEN_LIFETIME,
                user_id=user.id
            )
        )

    def _create_refresh_token(self, user: User) -> JWTToken:
        return self.repository.insert(
            JWTToken(
                token=create_refresh_token(
                    identity=user,
                    expires_delta=self.REFRESH_TOKEN_LIFETIME
                ),
                end_life=dt.now() + self.REFRESH_TOKEN_LIFETIME,
                user_id=user.id
            )
        )

    def revoke_token(self) -> None:
        self.repository.update(
            token=get_jwt()['jti'],
            revoked=True
        )

    def revoke_all_tokens(self) -> None:
        self.repository.update_by_user(
            user_id=current_user.id,
            revoked=True
        )

    def delete_expired_token(self, token: str) -> None:
        self.repository.delete(token=token)

    def delete_all_expired_tokens(self) -> None:
        self.repository.delete_expired()
