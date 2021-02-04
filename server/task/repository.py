# Класс для работы с БД


class TaskRepository:
    __table = 'tasks'
    __columns = ['id_task', 'title', 'status', 'id_category']
    __primary_key = __columns[0]

    def __init__(self, engine, model):
        self.engine = engine
        self.model = model

    def assert_exist(self, id_task: int):
        self.engine.assert_db(self.__table, self.__primary_key, id_task)

    def get(self):
        return self.engine.select_all(self.__table, sorted_column=self.__primary_key)

    def get_filtered(self, id_category: int):
        return self.engine.select_all(self.__table, self.__columns[3], self.__primary_key, (id_category,))

    def create_table(self):
        types = (
            "INTEGER",
            "title VARCHAR(20)",
            "INTEGER",
            "INTEGER")
        values = list(self.__columns[i] + " " + types[i] for i in range(len(self.__columns)))
        values.append("PRIMARY KEY(" + self.__primary_key + ")")
        values.append("FOREIGN KEY(" + self.__columns[3] + ") REFERENCES categories(" + self.__columns[3] + ")")

        self.engine.create_table(self.__table, values)

    def insert(self, title_task: str, id_category: int):
        value = (title_task, False, id_category)
        self.engine.insert(self.__table, self.__columns[1:], value)

    def update_task(self, id_task: int, title, ):
        value = (title, id_task)
        self.engine.update(self.__table, tuple(self.__columns[1]), self.__primary_key, value)

    def update_category(self, id_task: int, id_category: int):
        value = (id_category, id_task)
        self.engine.update(self.__table, tuple(self.__columns[3]), self.__primary_key, value)

    def update_status(self, id_task: int, status: bool):
        if status:
            int_status = 1
        else:
            int_status = 0
        value = (int_status, id_task)
        self.engine.update(self.__table, tuple(self.__columns[2]), self.__primary_key, value)

    def delete(self, id_task: int):
        self.engine.delete(self.__table, self.__primary_key, (id_task,))
        # files = file_rep.get_by_foreign(id_task)
        # for file in files:
            # file_rep.delete(file[0]) # TODO

