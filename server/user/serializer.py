# Серилазизация данных
from server.user.schema import UserSchema
from server.user.model import User


def serialize_user(user: User, many=False):
    return UserSchema(many=many).dump(user)
