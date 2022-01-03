from abc import ABC, abstractmethod
from typing import Tuple, NoReturn, Type
from dataclasses import dataclass

from .repository import CategoryRepository
from .entity import Category


@dataclass(frozen=True)
class CategoryInputData:
    name: str


class CategoryInteractor(ABC):
    def __init__(self, repository: Type[CategoryRepository]):
        """Initialization by the repository.
        :param repository: inherited from CategoryRepository used to access business-entities.
        """
        self.categories = repository

    @abstractmethod
    def get(self, id: int, user_id: int) -> Category:
        """Getting information about category.
        :param id: unique Category identifier.
        :param user_id: unique User identifier.
        :return: Category representation based on ID.
        :raises NotFoundError: the category was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the category.
        """
        pass

    @abstractmethod
    def get_all(self, user_id: int) -> Tuple[Category, ...]:
        """Getting information about categories.
        :param user_id: unique User identifier.
        :return: all user categories.
        :raises NotFoundError: the category was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the category.
        """
        pass

    @abstractmethod
    def create(self, user_id: int, data: CategoryInputData) -> NoReturn:
        """Creating new category in the system.
        :param user_id: unique User identifier.
        :param data: data from which a new category for tasks is created.
        :raises InvalidUserError: the user was not found by ID.
        """
        pass

    @abstractmethod
    def update(self, id: int, user_id: int, data: CategoryInputData) -> NoReturn:
        """Updating the category based on the received data.
        :param id: unique Category identifier.
        :param user_id: unique User identifier.
        :param data: contains the category's fields to be changed.
        :raises NotFoundError: the category was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the category.
        """
        pass

    @abstractmethod
    def delete(self, id: int, user_id: int) -> NoReturn:
        """Deleting the category from the system.
        :param id: unique Category identifier.
        :param user_id: unique User identifier.
        :raises NotFoundError: the category was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the category.
        """
        pass
