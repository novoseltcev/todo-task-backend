from abc import ABC, abstractmethod
from typing import Tuple, Type
from dataclasses import dataclass

from .repository import (
    AccountRepository,
    Account,
)


@dataclass(frozen=True)
class AccountInputData:
    """Input DTO to service with contain data of the accounts"""
    password: str
    email: str = ...
    name: str = ...


class AccountInteractor(ABC):
    """Interface of interaction with account business logics"""

    def __init__(self, repository: Type[AccountRepository]) -> None:
        self.accounts = repository()

    @abstractmethod
    def get(self, identity: int) -> Account:
        """Getting Account.
        :raises NotFoundError: the User is not found by ID."""

    @abstractmethod
    def get_all(self, admin_identity: int) -> Tuple[Account, ...]:
        """Getting Accounts.
            !!!Admin access required!!!
        :raises NotFoundError: the Account is not found by ID.
        :raises AdminRequiredError: the Account does not have access rights."""

    @abstractmethod
    def update(self, identity: int, data: AccountInputData) -> None:
        """Update the Account based on the data received.
        :raises NotFoundError: the Account is not found by ID.
        :raises DataUniqueError: email already in use."""

    @abstractmethod
    def mark_for_deletion(self, identity: int) -> None:
        """Marks account for deletion.
        :raises NotFoundError: the Account is not found by ID."""

    @abstractmethod
    def delete(self, identity: int) -> None:
        """Delete Account from the system.
        :raises NotFoundError: the Account is not found by ID."""

    @abstractmethod
    def register(self, data: AccountInputData) -> None:
        """Register new Account in the system.
        :raises DataUniqueError: email or name already in use."""

    @abstractmethod
    def login_by_name(self, data: AccountInputData) -> int:
        """Login in the system by name.
        :raises LoginError: the Account was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the Account doesn't confirm email."""

    @abstractmethod
    def login_by_email(self, data: AccountInputData) -> int:
        """Login in the system by email.
        :raises LoginError: the Account was not found to match the transmitted data.
        :raises UnconfirmedEmailError: the Account doesn't confirm email."""

    @abstractmethod
    def reset_password(self, token: str, password: str) -> None:
        """Reset Account's password by token with new password.
        :raises NotFoundError: the Account is not found by token."""

    @abstractmethod
    def confirm_email(self, token: str) -> None:
        """Confirm Account, which founded by token.
        :raises NotFoundError: the Account is not found by token."""
