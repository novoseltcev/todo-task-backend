from typing import List

from app.rest_lib.services import Service
from app.errors import NoSuchEntityError

from .model import Category
from .repository import CategoryRepository


class CategoryService(Service):
    repository: CategoryRepository

    def __init__(self, repository: CategoryRepository = CategoryRepository()):
        super().__init__(repository=repository)

    def get_by_pk(self, user_id: int, name: str) -> Category:
        category = self.repository.get_by_pk(
            self.repository.PrimaryKey(
                user_id=user_id,
                name=name
            )
        )
        if not category:
            raise NoSuchEntityError('Категория не существует.')

        return category

    def get_by_user(self, user_id: int) -> List[Category]:
        return self.repository.get_user_categories(user_id=user_id)

    def create(self, user_id: int, data: dict) -> Category:
        category = Category(user_id=user_id, **data)
        self.repository.insert(category)
        return category

    def edit(self, user_id: int, name: str, data: dict) -> None:
        self.repository.update(
            data=data,
            pk=self.repository.PrimaryKey(
                user_id=user_id,
                name=name
            )
        )

    def delete(self, user_id: int, name: str) -> None:
        self.repository.delete(
            self.repository.PrimaryKey(
                user_id=user_id,
                name=name
            )
        )
