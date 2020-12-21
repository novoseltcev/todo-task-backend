import os
import sqlite3


class SQLiteDB:
    _default = "None"
    current_category_id = 1

    def __init__(self, path="server/data"):
        self._setup_path(path)
        self.sqlite_connection = sqlite3.connect(self.path, check_same_thread=False)
        self.sqlite_connection.row_factory = sqlite3.Row
        self.cursor = self.sqlite_connection.cursor()
        self.create_tables()

    def _setup_path(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                files = []
                for file in os.listdir(path):
                    if file.endswith(".db"):
                        files.append(file)
                if len(files) != 0:
                    self.path = os.path.join(path, files[0])
                else:
                    self.__create_file_db(os.path.join(path, "task.db"))
            if os.path.isfile(path):
                self.path = path
        else:
            if os.path.isdir(path):
                self.__create_file_db(os.path.join(path, "task.db"))
            if os.path.isfile(path) and os.path.splitext(path)[1] == ".db":
                self.__create_file_db(path)
            if os.path.isfile(path) and os.path.splitext(path)[1] != ".db":
                self.__create_file_db(os.path.splitext(path)[0] + ".db")

    def __create_file_db(self, path):
        self.path = path
        with open(path, "w"):
            pass

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS categories (id_category INTEGER, name_category varchar(20) UNIQUE, PRIMARY KEY(id_category));")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id_task INTEGER, title VARCHAR(20), status INTEGER , id_category INTEGER, PRIMARY KEY(id_task), FOREIGN KEY(id_category) REFERENCES categories(id_category));")
        self.cursor.execute("SELECT COUNT(id_category) FROM categories")
        categories_count = self.cursor.fetchone()
        if categories_count == (0,):
            self.append_category(self._default)

    def __del__(self):
        self.sqlite_connection.close()

    def _remove(self, table, id_field, id_value: int):
        self.cursor.execute("DELETE FROM ? WHERE ?=?;", (table, id_field, id_value, ))

    def _get_table(self, name):
        self.cursor.execute("SELECT * FROM ?;", name)
        return self.cursor.fetchall()

    def _get_filtered_table(self, name, filter_key=True, filter_field="", filter_value=""):
        if filter_key:
            return self._get_table(name + " WHERE {0}={1}".format(filter_field, filter_value))
        else:
            return self._get_table(name)

    def _get_sorted_table(self, name, sort_field, filter_key=False, filter_field="", filter_value=""):
        return self._get_filtered_table(name, filter_key, filter_field, filter_value + " ORDER BY {0} DESC".format(sort_field))

    def append_task(self, title_task: str):
        self.cursor.execute("INSERT INTO tasks (title, status, id_category) VALUES (?, FALSE, ?)", (title_task, self.current_category_id,))
        self.sqlite_connection.commit()

    def append_category(self, category: str):
        self.cursor.execute("INSERT INTO categories (name_category) VALUES (?);", (category,))
        self.sqlite_connection.commit()

    def update_task_status(self, task_id: int):
        self.cursor.execute("SELECT status FROM tasks WHERE id_task = ?;", (task_id,))
        prev_status = (self.cursor.fetchone()[0] + 1) % 2
        self.cursor.execute(f"UPDATE tasks SET status={prev_status} WHERE id_task=?;", (task_id,))
        self.sqlite_connection.commit()

    def update_task_category(self, task_id: int, category: str):
        self.cursor.execute("SELECT id FROM categories WHERE name_category = ?;", (category,))
        self.cursor.execute(f"UPDATE tasks SET id_category={self.cursor.fetchone()[0]} WHERE id_task=?;", (task_id,))
        self.sqlite_connection.commit()

    def rename_category(self, destination: str, source: str):
        self.cursor.execute(f"UPDATE categories SET name_category=? WHERE name_category=?;", (source, destination,))
        self.sqlite_connection.commit()

    def remove_task(self, task_id: int):
        self._remove("tasks", "id_task", task_id)
        # self.cursor.execute("DELETE FROM tasks WHERE id_task = ?;", (task_id,))

    def remove_category(self, category_id: int):
        self._remove("categories", "id_category", category_id)
        # self.cursor.execute("DELETE FROM categories WHERE id_category = ?;", (category_id,))

    def get_tasks(self):
        if self.current_category_id == 1:
            return self._get_sorted_table("tasks", "task_id")
        return self._get_sorted_table("tasks", "task_id", True, "category_id", str(1))

    def get_categories(self):
        return self._get_table("categories")
