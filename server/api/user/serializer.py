from server.api.user.schema import UserSchema
from server.api.user.model import User


def serialize_user(user: User, many=False):
    return UserSchema(many=many).dump(user)
