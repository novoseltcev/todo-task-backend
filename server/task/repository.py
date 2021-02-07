# Класс для работы с БД


class TaskRepository:
    __table__ = 'tasks'
    _id = 'id'
    _title = 'title'
    _status = 'status'
    _category = 'category'

    __primary_key = _id
    __foreign_key = _category

    def __init__(self, engine, model):
        self.engine = engine
        self.model = model

    def assert_exist(self, id: int):
        self.engine.assert_db(self.__table__, self.__primary_key, id)

    def get(self):
        return self.engine.select_all(self.__table__, sorted_column=self.__primary_key)

    def get_by_primary(self, id: int):
        return self.engine.select_one(self.__table__, self.__primary_key, (id,))

    def get_by_foreign(self, category: int):
        return self.engine.select_all(self.__table__, self._category, self.__primary_key, (category,))

    def create_table(self):
        values = (
            self.__primary_key,
            "INTEGER",
            self._title,
            "VARCHAR(20)",
            self._status,
            "INTEGER",
            self._category,
            "INTEGER",
            "PRIMARY KEY(" + self.__primary_key + ")",
            "FOREIGN KEY(" + self.__foreign_key + ") REFERENCES categories(" + self.__foreign_key + ")"
        )

        self.engine.create_table(self.__table__, values)

    def insert(self, title: str, category: int):
        value = (title, False, category)
        self.engine.insert(self.__table__, (self._title, self._status, self._category), value)

    def update_title(self, id: int, title: str):
        value = (title, id)
        self.engine.update(self.__table__, (self._title,), self.__primary_key, value)

    def update_category(self, id: int, category: int):
        value = (category, id)
        self.engine.update(self.__table__, (self._category,), self.__primary_key, value)

    def update_status(self, id: int):
        status = self.get_by_primary(id)[2]
        new_status = (status + 1) % 2
        value = (new_status, id)
        self.engine.update(self.__table__, (self._status,), self.__primary_key, value)

    def delete(self, id_task: int):
        self.engine.delete(self.__table__, self.__primary_key, (id_task,))
