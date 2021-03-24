from sqlalchemy.orm.exc import NoResultFound

from server import sqlalchemy_session
from server.errors.exc import RoleUnknownId
from server.views import session_handler
from server.role.model import Role


class RoleRepository:
    @staticmethod
    def get_all():
        return Role.query.all()

    @staticmethod
    @session_handler
    def get_by_id(id: int):
        user = Role.query.get(id)
        if user:
            return user
        raise RoleUnknownId(id)

    @staticmethod
    @session_handler
    def insert(name: str, description: str):
        role = Role(name=name, description=description)
        sqlalchemy_session.add(role)
        return role

    @staticmethod
    @session_handler
    def update(schema: dict):
        id = schema['id']
        q = Role.query.filter_by(id=id)
        if q.first() is None:
            raise RoleUnknownId(id)
        q.update(schema)

    @classmethod
    @session_handler
    def delete(cls, id: int):
        role = cls.get_by_id(id)
        sqlalchemy_session.delete(role)
        return role
