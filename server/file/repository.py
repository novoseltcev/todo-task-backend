# Класс для работы с БД
from sqlalchemy.orm import sessionmaker


class FileRepository:

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
        return session.query(self.model).all()

    def get_by_primary(self, id: int):
        session = self.session_maker()
        return session.query(self.model).filter_by(id=id).one()

    def get_by_name(self, name):
        session = self.session_maker()
        return session.query(self.model).filter_by(name=name).one()

    def get_by_foreign(self, task):
        session = self.session_maker()
        return session.query(self.model).filter_by(task=task).all()

    def insert(self, name: str, data, task: int, path: str):
        session = self.session_maker()
        try:
            file = self.model(name=name, path=path, task=task)
            session.add(file)
            file.save(data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def update_task(self, id: int, task: int):
        session = self.session_maker()
        try:
            file = session.query(self.model).filter_by(id=id).one()
            file.task = task
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, id: int):
        session = self.session_maker()
        try:
            file = session.query(self.model).filter_by(id=id).one()
            session.delete(file)
            file.delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
