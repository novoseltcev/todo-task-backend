# Класс для работы с БД
from sqlalchemy.orm import sessionmaker

from database.manager import DBManager


class TaskRepository(DBManager):

    def get_by_primary(self, id: int):
        return self._get_by(all_rows=False, id=id)

    def get_by_foreign(self, category: int):
        return self._get_by(all_rows=True, category=category)

    def insert(self, title: str, category: int):
        self._insert(title=title, status=False, category=category)

    def update_title(self, id: int, title: str):
        task, session = self._before(id)
        task.change_title(title)
        session.commit()

    def update_category(self, id: int, category: int):
        task, session = self._before(id)
        task.change_category(category)
        session.commit()

    def update_status(self, id: int):
        task, session = self._before(id)
        task.change_status()
        session.commit()

    def delete(self, id: int):
        self._delete(id)
