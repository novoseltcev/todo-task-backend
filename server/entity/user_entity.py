from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum

from werkzeug.security import generate_password_hash, check_password_hash


class PasswordHash:
    @staticmethod
    def generate(value: str) -> str:
        return generate_password_hash(value)

    @staticmethod
    def check(password_hash: str, value: str) -> bool:
        return check_password_hash(password_hash, value)


class Role(Enum):
    USER = 'user'
    ADMIN = 'admin'
    OWNER = 'owner'


class EmailStatus(Enum):
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
    """User business-entity.🐙"""
    _name: str
    _email: str
    _password: str
    _role: Role
    _email_status: EmailStatus
    _registration_date: date

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
