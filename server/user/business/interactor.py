from abc import ABC, abstractmethod
from typing import Tuple, Type
from dataclasses import dataclass

from repository import UserRepository
from entity import User


@dataclass(frozen=True)
class UserInputData:
    """Input DTO to service with contain data of the users"""
    name: str
    email: str
    password: str


class UserInteractor(ABC):
    """Interface of interaction with user business logics"""

    def __init__(self, repository: Type[UserRepository]) -> None:
        """Initialization by the repository."""
        self.users = repository

    @abstractmethod
    def get_account(self, user_id: int) -> User:
        """Getting information about user account.
        :raises NotFoundError: the user is not found by ID."""
        pass

    @abstractmethod
    def get_accounts(self, admin_id: int) -> Tuple[User, ...]:
        """Getting information about user accounts.
            !!!Admin access required!!!
        :raises NotFoundError: the user is not found by ID.
        :raises AdminRequiredError: the user does not have access rights."""
        pass

    @abstractmethod
    def update_account(self, user_id: int, data: UserInputData) -> None:
        """Update the user account based on the data received.
        :raises NotFoundError: the user is not found by ID.
        :raises DataUniqueError: email or name already in use."""
        pass

    @abstractmethod
    def delete_account(self, user_id: int) -> None:
        """Delete user account from the system.
        :raises NotFoundError: the user is not found by ID."""
        pass

    @abstractmethod
    def register(self, data: UserInputData) -> None:
        """Register new user in the system.
        :raises EmailError: email invalid or already in use.
        :raises DataUniqueError: email or name already in use."""
        pass

    @classmethod
    @abstractmethod
    def login_by_name(cls, data: UserInputData) -> int:
        """Login in the system by email or name.
        :raises LoginError: the user was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the user doesn't confirm email."""
        pass

    @classmethod
    @abstractmethod
    def login_by_email(cls, data: UserInputData) -> int:
        """Login in the system by email or name.
        :raises LoginError: the user was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the user doesn't confirm email."""
        pass

    @classmethod
    @abstractmethod
    def reset_password(cls, uuid: str, password: str) -> None:
        """Reset user password by uuid with new password.
        :raises NotFoundError: the user is not found by UUID."""
        pass

    @classmethod
    @abstractmethod
    def confirm_email(cls, uuid: str) -> None:
        """Confirm user email by uuid.
        :raises NotFoundError: the user is not found by UUID."""
        pass
