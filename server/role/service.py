from server.role.repository import RoleRepository
from server.role.serializer import serialize_role, RoleSchema
from server.user.service import delete_account


def get_all():
    roles = RoleRepository.get_all()
    return serialize_role(roles, many=True)


def create(name, description):
    role = RoleRepository.insert(name, description)
    return role.id


def update(id, name, description):
    RoleRepository.update(id, name, description)


def delete(id):
    role = RoleRepository.delete(id)
    users_by_role = role.users
    for user in users_by_role:
        delete_account(user.id)

    role = RoleRepository.delete(id)
    return serialize_role(role)
