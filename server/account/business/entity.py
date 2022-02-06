from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum

from werkzeug.security import generate_password_hash, check_password_hash


class AccessError(Exception):
    """Access is denied"""


class UnconfirmedEmailError(Exception):
    """Trying to access with a non-correct email"""


@dataclass
class Account:
    """Domain entity: user account in the system."""

    class Status(Enum):
        """Account's statuses."""
        NOT_CONFIRMED = 'not_confirmed'
        CONFIRMED = 'confirmed'
        DELETED = 'deleted'

    class Role(Enum):
        """Account's roles."""
        USER = 'account'
        ADMIN = 'admin'
        OWNER = 'owner'

    name: str
    email: str
    password: str
    role: Role
    status: Status
    registration_date: date
    identity: int = ...

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return PasswordHash.generate(password)

    def check_password(self, password: str) -> None:
        if not PasswordHash.check(self.password, password):
            raise AccessError()

    def check_access_group(self, group: AccessGroup, msg=None) -> None:
        if self.role not in group:
            raise AccessError(msg)

    def __hash__(self):
        return hash(self.identity)

    def __eq__(self, other: Account):
        return self.identity == self.identity and self.identity is not None


class PasswordHash:
    """Utils to password hashing"""
    @staticmethod
    def generate(value: str) -> str:
        return generate_password_hash(value)

    @staticmethod
    def check(password_hash: str, value: str) -> bool:
        return check_password_hash(password_hash, value)


class AccessGroup(Enum):
    """Group of roles that define access levels"""
    OWNERS = (Account.Role.OWNER, )
    ADMINS = (*OWNERS, Account.Role.ADMIN)
    USERS = (*ADMINS, Account.Role.USER)
