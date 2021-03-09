from sqlalchemy.orm.exc import NoResultFound

from server import DB_session
from server.index import session_handler
from server.errors.exc import TaskUnknownId
from server.task.model import Task


class TaskRepository:

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def get_by_id(id: int):
        task = Task.query.get(id)
        if task:
            return task
        raise TaskUnknownId(id)

    @staticmethod
    def get_by_category_id(category_id: int):
        return Task.query.filter_by(category_id=category_id).all()

    @staticmethod
    @session_handler
    def insert(schema):
        task = Task(**schema)
        DB_session.add(task)
        return task

    @staticmethod
    @session_handler
    def update(schema):
        id = schema['id']
        try:
            q = Task.query.filter_by(id=id)
            q.one()
            q.update(schema)
        except NoResultFound:
            raise TaskUnknownId(id)

    @classmethod
    def delete(cls, id: int):
        task = cls.get_by_id(id)
        DB_session.delete(task)
        return task
