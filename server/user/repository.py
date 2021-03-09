from sqlalchemy.orm.exc import NoResultFound

from server import DB_session
from server.errors.exc import UserUnknownId
from server.index import session_handler
from server.user.model import User


class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    @session_handler
    def get_by_id(id: int):
        user = User.query.get(id)
        if user:
            return user
        raise UserUnknownId(id)

    @staticmethod
    def get_by_login(login: str):
        return User.query.filter_by(login=login).all()

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).all()

    @staticmethod
    @session_handler
    def insert(login: str, email: str, password: str, reg_date):
        user = User(login=login, email=email, password=password, reg_date=reg_date)
        DB_session.add(user)
        return user.id

    @staticmethod
    @session_handler
    def update(schema: dict):
        id = schema['id']
        try:
            q = User.query.filter_by(id=id)
            q.one()
            q.update(schema)
        except NoResultFound:
            raise UserUnknownId(id)

    @classmethod
    @session_handler
    def delete(cls, id: int):
        user = cls.get_by_id(id)
        DB_session.delete(user)
        return user
