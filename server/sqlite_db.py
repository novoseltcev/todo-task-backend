#
# класс SQLiteD,
# обёрка над БД,
# реализует базовые запросы к БД без знания логики приложения
#
import os
import sqlite3


class SQLiteDB:
    _default = "None"

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

    def is_exist_category(self, id_category: int):
        self.cursor.execute("SELECT COUNT(id_category) FROM categories WHERE id_category=?", (id_category,))
        categories_count = self.cursor.fetchone()[0]
        if categories_count == 0:
            raise ValueError("id_category=" + str(id_category) + " isn't exists")

    def is_exist_task(self, id_task: int):
        self.cursor.execute("SELECT COUNT(id_task) FROM tasks WHERE id_task=?", (id_task,))
        categories_count = self.cursor.fetchone()[0]
        if categories_count == 0:
            raise ValueError("id_task=" + str(id_task) + " isn't exists")

    def is_exist_file(self, id_file: int):
        self.cursor.execute("SELECT COUNT(id_file) FROM files WHERE id_file=?", (id_file,))
        categories_count = self.cursor.fetchone()[0]
        if categories_count == 0:
            raise ValueError("id_file=" + str(id_file) + " isn't exists")

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS categories (id_category INTEGER, "
                            "name_category varchar(20) UNIQUE, PRIMARY KEY(id_category));")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS files (id_file INTEGER, file_name VARCHAR(40),"
                            "file_data BLOB, PRIMARY KEY(id_file));")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id_task INTEGER, title VARCHAR(20), status INTEGER , "
                            "id_category INTEGER, id_file INTEGER, PRIMARY KEY(id_task), "
                            "FOREIGN KEY(id_category) REFERENCES categories(id_category),"
                            "FOREIGN KEY(id_file) REFERENCES files(id_file));")
        try:
            self.is_exist_category(1)
        except ValueError:
            self.insert_category(self._default)

    def get_all_tasks(self):
        self.cursor.execute("SELECT * FROM tasks ORDER BY id_task DESC;")
        return self.cursor.fetchall()

    def get_filtered_tasks(self, id_category):
        self.cursor.execute("SELECT * FROM tasks WHERE id_category=? ORDER BY id_task DESC;", (id_category,))
        return self.cursor.fetchall()

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories;")
        return self.cursor.fetchall()

    def get_file(self, id_file: int):
        self.cursor.execute("SELECT file_name, file_data FROM files WHERE id_file=?;", (id_file,))
        return self.cursor.fetchone()

    def get_files(self):
        self.cursor.execute("SELECT * FROM files")
        return self.cursor.fetchall()

    def insert_task(self, title_task: str, id_category: int):
        self.cursor.execute("INSERT INTO tasks (title, status, id_category) VALUES (?, FALSE, ?)",
                            (title_task, id_category,))
        self.sqlite_connection.commit()

    def insert_category(self, category: str):
        self.cursor.execute("INSERT INTO categories(name_category) VALUES (?);", (category,))
        self.sqlite_connection.commit()

    def insert_file(self, filename: str, file_data):
        self.cursor.execute("INSERT INTO files(file_name, file_data) VALUES (?, ?)", (filename, file_data,))
        self.sqlite_connection.commit()

    def update_task_status(self, id_task: int, new_status: int):
        self.cursor.execute("UPDATE tasks SET status=? WHERE id_task=?;", (new_status, id_task,))
        self.sqlite_connection.commit()

    def update_task_category(self, id_task: int, id_category: int):
        self.cursor.execute("UPDATE tasks SET id_category=? WHERE id_task=?;", (id_category, id_task,))
        self.sqlite_connection.commit()

    def update_task_file(self, id_task: int, id_file: int):
        self.cursor.execute("UPDATE tasks SET id_file=? WHERE id_task=?;", (id_file, id_task,))
        self.sqlite_connection.commit()

    def update_category_name(self, id_destination: int, source: str):
        self.cursor.execute("UPDATE categories SET name_category=? WHERE id_category=?;", (source, id_destination,))
        self.sqlite_connection.commit()

    def delete_task(self, id_task: int):
        self.cursor.execute("DELETE FROM tasks WHERE id_task=?;", (id_task,))
        self.sqlite_connection.commit()

    def delete_category(self, id_category: int):
        self.cursor.execute("DELETE FROM categories WHERE id_category=?;", (id_category,))
        self.sqlite_connection.commit()

    def delete_file(self, id_file: int):
        self.cursor.execute("DELETE FROM files WHERE id_file=?;", (id_file,))
        self.sqlite_connection.commit()

    def __del__(self):
        self.sqlite_connection.close()
