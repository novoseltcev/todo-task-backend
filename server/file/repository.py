# Класс для работы с БД
from database import DBManager


class FileRepository(DBManager):

    def get_by_primary(self, id: int):
        return self._get_by(id=id)

    def get_by_name(self, name):
        return self._get_by(name=name)

    def get_by_foreign(self, task):
        return self._get_by(task=task, all_rows=True)

    def insert(self, name: str, path: str, task: int):
        self._insert(name=name, path=path, task=task)

    def update_task(self, id: int, task: int):
        file, session = self._before(id)
        file.change_task(task)
        session.commit()

    def delete(self, id: int):
        self._delete(id)
