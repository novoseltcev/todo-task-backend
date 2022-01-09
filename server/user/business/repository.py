from abc import ABC, abstractmethod
from typing import Tuple, NoReturn

from entity import User


class UserRepository(ABC):
    """Interface of interaction with infrastructure level of the user."""

    @classmethod
    @abstractmethod
    def all(cls) -> Tuple[User, ...]:
        """Load all users from the system."""
        pass

    @classmethod
    @abstractmethod
    def from_id(cls, user_id: int) -> User:
        """Load user by id from the system.
        :raises NotFoundError: the user is not found by ID."""
        pass

    @classmethod
    @abstractmethod
    def from_name(cls, name: str) -> User:
        """Load user by name from the system.
        :raises NotFoundError: the user is not found by name."""
        pass

    @classmethod
    @abstractmethod
    def from_email(cls, email: str) -> User:
        """Load user by email from the system.
        :raises NotFoundError: the user is not found by email."""
        pass

    @classmethod
    @abstractmethod
    def from_uuid(cls, uuid: str) -> User:
        """Load user by uuid from the system.
        :raises NotFoundError: the user is not found by UUID."""
        pass

    @classmethod
    @abstractmethod
    def create(cls, user: User) -> NoReturn:
        """Create new user from User representation.
        :raises DataUniqueError: data is already contained in the user's unique fields."""
        pass

    @classmethod
    @abstractmethod
    def update(cls, user_id: int, user: User) -> NoReturn:
        """Update user by id from User representation.
        :raises NotFoundError: the user is not found by ID.
        :raises DataUniqueError: transmitted data already contained in the user's unique fields."""
        pass

    @classmethod
    @abstractmethod
    def delete(cls, user_id: int) -> NoReturn:
        """Delete user by id.
        :raises NotFoundError: the user is not found by ID."""
        pass
