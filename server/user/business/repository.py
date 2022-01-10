from abc import ABC, abstractmethod
from typing import Tuple

from .entity import User


class UserRepository(ABC):
    """Interface of interaction with infrastructure level (ORM, connections, etc.) of the user."""

    @abstractmethod
    def all(self) -> Tuple[User, ...]:
        """Load all users from the system."""
        pass

    @abstractmethod
    def from_id(self, user_id: int) -> User:
        """Load user by id from the system.
        :raises NotFoundError: the user is not found by ID."""
        pass

    @abstractmethod
    def from_name(self, name: str) -> User:
        """Load user by name from the system.
        :raises NotFoundError: the user is not found by name."""
        pass

    @abstractmethod
    def from_email(self, email: str) -> User:
        """Load user by email from the system.
        :raises NotFoundError: the user is not found by email."""
        pass

    @abstractmethod
    def from_uuid(self, uuid: str) -> User:
        """Load user by uuid from the system.
        :raises NotFoundError: the user is not found by UUID."""
        pass

    @abstractmethod
    def create(self, user: User) -> None:
        """Create new user from User representation.
        :raises DataUniqueError: data is already contained in the user's unique fields."""
        pass

    @abstractmethod
    def update(self, user_id: int, user: User) -> None:
        """Update user by id from User representation.
        :raises NotFoundError: the user is not found by ID.
        :raises DataUniqueError: transmitted data already contained in the user's unique fields."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        """Delete user by id.
        :raises NotFoundError: the user is not found by ID."""
        pass
