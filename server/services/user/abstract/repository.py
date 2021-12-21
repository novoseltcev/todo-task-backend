from abc import ABC, abstractmethod
from typing import Tuple, NoReturn

from server.services.user.entity import User


class UserRepo(ABC):
    @classmethod
    @abstractmethod
    def all(cls) -> Tuple[User, ...]:
        """Load all users from the system.
        :returns: Tuple of the User business-entity.
        """
        pass

    @classmethod
    @abstractmethod
    def from_id(cls, id: int) -> User:
        """Load user by id from the system.
        :param id: the ID by which the user is searched in the system.
        :returns: User business-entity.
        :raises NotFoundError: the user is not found by ID.
        """
        pass

    @classmethod
    @abstractmethod
    def from_name(cls, name: str) -> User:
        """Load user by name from the system.
        :param name: the name by which the user is searched in the system.
        :returns: User business-entity.
        :raises NotFoundError: the user is not found by name.
        """
        pass

    @classmethod
    @abstractmethod
    def from_email(cls, email: str) -> User:
        """Load user by email from the system.
        :param email: the email by which the user is searched in the system.
        :returns: User business-entity.
        :raises NotFoundError: the user is not found by email.
        """
        pass

    @classmethod
    @abstractmethod
    def from_uuid(cls, uuid: str) -> User:
        """Load user by uuid from the system.
        :param uuid: the UUID by which the user is searched in the system.
        :returns: User business-entity.
        :raises NotFoundError: the user is not found by UUID.
        """
        pass

    @classmethod
    @abstractmethod
    def create(cls, user: User) -> NoReturn:
        """Create new user from User representation.
        :param user: data for creating a new user
        :raises DataUniqueError: the transmitted data is already contained in the user's unique fields.
        """
        pass

    @classmethod
    @abstractmethod
    def update(cls, id: int, user: User) -> NoReturn:
        """Update user by id from User representation.
        :param id: the ID by which the user is searched in the system.
        :param user: data for updating an existing user.
        :raises NotFoundError: the user is not found by ID.
        :raises DataUniqueError: the transmitted data is already contained in the user's unique fields.
        """
        pass

    @classmethod
    @abstractmethod
    def delete(cls, id: int) -> NoReturn:
        """Delete user by id.
        :param id: the ID by which the user is searched in the system.
        :raises NotFoundError: the user is not found by ID.
        """
        pass
