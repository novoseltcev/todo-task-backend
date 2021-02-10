from sqlalchemy.orm import sessionmaker


class DBManager:
    def __init__(self, engine, model):
        self.engine = engine
        self.model = model
        self.session_maker = sessionmaker(bind=self.engine)

    def get(self):
        session = self.session_maker()
        return session.query(self.model).all()

    def _get_by(self, all_rows=False, session=None, **kwargs):
        if session is None:
            session = self.session_maker()
        query = session.query(self.model).filter_by(**kwargs)
        if all_rows:
            return query.all()
        return query.one()

    def assert_exist(self, id: int):
        session = self.session_maker()
        query = session.query(self.model).filter_by(id=id)
        if query.count() == 0:
            raise ValueError(str(self.model.id) + ' = ' + str(id) + " isn't exist")

    def _insert(self, **kwargs):
        session = self.session_maker()
        obj = self.model(**kwargs)
        session.add(obj)
        session.commit()
        return obj

    def _before(self, id: int):
        session = self.session_maker()
        obj = self._get_by(id=id, session=session)
        return obj, session

    def _delete(self, id: int):
        obj, session = self._before(id)
        session.delete(obj)
        session.commit()
        return obj
