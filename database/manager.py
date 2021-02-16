from server.initialize_db import DB_session


class DBManager:
    def __init__(self, model):
        self.model = model

    def get(self):
        return self.model.query.all()

    def _get_by(self, all_rows=False, **kwargs):
        query = self.model.query.filter_by(**kwargs)
        if all_rows:
            return query.all()
        return query.one()

    def assert_exist(self, id: int):
        query = self.model.query.filter_by(id=id)
        if query.count() == 0:
            raise ValueError(str(self.model.id) + ' = ' + str(id) + " isn't exist")

    def _insert(self, **kwargs):
        DB_session.add(self.model(**kwargs))

    def _delete(self, id: int):
        DB_session.delete(self._get_by(id=id))

    @staticmethod
    def session_handler(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                DB_session.commit()
            except Exception as e:
                DB_session.rollback()
                raise e
        return wrapper
