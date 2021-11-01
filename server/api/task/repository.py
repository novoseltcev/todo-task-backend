from server import sqlalchemy_session
from server.views import session_handler
from server.errors.exc import TaskUnknownId
from server.api.task.model import Task


class TaskRepository:
    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def get_by_id(id_user, id: int):
        task = Task.query.filter_by(id=id, id_user=id_user).first()
        if task is None:
            raise TaskUnknownId(id)
        return task

    @staticmethod
    def get_by_category_id(id_user, id_category: int):
        return Task.query.filter_by(id_category=id_category, id_user=id_user).all()

    @staticmethod
    @session_handler
    def insert(id_user, schema):
        task = Task(**schema, id_user=id_user)
        sqlalchemy_session.add(task)
        return task

    @staticmethod
    @session_handler
    def update(id_user, schema):
        id = schema['id']
        q = Task.query.filter_by(id=id, id_user=id_user)
        if q.first() is None:
            raise TaskUnknownId(id)
        q.update(schema)

    @classmethod
    @session_handler
    def delete(cls, id_user, id: int):
        task = cls.get_by_id(id_user, id)
        sqlalchemy_session.delete(task)
        return task
