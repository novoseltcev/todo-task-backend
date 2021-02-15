from server.initialize_db import session
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
        try:
            obj = self.model(**kwargs)
            session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return obj

    def _before(self, id: int):
        obj = self._get_by(id=id)
        return obj

    def _delete(self, id: int):
        try:
            obj = self._get_by(id=id)
            session.delete(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return obj

    @staticmethod
    def session_handler(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                session.commit()
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return wrapper
