from datetime import timedelta
from typing import List

from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash

from app.errors import Unauthorized, Forbidden, NoSuchEntityError
from app.models import Role, User
from app.config import config
from app.entities.user.service import UserService


class AuthService:
    def __init__(
            self,
            user_service: UserService = UserService(),
            access_token_lifetime: timedelta = config.JWT_ACCESS_TOKEN_EXPIRES
    ) -> None:
        self.user_service = user_service
        self.ACCESS_TOKEN_LIFETIME = access_token_lifetime
        self.user: User | None = None

    def allowed_roles(self, roles: List[Role], optional=False, fresh=False):
        def inner(func):
            @jwt_required(optional=optional, fresh=fresh)
            def wrapper(*args, **kwargs):
                jwt_identity = get_jwt_identity()
                if jwt_identity:
                    self.load_user(jwt_identity)
                    self._check_usable()
                    self._check_roles(roles)
                return func(*args, **kwargs)

            def wrapper_without_auth(*args, **kwargs):
                self.user = User(id=1, email='test@test.com', password=generate_password_hash('test'))
                return func(*args, **kwargs)

            return wrapper_without_auth if config.AUTH_DISABLE else wrapper

        return inner

    def load_user(self, user_id: int) -> None:
        try:
            self.user = self.user_service.get_by_pk(user_id)
        except NoSuchEntityError as e:
            raise Unauthorized('Данный пользователь был удален.') from e

    def _check_usable(self):
        self.user_service.check_usable(self.user)

    def _check_roles(self, roles):
        if self.user.role not in roles:
            raise Forbidden('Вам запрещен доступ к данной информации.')


auth_service = AuthService()
