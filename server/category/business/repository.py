from abc import abstractmethod
from typing import List

from ...types import CRUD, NotFoundError
from .entity import Category


class CategoryRepository(CRUD[Category]):
    """Interface of interact with infrastructure level (ORM, connections, etc.) of the category."""

    @abstractmethod
    def from_account(self, account_id: int) -> List[Category, ]:
        """Load folders by Account Identity from the system.
        :raises NotFoundError: the account is not found by ID."""
