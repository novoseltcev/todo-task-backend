from abc import ABC, abstractmethod
from typing import Tuple
from dataclasses import dataclass

from .repository import (
    CategoryRepository,
    Category,
    NotFoundError,
)


@dataclass(frozen=True)
class CategoryInputData:
    """Input DTO to service with contain data of the category"""
    name: str


class CategoryInteractor(ABC):
    """Interface of interaction with category domain logics"""

    def __init__(self, repository: CategoryRepository):
        self.categories = repository

    @abstractmethod
    def get(self, identity: int, account_id: int) -> Category:
        """Getting information about category.
        :raises NotFoundError: the Category by ID associated with the Account was not found."""

    @abstractmethod
    def get_all(self, account_id: int) -> Tuple[Category, ...]:
        """Getting information about Category by Account.
        :raises NotFoundError: the Account was not found."""

    @abstractmethod
    def create(self,  account_id: int, data: CategoryInputData) -> None:
        """Creating new Category in the system.
        :raises NotFoundError: the Account was not found."""

    @abstractmethod
    def update(self, identity: int, account_id: int, data: CategoryInputData) -> None:
        """Updating the Category based on the received data.
        :raises NotFoundError: the Category by ID associated with the Account was not found."""

    @abstractmethod
    def delete(self, identity: int, account_id: int) -> None:
        """Deleting the Category from the system.
        :raises NotFoundError: the Category by ID associated with the Account was not found."""
