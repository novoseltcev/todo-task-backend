class Generator:
    @staticmethod
    def create(table, columns):
        result = "CREATE TABLE IF NOT EXISTS " + table
        result += "(" + ", ".join(columns) + ")"
        return result

    @staticmethod
    def count(table, column, where=True):
        result = "SELECT COUNT(" + column + ") FROM " + table
        if where:
            result += " WHERE " + column + "=?"
        return result

    @staticmethod
    def select(table: str, columns=(), where=None, order_by=None, invert_sort=False):
        result = "SELECT "
        if len(columns) != 0:
            result += ", ".join(columns)
        else:
            result += "*"
        result += " FROM " + table
        if where is not None:
            result += " WHERE " + where + "=?"
        if order_by is not None:
            result += " ORDER BY " + order_by
            if invert_sort:
                result += " DESC"
        return result

    @staticmethod
    def insert(table, columns):
        result = "INSERT INTO " + table
        result += "(" + ", ".join(columns) + ") VALUES (" + "?," * (len(columns) - 1) + "?) "
        return result

    @staticmethod
    def update(table, columns=(), where=None):
        result = "UPDATE " + table
        result += " SET (" + ", ".join(columns) + ")=(" + "?," * (len(columns) - 1) + "?) "
        if where is not None:
            result += " WHERE " + where + "=?"
        return result

    @staticmethod
    def delete(table, where: str):
        result = "DELETE FROM " + table + " WHERE " + where + "=?"
        return result
