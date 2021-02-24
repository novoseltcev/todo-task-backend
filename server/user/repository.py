from server import DB_session

from .model import User


def session_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            DB_session.commit()
        except Exception as e:
            DB_session.rollback()
            raise e

    return wrapper


class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def __get_by(all_rows=False, **kwargs):
        assert (len(kwargs.items()) != 0)
        query = User.query.filter_by(**kwargs)
        if all_rows:
            return query.all()
        return query.one()

    def get_by_primary(self, id: int):
        return self.__get_by(id=id)

    @staticmethod
    def get_by_login_or_email(value: str):
        query = User.query.filter_by(User.login == value, User.email == value)
        return query.one()

    def assert_id(self, func):
        def wrapper(id, *args, **kwargs):
            self.get_by_primary(id)
            return func(id, *args, **kwargs)

        return wrapper

    @session_handler
    def insert(self, login: str, email: str, password: str, date):
        user = User(login=login, email=email, password=password, reg_date=date)
        DB_session.add(user)

    @session_handler
    def update(self, id: int, email: str, password: str):
        user = self.get_by_primary(id)
        user.email = email
        user.password = password

    @session_handler
    def delete(self, id: int):
        DB_session.delete(self.get_by_primary(id))
