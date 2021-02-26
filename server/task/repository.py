# Класс для работы с БД
from sqlalchemy.orm.exc import MultipleResultsFound

from server import DB_session

from .model import Task


def session_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            DB_session.commit()
        except Exception as e:
            DB_session.rollback()
            raise e

    return wrapper


class TaskRepository:

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def __get_by(all_rows=False, **kwargs):
        assert (len(kwargs.items()) != 0)
        query = Task.query.filter_by(**kwargs)
        if all_rows:
            return query.all()
        return query.one()

    def get_by_primary(self, id: int):
        return self.__get_by(id=id)

    def get_by_foreign(self, category: int):
        return self.__get_by(all_rows=True, category=category)

    def assert_id(self, field='id'):
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.get_by_primary(kwargs[field])
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @session_handler
    def insert(self, title: str, category: int):
        task = Task(title=title, status=False, category=category)
        DB_session.add(task)

    @session_handler
    def update(self, id: int, title: str, status: int, category: int):
        task = self.get_by_primary(id)
        task.title = title
        task.status = status
        task.category = category

    @session_handler
    def delete(self, id: int):
        DB_session.delete(self.get_by_primary(id))
