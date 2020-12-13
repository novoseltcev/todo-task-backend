import sqlite3
from flask import abort
from server.istorage import IStorage


class SQLiteDB(IStorage):
    def __init__(self, path="server/data"):
        super().__init__(path)
        self.path = path + "/tasks.db"
        self.sqlite_connection = sqlite3.connect(self.path, check_same_thread=False)
        self.sqlite_connection.row_factory = sqlite3.Row
        self.cursor = self.sqlite_connection.cursor()
        self.create_tables()

    def __del__(self):
        self.sqlite_connection.close()

    def append_task(self, title_task: str):
        self.cursor.execute("""INSERT INTO tasks (title, status, id_category) VALUES (?, FALSE, ?)""", (title_task, self.current_category,))
        self.sqlite_connection.commit()
        return self.cursor.fetchall()

    def append_category(self, category: str):
        self.cursor.execute("""INSERT INTO categories (name_category) VALUES (?);""", (category,))
        self.sqlite_connection.commit()
        return self.cursor.fetchall()

    def update_task_status(self, task_id: int):
        self.cursor.execute("""SELECT status FROM tasks WHERE id_task = ?;""", (task_id,))
        prev_status = (self.cursor.fetchone()[0] + 1) % 2
        self.cursor.execute(f"""UPDATE OR ABORT tasks SET status={prev_status} WHERE id_task=?;""", (task_id,))
        self.sqlite_connection.commit()
        return self.cursor.fetchall()

    def update_task_category(self, task_id: int, category: str):
        self.cursor.execute(f"""UPDATE OR ABORT tasks SET id_category=(SELECT id FROM categories WHERE name_category={category}) WHERE id_task=?;""", (task_id,))
        self.sqlite_connection.commit()
        return self.cursor.fetchall()

    def remove_task(self, task_id: int):
        self.cursor.execute("""DELETE FROM tasks WHERE id_task = ?;""", (task_id,))

    def remove_category(self, category: str):
        self.cursor.execute("""DELETE FROM categories WHERE name_category = ?;""", (category,))

    def rename_category(self, destination: str, source: str):
        self.cursor.execute(f"""UPDATE OR ABORT categories SET name_category={source} WHERE name_category=?;""", (destination,))
        self.sqlite_connection.commit()
        return self.cursor.fetchall()

    def get_filtered_tasks(self):
        # print(self.current_category)
        if self.current_category != self._default:
            self.cursor.execute("""SELECT id FROM categories WHERE name_category=?""", self.current_category)
            cur_category = self.cursor.fetchone()
            self.cursor.execute("""SELECT * FROM tasks WHERE id_category=? ORDER BY id_task DESC ;""", cur_category)
        else:
            self.cursor.execute("SELECT * FROM tasks ORDER BY id_task DESC ;")
        return self.cursor.fetchall()

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories WHERE id <> 1;")
        return self.cursor.fetchall()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS categories (id INTEGER, name_category varchar(20) UNIQUE, PRIMARY KEY(id));""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (id_task INTEGER, title VARCHAR(20), status INTEGER , id_category INTEGER, PRIMARY KEY(id_task), FOREIGN KEY(id_category) REFERENCES categories(id));""")
        self.cursor.execute("""SELECT COUNT(name_category) FROM categories""")
        categories_count = self.cursor.fetchone()
        if categories_count == (0,):
            self.append_category(self._default)
