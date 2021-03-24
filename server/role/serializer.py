from server.role.schema import RoleSchema
from server.role.model import Role


def serialize_role(role: Role, many=False):
    return RoleSchema(many=many).dump(role)
