from typing import NamedTuple

from app.rest_lib.repository import Repository
from .model import Category


class CategoryRepository(Repository):

    class PrimaryKey(NamedTuple):
        user_id: int
        name: str

    model: Category

    def __init__(self):
        super().__init__(model=Category)

    def pk_query(self, pk: PrimaryKey):
        return self.query().filter(
            self.model.user_id == pk.user_id,
            self.model.name == pk.name
        )

    def get_by_pk(self, pk: PrimaryKey):
        return self.pk_query(pk).first()

    def get_user_categories(self, user_id: int):
        return self.query().filter(self.model.user_id == user_id).all()

    def insert(self, entity: Category):
        self.session.add(entity)
        self.session.commit()

    def update(self, pk: PrimaryKey, data: dict):
        self.pk_query(pk).edit(**data)
        self.session.commit()

    def delete(self, pk: PrimaryKey):
        self.pk_query(pk).delete()
        self.session.commit()
