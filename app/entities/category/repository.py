from app.rest_lib.repository import Repository, NamedTuple
from .model import Category


class PK(NamedTuple):
    id: int
    user_id: int


class CategoryRepository(Repository):
    model: Category

    def __init__(self):
        super().__init__(model=Category)

    def get_by_pk(self, pk: PK) -> Category:
        return self.pk_query(pk).first()

    def get_user_categories(self, user_id: int):
        return self.query().filter(self.model.user_id == user_id).all()

    def insert(self, entity: Category):
        self.session.add(entity)
        self.session.commit()

    def update(self, pk: PK, data: dict):
        self.pk_query(pk).update(data)
        self.session.commit()

    def delete(self, pk: PK):
        self.pk_query(pk).delete()
        self.session.commit()
