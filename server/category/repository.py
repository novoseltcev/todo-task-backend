# Класс для работы с БД
from database import DBManager

from .model import Category


class CategoryRepository(DBManager):
    __default = 'All'

    def __init__(self):
        super().__init__(Category)
        count = self.model.query.count()
        if count == 0:
            self.insert(self.__default)

    def get_by_name(self, name):
        return self._get_by(name=name)

    def insert(self, name: str):
        self._insert(name=name)

    @DBManager.session_handler
    def update_name(self, id: int, source: str):
        category = self._get_by(id=id)
        category.change_name(source)

    def delete(self, id: int):
        self._delete(id)
