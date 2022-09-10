from datetime import timedelta, datetime as dt
from typing import NamedTuple

from flask_jwt_extended import create_refresh_token, create_access_token, get_jti


from app.config import config
from app.models import User
from app.rest_lib.services import Service
from app.entities.user.service import UserService

from .repository import JWTRepository, JWTToken, PK
from app.errors import Forbidden


class Tokens(NamedTuple):
    access_token: str
    refresh_token: str = None


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

    def check_revoke(self, jti: str) -> bool:
        return self.repository.get_by_pk(PK(jti=jti)).revoked

    def create_tokens(self, auth_data: dict) -> Tokens:
        user = self.user_service.authorize(auth_data)
        return Tokens(
            access_token=self._create_access_token(user=user, fresh=True),
            refresh_token=self._create_refresh_token(user=user)
        )

    def refresh_access_token(self, user: User, refresh_jti: str) -> Tokens:
        if self.repository.get_by_pk(PK(jti=refresh_jti)).user_id != user.id:
            raise Forbidden()

        return Tokens(
            access_token=self._create_access_token(user=user, fresh=False)
        )

    def _create_access_token(self, user: User, fresh: bool) -> str:
        encoded_token = create_access_token(
            identity=user,
            additional_claims={
                'role': user.role.name,
                'status': user.status.name
            },
            expires_delta=self.ACCESS_TOKEN_LIFETIME,
            fresh=fresh
        )
        self.repository.insert(
            JWTToken(
                jti=get_jti(encoded_token),
                end_life=dt.now() + self.ACCESS_TOKEN_LIFETIME,
                user_id=user.id
            )
        )
        return encoded_token

    def _create_refresh_token(self, user: User) -> str:
        encoded_token = create_refresh_token(
            identity=user,
            expires_delta=self.REFRESH_TOKEN_LIFETIME
        )
        self.repository.insert(
            JWTToken(
                jti=get_jti(encoded_token),
                end_life=dt.now() + self.REFRESH_TOKEN_LIFETIME,
                user_id=user.id
            )
        )
        return encoded_token

    def revoke_token(self, jti: str) -> None:
        self.repository.update(
            pk=PK(jti=jti),
            data=dict(
                revoked=True
            )
        )

    def revoke_all_tokens(self, user_id: int) -> None:
        self.repository.update_by_user(
            user_id=user_id,
            data=dict(revoked=True)
        )

    def delete_expired_token(self, jti: str) -> None:
        self.repository.delete(PK(jti=jti))

    def delete_all_expired_tokens(self) -> None:
        self.repository.delete_expired()
