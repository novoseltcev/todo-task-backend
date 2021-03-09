# Класс для работы с БД
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


from server import DB_session
from server.errors.exc import CategoryUnknownId, CategoryExistName
from server.index import session_handler
from server.category.model import Category


class CategoryRepository:

    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def get_by_id(id: int):
        category = Category.query.get(id)
        if category:
            return category
        raise CategoryUnknownId(id)

    @staticmethod
    def get_by_name(name: str):
        return Category.query.filter_by(name=name).one()

    @staticmethod
    @session_handler
    def insert(name: str):
        try:
            category = Category(name=name)
            DB_session.add(category)
            return category
        except IntegrityError:
            raise CategoryExistName(name)

    @staticmethod
    @session_handler
    def update(schema):
        id = schema['id']
        try:
            q = Category.query.filter_by(id=id)
            q.one()
            q.update(schema)
        except NoResultFound:
            raise CategoryUnknownId(id)

    @classmethod
    @session_handler
    def delete(cls, id: int):
        category = cls.get_by_id(id)
        DB_session.delete(category)
        return category
