# Класс для работы с БД


class FileRepository:
    __table = 'files'
    __columns = ['id_file', 'file_name', 'file_path', 'id_task']
    __primary_key = __columns[0]

    def __init__(self, engine, model):
        self.engine = engine
        self.model = model

    def assert_exist(self, id_file: int):
        self.engine.assert_db(self.__table, self.__primary_key, id_file)

    def get(self):
        return self.engine.select_all(self.__table)

    def get_by_primary(self, id_file: int):
        return self.engine.select_one(self.__table, filter_column="id_file", value=(id_file,))

    def get_by_foreign(self, id_task):
        return self.engine.select_all(self.__table, filter_column=self.__columns[3], value=(id_task,))

    def create_table(self):
        self.engine.create_table(self.__table,
                                 (
                                     "id_file INTEGER",
                                     "filename VARCHAR(40)",
                                     "path TEXT",
                                     "id_task INTEGER",
                                     "PRIMARY KEY(id_file)",
                                     "FOREIGN KEY(id_task) REFERENCES tasks(id_task)"
                                 )
                                 )

    def insert(self, filename: str, path: str, id_task: int):
        value = (filename, path, id_task)
        self.engine.insert(self.__table, self.__columns[1:], value)

    def update_task(self, id_file: int, id_task: int):
        value = (id_task, id_file)
        self.engine.update(self.__table, (self.__columns[3],), self.__primary_key, value)

    def delete(self, id_file: int):
        self.engine.delete(self.__table, self.__columns, (id_file,))
