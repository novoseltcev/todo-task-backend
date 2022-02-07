import contextlib
from abc import abstractmethod, ABC
from typing import Generic, TypeVar

Entity = TypeVar('Entity')


class CRUD(ABC, Generic[Entity]):
    """Interface of interaction with infrastructure level of the generic."""

    @abstractmethod
    @contextlib.contextmanager
    def do_atomic(self):
        pass



    @abstractmethod
    def from_id(self, identity: int) -> Entity:
        """Load object by himself ID from the system.
        :raises NotFoundError: the object was not found by ID."""

    @abstractmethod
    def insert(self, obj: Entity) -> int:
        """Create new object from representation.
        :returns: identity of created object.
        :raises NotFoundError: the object can't be created for the transmitted data and external links."""

    @abstractmethod
    def save(self, obj: Entity) -> None:
        """Update object in the system from representation.
        :raises NotFoundError: the object was not found by passing an ID and immutable references"""

    @abstractmethod
    def remove(self, obj: Entity) -> None:
        """Delete object from system by himself representation.
        :raises NotFoundError: the object was not found by passing an ID and immutable references"""
