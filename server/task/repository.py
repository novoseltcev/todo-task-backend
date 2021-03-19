from sqlalchemy.orm.exc import NoResultFound

from server import DB_session
from server.views import session_handler
from server.errors.exc import TaskUnknownId
from server.task.model import Task


class TaskRepository:

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def get_by_id(id_user, id: int):
        task = Task.query.filter_by(id=id, id_user=id_user).first()
        if task:
            return task
        raise TaskUnknownId(id)

    @staticmethod
    def get_by_category_id(id_user, id_category: int):
        return Task.query.filter_by(id_category=id_category, id_user=id_user).all()

    @staticmethod
    @session_handler
    def insert(id_user, schema):
        task = Task(**schema, id_user=id_user)
        DB_session.add(task)
        return task

    @staticmethod
    @session_handler
    def update(id_user, schema):
        id = schema['id']
        try:
            q = Task.query.filter_by(id=id, id_user=id_user)
            q.one()
            q.update(schema)
        except NoResultFound:
            raise TaskUnknownId(id)

    @classmethod
    @session_handler
    def delete(cls, id_user, id: int):
        task = cls.get_by_id(id_user, id)
        DB_session.delete(task)
        return task
