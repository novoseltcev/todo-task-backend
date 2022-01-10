from abc import ABC, abstractmethod
from typing import Tuple, Type
from dataclasses import dataclass

from .repository import (
    UserRepository,
    User,
)


@dataclass(frozen=True)
class UserInputData:
    """Input DTO to service with contain data of the users"""
    email: str
    password: str
    name: str = ...


class UserInteractor(ABC):
    """Interface of interaction with user business logics"""

    def __init__(self, repository: Type[UserRepository]) -> None:
        self.users = repository()

    @abstractmethod
    def get_account(self, user_id: int) -> User:
        """Getting User's account.
        :raises NotFoundError: the User is not found by ID."""
        pass

    @abstractmethod
    def get_accounts(self, admin_id: int) -> Tuple[User, ...]:
        """Getting User's accounts.
            !!!Admin access required!!!
        :raises NotFoundError: the USer is not found by ID.
        :raises AdminRequiredError: the User does not have access rights."""
        pass

    @abstractmethod
    def update_account(self, user_id: int, data: UserInputData) -> None:
        """Update the User's account based on the data received.
        :raises NotFoundError: the user is not found by ID.
        :raises DataUniqueError: email already in use."""
        pass

    @abstractmethod
    def delete_account(self, user_id: int) -> None:
        """Delete User's account from the system.
        :raises NotFoundError: the User is not found by ID."""
        pass

    @abstractmethod
    def register(self, data: UserInputData) -> None:
        """Register new User in the system.
        :raises DataUniqueError: email or name already in use."""
        pass

    @abstractmethod
    def login_by_name(self, data: UserInputData) -> int:
        """Login in the system by name.
        :raises LoginError: the User was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the User doesn't confirm email."""
        pass

    @abstractmethod
    def login_by_email(self, data: UserInputData) -> int:
        """Login in the system by email.
        :raises LoginError: the User was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the User doesn't confirm email."""
        pass

    @abstractmethod
    def reset_password(self, uuid: str, password: str) -> None:
        """Reset User's password by UUID with new password.
        :raises NotFoundError: the User is not found by UUID."""
        pass

    @abstractmethod
    def confirm_email(self, uuid: str) -> None:
        """Confirm User's email by UUID.
        :raises NotFoundError: the User is not found by UUID."""
        pass
