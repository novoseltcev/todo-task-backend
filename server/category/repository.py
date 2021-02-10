# Класс для работы с БД
from sqlalchemy.orm import sessionmaker


class CategoryRepository:
    __default = 'All'

    def __init__(self, engine, model):
        self.session_maker = sessionmaker(bind=engine)
        self.model = model
        session = self.session_maker()
        count = session.query(self.model).count()
        if count == 0:
            self.insert(self.__default)

    def assert_exist(self, id: int):
        session = self.session_maker()
        count = session.query(self.model).filter_by(id=id).count()
        if count == 0:
            raise ValueError(str(self.model.id) + ' = ' + str(id) + " isn't exists")

    def get(self):
        session = self.session_maker()
        return session.query(self.model).all()

    def get_by_name(self, name):
        session = self.session_maker()
        return session.query(self.model).filter_by(name=name).one()

    def insert(self, name: str):
        session = self.session_maker()
        try:
            category = self.model(name=name)
            session.add(category)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def update_name(self, id: int, source: str):
        session = self.session_maker()
        try:
            category = session.query(self.model).filter_by(id=id).one()
            category.change_name(source)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, id: int):
        session = self.session_maker()
        try:
            category = session.query(self.model).filter_by(id=id).one()
            session.delete(category)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e