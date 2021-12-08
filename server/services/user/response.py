from typing import Tuple

from .schema import UserSchema
from .entity import User


class UserResponse(dict):
    pass


class UserSerializer:
    @staticmethod
    def dump(user: User) -> UserResponse:
        return UserResponse(UserSchema(many=False).dump(user))

    @staticmethod
    def dump_many(users: Tuple[User]) -> UserResponse:
        return UserResponse(UserSchema(many=True).dump(users))
