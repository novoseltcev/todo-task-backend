from datetime import date
from enum import Enum
from functools import wraps
from typing import NoReturn, Callable

from werkzeug.security import generate_password_hash, check_password_hash

from .exceptions import *


def authorized(func: Callable) -> Callable:
    @wraps
    def wrapped(self: User, value: str, password: str) -> NoReturn:
        User.check_password(self, password)
        func(self, value)

    return wrapped


class Role(Enum):
    USER = 'user'
    ADMIN = 'admin'
    OWNER = 'owner'


class EmailStatus(Enum):
    NOT_CONFIRMED = 'not_confirmed'
    CONFIRMED = 'confirmed'
    REFUSED = 'refused'


class User:
    """
    User business-entity.\n
    Fields:
        name: str\n
        email: str\n
        password: str\n
        role: Role[USER | ADMIN | OWNER]\n
        registration_date: datetime.date\n
        email_status: EmailStatus
    """

    def __init__(self,
                 name: str,
                 email: str,
                 password: str,
                 registration_date: date,
                 role: Role,
                 email_status: EmailStatus):
        self._name: str = name
        self._email: str = email
        self._password: str = password
        self._role: Role = role
        self._email_status: EmailStatus = email_status
        self._registration_date: date = registration_date

    @property
    def name(self) -> str:
        return self.name

    @name.setter
    def name(self, value: str) -> NoReturn:
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self):
        return self._role

    @property
    def registration_date(self) -> date:
        return self._registration_date

    @property
    def email_status(self) -> EmailStatus:
        return self._email_status

    @authorized
    def change_email(self, value: str) -> NoReturn:
        self._email = value
        self._email_status = EmailStatus.NOT_CONFIRMED

    @authorized
    def change_password(self, value: str) -> NoReturn:
        self._password = generate_password_hash(value)

    def check_password(self, value: str) -> NoReturn:
        if not check_password_hash(self._password, value):
            raise InvalidPasswordError()

    def check_email_confirm(self) -> NoReturn:
        if self.email_status == EmailStatus.confirmed_email:
            raise UnconfirmedEmailError(self.email)

    def confirm_email(self) -> NoReturn:
        self._email_status = EmailStatus.CONFIRMED

    def refuse_email(self) -> NoReturn:
        self._email_status = EmailStatus.REFUSED

    def admin_access(self) -> NoReturn:
        if self.role not in (Role.ADMIN, Role.OWNER):
            raise AdminRequiredError()

    @staticmethod
    def create(name: str, email: str, password: str, role=Role.USER):
        return User(
            name,
            email,
            generate_password_hash(password),
            date.today(),
            role,
            EmailStatus.NOT_CONFIRMED
        )
