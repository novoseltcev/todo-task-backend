from __future__ import annotations
from typing import Tuple

from server.services.user.schema import UserSchema
from server.services.user.model import User


class UserResponse(dict):
    @staticmethod
    def dump(user: User | Tuple[User], many=False):
        return UserResponse(UserSchema(many=many).dump(user))

    @staticmethod
    def success():
        return UserResponse(success=True)
