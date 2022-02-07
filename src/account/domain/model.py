from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum

from werkzeug.security import generate_password_hash, check_password_hash


class AccessError(Exception):
    """Access is denied"""


class UnconfirmedEmailError(Exception):
    """Trying to access with a non-correct email"""


class PasswordHash:
    """Utils to password hashing"""
    def __init__(self, algorythm: str, salt_length: int):
        self.algorythm = algorythm
        self.salt_length = salt_length

    def generate(self, value: str) -> str:
        return generate_password_hash(value, self.algorythm, self.salt_length)

    def check(self, hash: str, value: str) -> bool:
        return check_password_hash(hash, value)

    @staticmethod
    def make():
        return PasswordHash(
            Config.PASSWORD_HASH_METHO,
            Config.PASSWORD_SALT_LENGTH
        )

@dataclass
class Account:
    """Domain entity: user's account in the system."""
    username: str
    email: str
    password_hash: str
    role: Role
    status: Status
    registration_date: date
    reference: str = ...

    @staticmethod
    def encrypt_password(password: str) -> str:
        return PasswordHash.make().generate(password)

    def cmp_password(self, password: str) -> None:
        if not PasswordHash.make().check(self.password_hash, password):
            raise AccessError()

    def check_access_group(self, group: AccessGroup, msg=None) -> None:
        if self.role not in group:
            raise AccessError(msg)

    def __hash__(self):
        return hash(self.reference)

    def __eq__(self, other: Account):
        return self.reference == self.reference and self.reference is not None


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


class AccessGroup(Enum):
    """Group of roles that define access levels"""
    OWNERS = (Role.OWNER, )
    ADMINS = (*OWNERS, Role.ADMIN)
    USERS = (*ADMINS, Role.USER)
