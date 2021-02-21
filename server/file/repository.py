# Класс для работы с БД
from database import DBManager

from .model import File


class FileRepository(DBManager):
    def __init__(self):
        super().__init__(File)

    def get_by_primary(self, id: int):
        return self._get_by(id=id)

    def get_by_name(self, name):
        return self._get_by(name=name)

    def get_by_foreign(self, task: int):
        return self._get_by(task=task, all_rows=True)

    @DBManager.session_handler
    def insert(self, name: str, path: str, task: int):
        self._insert(name=name, path=path, task=task)

    @DBManager.session_handler
    def delete(self, id: int):
        self._delete(id)
