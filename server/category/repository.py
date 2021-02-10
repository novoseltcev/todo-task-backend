# Класс для работы с БД
from database import DBManager


class CategoryRepository(DBManager):
    __default = 'All'

    def __init__(self, engine, model):
        super().__init__(engine, model)
        session = self.session_maker()
        count = session.query(self.model).count()
        if count == 0:
            self.insert(self.__default)

    def get_by_name(self, name):
        return self._get_by(name=name)

    def insert(self, name: str):
        self._insert(name=name)

    def update_name(self, id: int, source: str):
        category, session = self._before(id)
        category.change_name(source)
        session.commit()

    def delete(self, id: int):
        self._delete(id)
