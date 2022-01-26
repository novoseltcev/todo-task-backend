from abc import abstractmethod, ABC
from typing import Generic, TypeVar
from server.error import NotFoundError

T = TypeVar('T')


class CRUD(ABC, Generic[T]):
    """Interface of interaction with infrastructure level of the generic."""

    @abstractmethod
    def from_id(self, identity: int) -> T:
        """Load object by himself ID from the system.
        :raises NotFoundError: the object was not found by ID."""

    @abstractmethod
    def insert(self, obj: T) -> int:
        """Create new object from representation.
        :returns: identity of created object.
        :raises NotFoundError: the object can't be created for the transmitted data and external links."""

    @abstractmethod
    def save(self, obj: T) -> None:
        """Update object in the system from representation.
        :raises NotFoundError: the object was not found by passing an ID and immutable references"""

    @abstractmethod
    def remove(self, obj: T) -> None:
        """Delete object from system by himself representation.
        :raises NotFoundError: the object was not found by passing an ID and immutable references"""
