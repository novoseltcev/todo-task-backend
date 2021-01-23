#
# класс SQLiteDB,
# обёрка над БД,
# реализует базовые запросы к БД без знания логики приложения
#
import sqlite3
from server.sql_generator import SQLGenerator


class SQLiteUtility:
    SQL = SQLGenerator()

    def __init__(self, path="server/data/task.db"):
        self.__path = path
        self.__sqlite_connection = sqlite3.connect(self.__path, check_same_thread=False)
        self.__sqlite_connection.row_factory = sqlite3.Row
        self.__cursor = self.__sqlite_connection.cursor()
        self.__execute = self.__cursor.execute
        self.__commit = self.__sqlite_connection.commit

    def create_table(self, table, columns):
        sql = self.SQL.create(table, columns)
        self.__execute(sql)

    def assert_db(self, table, field: str, value: int):
        sql = self.SQL.count(table, field)
        params = (value,)
        self.__execute(sql, params)
        field_count = self.get_data(is_all=False)
        if field_count == 0:
            raise ValueError(field + "=" + str(value) + " isn't exists")

    def get_data(self, is_all=True):
        if is_all:
            return self.__cursor.fetchall()
        return self.__cursor.fetchone()

    def select_all(self, table, filter_column=None, sorted_column=None, value=None, invert_sort=True):
        sql = self.SQL.select(table=table, where=filter_column, order_by=sorted_column, invert_sort=invert_sort)
        if value is None:  # TODO
            self.__execute(sql)
        else:
            self.__execute(sql, value)
        return self.get_data()

    def select_one(self, table, filter_column=None, value=None):
        sql = self.SQL.select(table, where=filter_column)
        if value is None:
            self.__execute(sql)
        else:
            self.__execute(sql, value)
        return self.get_data(is_all=False)

    def insert(self, table, columns, value):
        sql = self.SQL.insert(table, columns)
        self.__execute(sql, value)
        self.__commit()

    def update(self, table, columns, filtered_column, value):
        sql = self.SQL.update(table, columns, filtered_column)
        self.__execute(sql, value)
        self.__commit()

    def delete(self, table, deleting_column, value):
        sql = self.SQL.delete(table, deleting_column)
        self.__execute(sql, value)
        self.__commit()

    def __del__(self):
        self.__sqlite_connection.close()
