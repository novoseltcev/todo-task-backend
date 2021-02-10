# Класс для работы с БД
from sqlalchemy.orm import sessionmaker


class TaskRepository:

    def __init__(self, engine, model):
        self.session_maker = sessionmaker(bind=engine)
        self.model = model

    def assert_exist(self, id: int):
        session = self.session_maker()
        count = session.query(self.model).filter_by(id=id).count()
        if count == 0:
            raise ValueError(str(self.model.id) + ' = ' + str(id) + " isn't exists")

    def get(self):
        session = self.session_maker()
        return tuple(reversed(session.query(self.model).all()))

    def get_by_primary(self, id: int):
        session = self.session_maker()
        return session.query(self.model).filter_by(id=id).one()

    def get_by_foreign(self, category: int):
        session = self.session_maker()
        return session.query(self.model).filter_by(category=category).all()

    def insert(self, title: str, category: int):
        session = self.session_maker()
        try:
            task = self.model(title=title, status=False, category=category)
            session.add(task)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def update_title(self, id: int, title: str):
        session = self.session_maker()
        try:
            task = session.query(self.model).filter_by(id=id).one()
            task.change_title(title)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def update_category(self, id: int, category: int):
        session = self.session_maker()
        try:
            task = session.query(self.model).filter_by(id=id).one()
            task.change_category(category)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def update_status(self, id: int):
        session = self.session_maker()
        try:
            task = session.query(self.model).filter_by(id=id).one()
            task.change_status()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, id: int):
        session = self.session_maker()
        try:
            task = session.query(self.model).filter_by(id=id).one()
            session.delete(task)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
