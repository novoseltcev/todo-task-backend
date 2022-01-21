from abc import ABC, abstractmethod
from typing import List

from .entity import Category


class CategoryRepository(ABC):
    """Interface of interact with infrastructure level (ORM, connections, etc.) of the category."""

    @abstractmethod
    def from_id(self, category_id: int) -> Category:
        """Load category by himself ID from the system.
        :raises NotFoundError: the category was not found by ID."""

    @abstractmethod
    def from_account(self, account_id: int) -> List[Category, ]:
        """Load folders by Account Identity from the system.
        :raises NotFoundError: the account is not found by ID."""

    @abstractmethod
    def insert(self, category: Category) -> int:
        """Create new category from Folder representation and Account ID.
        :raises NotFoundError: the category wasn't found by passing Account ID."""

    @abstractmethod
    def save(self, category: Category) -> None:
        """Update category in the system from Folder representation.
        :raises NotFoundError: the category wasn't found by passing ID and Account ID."""

    @abstractmethod
    def remove(self, category: Category) -> None:
        """Delete category from system by himself representation.
        :raises NotFoundError: the category wasn't found by passing ID and Account ID."""
