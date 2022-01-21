from typing import Tuple, List

from .schema import UserSchema
from ..business import Account


class UserResponse(dict):
    pass


class UserSerializer:
    @staticmethod
    def dump(user: Account) -> UserResponse:
        return UserResponse(UserSchema().dump(user))

    @staticmethod
    def dump_many(users: Tuple[Account, ...]) -> List[UserResponse]:
        return [UserResponse(user) for user in UserSchema(many=True).dump(users)]
