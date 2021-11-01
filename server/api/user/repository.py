from server import sqlalchemy_session
from server.errors.exc import UserUnknownId
from server.views import session_handler
from server.api.user.model import User


class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    @session_handler
    def get_by_id(id: int):
        user = User.query.get(id)
        if not user:
            raise UserUnknownId(id)
        return user

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).one()

    @staticmethod
    @session_handler
    def insert(email: str, password: str, reg_date):
        user = User(email=email, password=password, reg_date=reg_date)
        sqlalchemy_session.add(user)
        return user

    @staticmethod
    @session_handler
    def update(schema: dict):
        id = schema['id']
        q = User.query.filter_by(id=id)
        if q.first() is None:
            raise UserUnknownId(id)
        q.update(schema)

    @classmethod
    @session_handler
    def delete(cls, id: int):
        user = cls.get_by_id(id)
        sqlalchemy_session.delete(user)
        return user

    @classmethod
    @session_handler
    def confirm_email(cls, id: int):
        user = cls.get_by_id(id)
        user.confirmed_email = True
