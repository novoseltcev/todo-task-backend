# Класс для работы с БД
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


from server import DB_session
from server.errors.exc import CategoryUnknownId, CategoryExistName, ForbiddenOperation
from server.index import session_handler
from server.category.model import Category


class CategoryRepository:
    @staticmethod
    def get_by_id(id: int):
        category = Category.query.get(id)
        if category:
            return category
        raise CategoryUnknownId(id)

    @staticmethod
    def get_by_user_id(user_id: int):
        return Category.query.filter_by(user_id=user_id).all()

    @staticmethod
    @session_handler
    def insert(name: str, user_id: int):
        try:
            category = Category(name=name, user_id=user_id)
            DB_session.add(category)
            return category
        except IntegrityError:
            raise CategoryExistName(name)

    @staticmethod
    @session_handler
    def update(schema, user_id):
        id = schema['id']
        try:
            q = Category.query.filter_by(id=id, user_id=user_id)
            q.one()
            q.update(schema)
        except NoResultFound:
            raise CategoryUnknownId(id)

    @classmethod
    @session_handler
    def delete(cls, id: int, user_id: int):
        category = cls.get_by_id(id)
        if category.user_id != user_id:
            raise ForbiddenOperation("")  # TODO
        DB_session.delete(category)
        return category
