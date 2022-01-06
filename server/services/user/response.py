from typing import Tuple, List

from .schema import UserSchema
from server.entity import User


class UserResponse(dict):
    pass


class UserSerializer:
    @staticmethod
    def dump(user: User) -> UserResponse:
        return UserResponse(UserSchema().dump(user))

    @staticmethod
    def dump_many(users: Tuple[User, ...]) -> List[UserResponse]:
        return [UserResponse(user) for user in UserSchema(many=True).dump(users)]
