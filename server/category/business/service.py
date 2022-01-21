from typing import Tuple

from .interactor import (
    CategoryInteractor, CategoryInputData,
    CategoryRepository, Category,
)


class CategoryService(CategoryInteractor):
    """Implementation of the interface for interacting with the Folder's business logic"""

    def get(self, identity: int, account_id: int) -> Category:
        result = self.categories.from_id(identity)
        result.check(account_id)
        return result

    def get_all(self, account_identity: int) -> Tuple[Category, ...]:
        return tuple(self.categories.from_account(account_identity))

    def create(self, account_id: int, data: CategoryInputData) -> None:
        category = Category(data.name, account_id)
        return self.categories.insert(category)

    def update(self, identity: int, account_id: int, data: CategoryInputData) -> None:
        category = self.categories.from_id(identity)
        category.check(account_id)
        category.name = data.name
        self.categories.save(category)

    def delete(self, identity: int, account_id: int) -> None:
        category = self.categories.from_id(identity)
        category.check(account_id)
        self.categories.remove(category)

