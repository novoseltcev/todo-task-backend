from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum
from functools import lru_cache

from werkzeug.security import generate_password_hash, check_password_hash


class PasswordHash:
    """Utils to password hashing"""

    @staticmethod
    def generate(value: str) -> str:
        return generate_password_hash(value)

    @staticmethod
    def check(password_hash: str, value: str) -> bool:
        return check_password_hash(password_hash, value)


class AccessError(Exception):
    """Raises when access is denied"""
    pass


class UnconfirmedEmailError(Exception):
    """Raises when trying to access with a non-correct email"""
    pass


@dataclass(eq=True)
class Account:
    """Account business entity."""

    class Role(Enum):
        """Enum with account's roles in the system"""
        USER = 'account'
        ADMIN = 'admin'
        OWNER = 'owner'

    class Status(Enum):
        """Enum with account status based on email confirmation"""
        NOT_CONFIRMED = 'not_confirmed'
        CONFIRMED = 'confirmed'
        DELETED = 'deleted'

    name: str
    email: str
    password: str
    role: Role
    status: Status
    registration_date: date
    identity: int = ...

    @staticmethod
    def generate_password(password: str) -> str:
        return PasswordHash.generate(password)

    def check_password(self, password: str) -> None:
        if not PasswordHash.check(self.password, password):
            raise AccessError()

    def admin_access(self):
        if self.role not in (self.Role.OWNER, self.Role.ADMIN):
            raise AccessError("Required owner to access")

    def owner_access(self):
        if self.role != self.Role.OWNER:
            raise AccessError("Required owner to access")

    class Generator:
        """User's subclass to generate users examples for tests."""

        @staticmethod
        @lru_cache
        def get(identity: int, name: str, role: Account.Role, status: Account.Status) -> Account:
            return Account(
                name,
                f'{name}@domen.com',
                Account.generate_password(name),
                role,
                status,
                date(2012, 12, 12),
                identity
            )

        @classmethod
        @lru_cache
        def user(cls, identity: int, status: Account.Status) -> Account:
            return cls.get(identity, f'User<{identity}>', Account.Role.USER, status)

        @classmethod
        @lru_cache
        def admin(cls, identity: int, status: Account.Status) -> Account:
            return cls.get(identity, f'Admin<{identity}>', Account.Role.ADMIN, status)

        @classmethod
        @lru_cache
        def owner(cls, identity: int, status: Account.Status) -> Account:
            return cls.get(identity, f'Owner<{identity}>', Account.Role.OWNER, status)

        @classmethod
        @lru_cache
        def example(cls, identity: int) -> Account:
            return cls.user(identity, Account.Status.CONFIRMED)
