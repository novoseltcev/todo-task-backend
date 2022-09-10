from typing import List

from app.rest_lib.services import Service
from app.errors import NoSuchEntityError

from .model import Category
from .repository import CategoryRepository, PK


class CategoryService(Service):
    repository: CategoryRepository

    def __init__(self, repository: CategoryRepository = CategoryRepository()):
        super().__init__(repository=repository)
        self.PK = self.repository.PK

    def get_by_pk(self, user_id: int, entity_id: int) -> Category:
        category = self.repository.get_by_pk(PK(user_id=user_id, id=entity_id))
        if not category:
            raise NoSuchEntityError('Категория не существует.')

        return category

    def get_by_user(self, user_id: int) -> List[Category]:
        return self.repository.get_user_categories(user_id=user_id)

    def create(self, user_id: int, data: dict) -> Category.id:
        category = Category(user_id=user_id, **data)
        self.repository.insert(category)
        return category.id

    def edit(self, user_id: int, entity_id: int, data: dict) -> None:
        self.repository.update(PK(user_id=user_id, id=entity_id), data)

    def delete(self, user_id: int, entity_id: int) -> None:
        self.repository.delete(PK(user_id=user_id, id=entity_id))
