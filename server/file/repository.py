from server import DB_session
from server.errors.exc import FileUnknownId
from server.index import session_handler
from server.file.model import File


class FileRepository:
    @staticmethod
    def get_all():
        return File.query.all()

    @staticmethod
    def get_by_id(id: int):
        file = File.query.get(id)
        if file:
            return file
        raise FileUnknownId(id)

    @staticmethod
    def get_by_task_id(task_id: int):
        return File.query.filter_by(task_id=task_id).all()

    @staticmethod
    @session_handler
    def insert(name: str, path: str, task_id: int):
        file = File(name=name, path=path, task_id=task_id)
        DB_session.add(file)
        return file

    @classmethod
    @session_handler
    def delete(cls, id: int):
        file = cls.get_by_id(id)
        DB_session.delete(file)
        return file
