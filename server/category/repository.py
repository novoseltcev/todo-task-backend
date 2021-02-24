# Класс для работы с БД
from sqlalchemy.orm.exc import MultipleResultsFound

from server import DB_session

from .model import Category


def session_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            DB_session.commit()
        except Exception as e:
            DB_session.rollback()
            raise e

    return wrapper


class CategoryRepository:
    __default = 'All'

    def __init__(self):  # TODO - it's a business logic in repository
        pass
        # count = Category.query.count()
        # if count == 0:
        #     self.insert(self.__default)

    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def __get_by(all_rows=False, **kwargs):
        assert (len(kwargs.items()) != 0)
        query = Category.query.filter_by(**kwargs)
        if all_rows:
            return query.all()
        return query.one()

    def get_by_primary(self, id: int):
        return self.__get_by(id=id)

    def get_by_name(self, name: str):
        return self.__get_by(name=name)

    def assert_id(self, func):
        def wrapper(id, *args, **kwargs):
            self.get_by_primary(id)
            return func(id, *args, **kwargs)

        return wrapper

    @session_handler
    def insert(self, name: str):
        category = Category(name=name)
        DB_session.add(category)

    @session_handler
    def update(self, id: int, name: str):
        category = self.get_by_primary(id=id)
        category.name = name

    @session_handler
    def delete(self, id: int):
        DB_session.delete(self.get_by_primary(id))
