# Класс для работы с БД

from database.manager import DBManager

from .model import Task


class TaskRepository(DBManager):
    def __init__(self):
        super().__init__(Task)

    def get_by_primary(self, id: int):
        return self._get_by(all_rows=False, id=id)

    def get_by_foreign(self, category: int):
        return self._get_by(all_rows=True, category=category)

    @DBManager.session_handler
    def insert(self, title: str, category: int):
        self._insert(title=title, status=False, category=category)

    @DBManager.session_handler
    def update_title(self, id: int, title: str):
        task = self._get_by(id=id)
        task.change_title(title)

    @DBManager.session_handler
    def update_category(self, id: int, category: int):
        task = self._get_by(id=id)
        task.change_category(category)

    @DBManager.session_handler
    def update_status(self, id: int):
        task = self._get_by(id=id)
        task.change_status()

    @DBManager.session_handler
    def delete(self, id: int):
        self._delete(id)

