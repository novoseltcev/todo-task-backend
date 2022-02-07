from abc import abstractmethod
from typing import Tuple

from ...types import CRUD, NotFoundError
from .model import Account


class AccountRepository(CRUD[Account]):
    """Interface of interaction with infrastructure level (ORM, connections, etc.) of the account"""

    @abstractmethod
    def all(self) -> Tuple[Account, ...]:
        """Load all users from the system."""

    @abstractmethod
    def from_name(self, name: str) -> Account:
        """Load account by name from the system.
        :raises NotFoundError: the account is not found by name."""

    @abstractmethod
    def from_email(self, email: str) -> Account:
        """Load account by email from the system.
        :raises NotFoundError: the account is not found by email."""

    @abstractmethod
    def from_token(self, token: str) -> Account:
        """Load account by token from the system.
        :raises NotFoundError: the account is not found by token."""
