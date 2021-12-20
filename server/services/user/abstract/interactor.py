from abc import ABC, abstractmethod
from typing import NoReturn, Tuple
from dataclasses import dataclass

from server.services.user.entity import User


@dataclass(frozen=True)
class UserInputData:
    name:     str = None
    email:    str = None
    password: str = None


class UserInteractor(ABC):
    @classmethod
    @abstractmethod
    def get_account(cls, id: int) -> User:
        """Getting information about user account.
        :param id: unique identifier User in the system.
        :returns: User representation based on ID.
        :raises IDError: the user is not found by ID.
        """
        pass

    @classmethod
    @abstractmethod
    def get_accounts(cls, admin_id: int) -> Tuple[User, ...]:
        """Getting information about user accounts.
            Admin access required!!!
        :param admin_id: unique identifier User in the system.
        :returns: Representation of all users.
        :raises NotFoundError: the user is not found by ID.
        :raises AdminRequiredError: the user does not have access rights.
        """
        pass

    @classmethod
    @abstractmethod
    def update_account(cls, id: int, data: UserInputData) -> NoReturn:
        """Update the user account based on the data received.
        :param id: unique identifier User in the system.
        :param data: contains the user fields to be changed.
        :raises NotFoundError: the user is not found by ID.
        :raises EmailError: email invalid or already in use.
        :raises PasswordError: password invalid.
        :raises NameError: name invalid.
        """
        pass

    @classmethod
    @abstractmethod
    def delete_account(cls, id: int) -> NoReturn:
        """Delete user account from the system
        :param id: unique identifier User in the system.
        :raises NotFoundError: the user is not found by ID.
        """
        pass

    @classmethod
    @abstractmethod
    def register(cls, data: UserInputData) -> NoReturn:
        """Register new user in the system.
        :param data: contains user data for registration.
        :raises EmailError: email invalid or already in use.
        :raises PasswordError: password invalid.
        :raises NameError: name invalid.
        """
        pass

    @classmethod
    @abstractmethod
    def login(cls, data: UserInputData) -> int:
        """Login in the system by email or name
        :param data: contains user data(email or name, password) for authorization.
        :returns: ID of an authorized user.
        :raises LoginError: the user was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the user doesn't confirm email.
        """
        pass

    @classmethod
    @abstractmethod
    def reset_password(cls, uuid: int, password: int) -> NoReturn:
        """Reset user password by uuid with new password.
        :param uuid: a unique public key to confirm the action.
        :param password: a new password by user account.
        :raises NotFoundError: the user is not found by UUID.
        :raises PasswordError: password invalid.
        """
        pass

    @classmethod
    @abstractmethod
    def confirm_email(cls, uuid: int) -> NoReturn:
        """Confirm user email by uuid.
        :param uuid: a unique public key to confirm the action.
        :raises NotFoundError: the user is not found by UUID.
        """
        pass
