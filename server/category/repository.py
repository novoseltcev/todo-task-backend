# Класс для работы с БД
from server.initialize_db import engine


class CategoryRepository:
    __table = 'categories'
    __columns = ['id_category', 'name']
    __primary_key = __columns[0]
    __default = 'All'

    def __init__(self):
        self.engine = engine

    def assert_exist(self, id_category: int):
        self.engine.assert_db(self.__table, self.__primary_key, id_category)

    def create_tables(self):
        res = self.engine.create_table(self.__table,
                                 (
                                     "id_category INTEGER",
                                     "name varchar(20) UNIQUE",
                                     "PRIMARY KEY(id_category)"
                                 )
                                 )

        try:
            self.engine.assert_db(self.__table, self.__primary_key, 1)
            return res
        except ValueError:
            return self.engine.insert(self.__table, tuple(self.__columns[1]), tuple(self.__default))

    def get(self):
        return self.engine.select_all(self.__table)

    def get_by_name(self, name):
        return self.engine.select_one(self.__table, self.__columns[1], name)

    def insert(self, category: str):
        value = (category,)
        return self.engine.insert(self.__table, tuple(self.__columns[1]), value)

    def update_name(self, id_destination: int, source: str):
        value = (source, id_destination)
        return self.engine.update(self.__table, tuple(self.__columns[1]), self.__primary_key, value)

    def delete(self, id_category: int):
        return self.engine.delete(self.__table, self.__primary_key, (id_category,))


category_rep = CategoryRepository()
