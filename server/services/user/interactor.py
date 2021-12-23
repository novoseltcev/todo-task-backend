from abc import ABC, abstractmethod
from typing import NoReturn, Tuple, Type
from dataclasses import dataclass

from .repository import UserRepository
from .entity import User


@dataclass(frozen=True)
class UserInputData:
    name: str
    email: str
    password: str


class UserInteractor(ABC):
    def __init__(self, repository: Type[UserRepository]):
        """Initialization by the repository.
        :param repository: inherited from UserRepository used to access business-entities.
        """
        self.users = repository

    @abstractmethod
    def get_account(self, id: int) -> User:
        """Getting information about user account.
        :param id: unique User identifier.
        :returns: User representation based on ID.
        :raises NotFoundError: the user is not found by ID.
        """
        pass

    @abstractmethod
    def get_accounts(self, admin_id: int) -> Tuple[User, ...]:
        """Getting information about user accounts.
            Admin access required!!!
        :param admin_id: unique User identifier.
        :returns: Representation of all users.
        :raises NotFoundError: the user is not found by ID.
        :raises AdminRequiredError: the user does not have access rights.
        """
        pass

    @abstractmethod
    def update_account(self, id: int, data: UserInputData) -> NoReturn:
        """Update the user account based on the data received.
        :param id: unique User identifier.
        :param data: contains the user fields to be changed.
        :raises NotFoundError: the user is not found by ID.
        :raises DataUniqueError: email or name already in use.
        """
        pass

    @abstractmethod
    def delete_account(self, id: int) -> NoReturn:
        """Delete user account from the system
        :param id: unique User identifier.
        :raises NotFoundError: the user is not found by ID.
        """
        pass

    @abstractmethod
    def register(self, data: UserInputData) -> NoReturn:
        """Register new user in the system.
        :param data: contains user data for registration.
        :raises EmailError: email invalid or already in use.
        :raises DataUniqueError: email or name already in use.
        """
        pass

    @classmethod
    @abstractmethod
    def login_by_name(cls, data: UserInputData) -> int:
        """Login in the system by email or name
        :param data: contains user data(name, password) for authorization.
        :returns: ID of an authorized user.
        :raises LoginError: the user was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the user doesn't confirm email.
        """
        pass

    @classmethod
    @abstractmethod
    def login_by_email(cls, data: UserInputData) -> int:
        """Login in the system by email or name
        :param data: contains user data(email, password) for authorization.
        :returns: ID of an authorized user.
        :raises LoginError: the user was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the user doesn't confirm email.
        """
        pass

    @classmethod
    @abstractmethod
    def reset_password(cls, uuid: str, password: str) -> NoReturn:
        """Reset user password by uuid with new password.
        :param uuid: a unique public key to confirm the action.
        :param password: a new password by user account.
        :raises NotFoundError: the user is not found by UUID.
        """
        pass

    @classmethod
    @abstractmethod
    def confirm_email(cls, uuid: str) -> NoReturn:
        """Confirm user email by uuid.
        :param uuid: a unique public key to confirm the action.
        :raises NotFoundError: the user is not found by UUID.
        """
        pass

