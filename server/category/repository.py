# Класс для работы с БД


class CategoryRepository:
    __table = 'categories'
    _id = 'id'
    _name = 'name'

    __primary_key = _id
    __default = 'All'

    def __init__(self, engine, model):
        self.engine = engine
        self.model = model

    def assert_exist(self, id: int):
        return self.engine.assert_db(self.__table, self.__primary_key, id)

    def create_tables(self):
        res = self.engine.create_table(self.__table,
                                       (
                                           self._id + " INTEGER",
                                           self._name + " varchar(20) UNIQUE",
                                           "PRIMARY KEY(" + self.__primary_key + ")"
                                       )
                                       )

        try:
            self.engine.assert_db(self.__table, self.__primary_key, 1)
            return res
        except ValueError:
            return self.engine.insert(self.__table, (self._name,), (self.__default,))

    def get(self):
        return self.engine.select_all(self.__table)

    def get_by_name(self, name):
        return self.engine.select_one(self.__table, self._name, (name,))

    def insert(self, category: str):
        value = (category,)
        return self.engine.insert(self.__table, (self._name,), value)

    def update_name(self, id: int, source: str):
        value = (source, id)
        return self.engine.update(self.__table, (self._name,), self.__primary_key, value)

    def delete(self, id: int):
        return self.engine.delete(self.__table, self.__primary_key, (id,))
