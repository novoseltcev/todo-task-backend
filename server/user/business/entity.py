from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum
from functools import lru_cache

from werkzeug.security import generate_password_hash, check_password_hash


class PasswordHash:  # TODO - add docstring
    @staticmethod
    def generate(value: str) -> str:
        return generate_password_hash(value)

    @staticmethod
    def check(password_hash: str, value: str) -> bool:
        return check_password_hash(password_hash, value)


class Role(Enum):  # TODO - add docstring
    USER = 'user'
    ADMIN = 'admin'
    OWNER = 'owner'


class EmailStatus(Enum):  # TODO - add docstring
    NOT_CONFIRMED = 'not_confirmed'
    CONFIRMED = 'confirmed'
    REFUSED = 'refused'


class UserAccessError(Exception):
    """Exception raises when access is denied"""
    pass


class UnconfirmedEmailError(Exception):
    """Exception raises when trying to access with a non-correct email"""
    pass


class PasswordError(Exception):
    """Exception raises when trying to access with a non-correct password"""
    pass


@dataclass
class User:
    """User business entity.🐙"""
    _name: str
    _email: str
    _password: str
    _role: Role
    _email_status: EmailStatus
    _registration_date: date
    _id: int = ...

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value
        self._unconfirm()

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = PasswordHash.generate(value)

    @property
    def role(self) -> Role:
        return self._role

    @property
    def email_status(self) -> EmailStatus:
        return self._email_status

    def confirm(self):
        self._email_status = EmailStatus.CONFIRMED

    def refuse(self):
        self._email_status = EmailStatus.REFUSED

    def _unconfirm(self):
        self._email_status = EmailStatus.NOT_CONFIRMED

    @property
    def registration_date(self) -> date:
        return self._registration_date

    def check_password(self, value: str):
        if not PasswordHash.check(self._password, value):
            raise PasswordError()

    def check_email(self):
        if self.email_status != EmailStatus.CONFIRMED:
            raise UnconfirmedEmailError(self.email)

    def _is_admin(self) -> bool:
        return self._role == Role.ADMIN

    def _is_owner(self) -> bool:
        return self._role == Role.OWNER

    def admin_access(self):
        self.check_email()
        if not (self._is_admin() or self._is_owner()):
            raise UserAccessError("Required admins to access")

    def owner_access(self):
        if not self._is_owner():
            raise UserAccessError("Required owner to access")

    @property
    def id(self):
        return self._id

    def __eq__(self, value: User) -> bool:
        return self._id == value._id

    @staticmethod
    def create(name: str, email: str, password: str, role=Role.USER) -> User:
        return User(
            name,
            email,
            PasswordHash.generate(password),
            role, {
                role.USER: EmailStatus.NOT_CONFIRMED,
                role.ADMIN: EmailStatus.REFUSED,
                role.OWNER: EmailStatus.CONFIRMED
            }[role],
            date.today()
        )

    class Generator:
        """User's subclass to generate users examples for tests."""

        @staticmethod
        @lru_cache
        def _get(user_id: int, name: str, role: Role, status: EmailStatus) -> User:
            return User(
                name,
                f'{name}@domen.ru',
                PasswordHash.generate(name),
                role,
                status,
                date.today(),
                user_id
            )

        @classmethod
        @lru_cache
        def user(cls, user_id: int, status: EmailStatus) -> User:
            return cls._get(user_id, cls.user.__str__(), Role.USER, status)

        @classmethod
        @lru_cache
        def admin(cls, user_id: int, status: EmailStatus) -> User:
            return cls._get(user_id, cls.admin.__str__(), Role.ADMIN, status)

        @classmethod
        @lru_cache
        def owner(cls, user_id: int, status: EmailStatus) -> User:
            return cls._get(user_id, cls.owner.__str__(), Role.OWNER, status)

        @classmethod
        @lru_cache
        def example(cls, user_id: int) -> User:
            return cls.user(user_id, EmailStatus.CONFIRMED)
