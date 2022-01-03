from abc import ABC, abstractmethod
from typing import NoReturn, Tuple

from .entity import Category


class CategoryRepository(ABC):
    @abstractmethod
    def from_id(self, id: int) -> Category:
        """Load category by id from the system.
        :param id: the ID by which the category is searched in the system.
        :return: Category business-entity.
        :raises NotFoundError: the category was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the category.
        """
        pass

    @abstractmethod
    def from_user(self, user_id: int) -> Tuple[Category, ...]:
        """Load categories by user from the system.
        :param user_id: the user ID by which the categories searched in the system.
        :return: Category business-entities.
        :raises NotFoundError: the user is not found by ID.
        """
        pass

    @abstractmethod
    def create(self, category: Category) -> NoReturn:
        """Create new category from Category representation.
        :param category: data for creating a new category.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the category.
        :raises DataUniqueError: the transmitted data is already contained in unique category fields.
        """
        pass

    @abstractmethod
    def update(self, id: int, category: Category) -> NoReturn:
        """Update category by id from Category representation.
        :param id: the ID by which the category is searched in the system.
        :param category: data for updating an existing category.
        :raises NotFoundError: the category was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the category.
        :raises DataUniqueError: the transmitted data is already contained in unique category fields.
        """
        pass

    @abstractmethod
    def delete(self, id: int) -> NoReturn:
        """Delete category by id.
        :param id: the ID by which the category is searched in the system.
        :raises NotFoundError: the category was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the category.
        """
        pass
