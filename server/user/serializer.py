# Серилазизация данных
from .schema import UserSchema
from .model import User


def serialize_user(user: User, many=False):
    return UserSchema(many=many).dump(user)
