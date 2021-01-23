#
# класс SQLiteDB,
# обёрка над БД,
# реализует базовые запросы к БД без знания логики приложения
#
from server.sqlite_utility import SQLiteUtility


class SQLiteDB:
    __default = "All"

    def __init__(self, path="server/data/task.db"):
        self.utility = SQLiteUtility(path)
        self.create_tables()

    def assert_task(self, id_task: int):
        self.utility.assert_db("tasks", "id_task", id_task)

    def assert_category(self, id_category: int):
        self.utility.assert_db("categories", "id_category", id_category)

    def assert_file(self, id_file: int):
        self.utility.assert_db("files", "id_file", id_file)

    def create_tables(self):
        self.utility.create_table("categories",
                                  (
                                      "id_category INTEGER",
                                      "name_category varchar(20) UNIQUE",
                                      "PRIMARY KEY(id_category)"
                                  )
                                  )

        self.utility.create_table("files",
                                  (
                                      "id_file INTEGER",
                                      "file_name VARCHAR(40)",
                                      "file_data BLOB",
                                      "PRIMARY KEY(id_file)"
                                  )
                                  )

        self.utility.create_table("tasks",
                                  (
                                      "id_task INTEGER",
                                      "title VARCHAR(20)",
                                      "status INTEGER",
                                      "id_category INTEGER",
                                      "id_file INTEGER",
                                      "PRIMARY KEY(id_task)",
                                      "FOREIGN KEY(id_category) REFERENCES categories(id_category)",
                                      "FOREIGN KEY(id_file) REFERENCES files(id_file)"
                                  )
                                  )

        try:
            self.utility.assert_db("categories", "id_category", 1)
        except ValueError:
            self.utility.insert("categories", "name_category", self.__default)

    def get_all_tasks(self):
        return self.utility.select_all("tasks", sorted_column="id_task")

    def get_filtered_tasks(self, id_category):
        return self.utility.select_all("tasks", "id_category", "id_task", (id_category,))

    def get_categories(self):
        return self.utility.select_all("categories")

    def get_file(self, id_file: int):
        return self.utility.select_one("files", filter_column="id_file", value=(id_file,))

    def get_files(self):
        return self.utility.select_all("files")

    def insert_task(self, title_task: str, id_category: int):
        value = (title_task, False, id_category, 0)
        self.utility.insert("tasks", ("title", "status", "id_category", "id_file"), value)

    def insert_category(self, category: str):
        value = (category,)
        self.utility.insert("categories", ("name_category",), value)

    def insert_file(self, filename: str, file_data):
        value = (filename, file_data)
        self.utility.insert("files", ("file_name", "file_data"), value)

    def update_task(self, id_task: int, title, status: int, id_category: int):
        value = (title, status, id_category, id_task)
        self.utility.update("tasks", ("title", "status", "id_category"), "id_task", value)

    def update_task_file(self, id_task: int, id_file: int):
        value = (id_file, id_task)
        self.utility.update("tasks", ("id_file",), "id_task", value)

    def update_category(self, id_destination: int, source: str):
        value = (source, id_destination)
        self.utility.update("categories", ("name_category",), "id_category", value)

    def delete_task(self, id_task: int):
        self.utility.delete("tasks", "id_task", (id_task,))

    def delete_category(self, id_category: int):
        self.utility.delete("categories", "id_category", (id_category,))

    def delete_file(self, id_file: int):
        self.utility.delete("files", "id_file", (id_file,))

    def __del__(self):
        self.utility.__del__()
