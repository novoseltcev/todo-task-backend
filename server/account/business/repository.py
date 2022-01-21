from abc import ABC, abstractmethod
from typing import Tuple

from .entity import Account


class AccountRepository(ABC):
    """Interface of interaction with infrastructure level (ORM, connections, etc.) of the account"""

    @abstractmethod
    def all(self) -> Tuple[Account, ...]:
        """Load all users from the system."""
        pass

    @abstractmethod
    def from_id(self, identity: int) -> Account:
        """Load account by id from the system.
        :raises NotFoundError: the account is not found by ID."""
        pass

    @abstractmethod
    def from_name(self, name: str) -> Account:
        """Load account by name from the system.
        :raises NotFoundError: the account is not found by name."""
        pass

    @abstractmethod
    def from_email(self, email: str) -> Account:
        """Load account by email from the system.
        :raises NotFoundError: the account is not found by email."""
        pass

    @abstractmethod
    def from_token(self, token: str) -> Account:
        """Load account by token from the system.
        :raises NotFoundError: the account is not found by token."""
        pass

    @abstractmethod
    def create(self, account: Account) -> None:
        """Create new account in the system.
        :raises DataUniqueError: data is already contained in the account's unique fields."""
        pass

    @abstractmethod
    def update(self, account: Account) -> None:
        """Update account in the system.
        :raises NotFoundError: the account is not found by ID.
        :raises DataUniqueError: transmitted data already contained in account's unique fields."""
        pass

    @abstractmethod
    def delete(self, account: Account) -> None:
        """Delete account in the system.
        :raises NotFoundError: the account is not found by ID."""
        pass
