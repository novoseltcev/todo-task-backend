# Класс для работы с БД
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


from server import DB_session
from server.errors.exc import CategoryUnknownId, CategoryExistName, ForbiddenOperation
from server.views import session_handler
from server.category.model import Category


class CategoryRepository:
    @staticmethod
    def get_by_id(id_user, id: int):
        category = Category.query.filter_by(id=id, id_user=id_user).first()
        if category:
            return category
        raise CategoryUnknownId(id)

    @staticmethod
    def get_by_user_id(id_user: int):
        return Category.query.filter_by(id_user=id_user).all()

    @staticmethod
    @session_handler
    def insert(id_user, name: str):
        try:
            category = Category(name=name, id_user=id_user)
            DB_session.add(category)
            return category
        except IntegrityError:
            raise CategoryExistName(name)

    @staticmethod
    @session_handler
    def update(id_user, schema):
        id = schema['id']
        try:
            q = Category.query.filter_by(id=id, id_user=id_user)
            q.one()
            q.update(schema)
        except NoResultFound:
            raise CategoryUnknownId(id)

    @classmethod
    @session_handler
    def delete(cls, id_user, id: int, user_id: int):
        category = cls.get_by_id(id_user, id)
        DB_session.delete(category)
        return category
