# Класс для работы с БД
from server import DB_session

from .model import File


def session_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            DB_session.commit()
        except Exception as e:
            DB_session.rollback()
            raise e

    return wrapper


class FileRepository:
    @staticmethod
    def get_all():
        return File.query.all()

    @staticmethod
    def __get_by(all_rows=False, **kwargs):
        assert (len(kwargs.items()) != 0)
        query = File.query.filter_by(**kwargs)
        if all_rows:
            return query.all()
        return query.one()

    def get_by_primary(self, id: int):
        return self.__get_by(id=id)

    def get_by_name(self, name):
        return self.__get_by(name=name)

    def get_by_foreign(self, task: int):
        return self.__get_by(task=task, all_rows=True)

    def assert_id(self, field='id'):
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.get_by_primary(kwargs[field])
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @session_handler
    def insert(self, name: str, path: str, task: int):
        file = File(name=name, path=path, task=task)
        DB_session.add(file)

    @session_handler
    def delete(self, id: int):
        DB_session.delete(self.get_by_primary(id))
