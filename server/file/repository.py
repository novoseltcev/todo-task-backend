# Класс для работы с БД
import os


class FileRepository:
    __table = 'files'
    _id = 'id'
    _name = "name"
    _path = 'path'
    _task = 'task'

    __primary_key = _id
    __foreign_key = _task

    def __init__(self, engine, model):
        self.engine = engine
        self.model = model

    def assert_exist(self, id: int):
        self.engine.assert_db(self.__table, self.__primary_key, id)

    def get(self):
        return self.engine.select_all(self.__table)

    def get_by_primary(self, id: int):
        return self.engine.select_one(self.__table, filter_column=self._id, value=(id,))

    def get_by_name(self, name):
        return self.engine.select_all(self.__table, filter_column=self._name, value=(name,))

    def get_by_foreign(self, task):
        return self.engine.select_all(self.__table, filter_column=self.__foreign_key, value=(task,))

    def create_table(self):
        self.engine.create_table(self.__table,
                                 (
                                     self._id + " INTEGER",
                                     self._name + " VARCHAR(40)",
                                     self._path + " TEXT UNIQUE",
                                     self._task + " INTEGER",
                                     "PRIMARY KEY(" + self.__primary_key + ")",
                                     "FOREIGN KEY(" + self.__foreign_key + ") REFERENCES tasks(" + self.__foreign_key + ")"
                                 )
                                 )

    def insert(self, name: str, data, task: int, path: str):
        value = (name, path, task)
        self.engine.insert(self.__table, (self._name, self._path, self._task), value)
        with open(path, 'wb+') as fp:
            fp.write(data)

    def update_task(self, id: int, task: int):
        value = (task, id)
        self.engine.update(self.__table, (self.__foreign_key,), self.__primary_key, value)

    def delete(self, id: int):
        self.engine.delete(self.__table, self.__primary_key, (id,))
