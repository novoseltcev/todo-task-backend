from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import NoReturn
from werkzeug.security import generate_password_hash, check_password_hash

from .exc import *


class Role(Enum):
    USER = 'user'
    ADMIN = 'admin'
    OWNER = 'owner'


class EmailStatus(Enum):
    NOT_CONFIRMED = 'not_confirmed'
    CONFIRMED = 'confirmed'
    REFUSED = 'refused'


@dataclass
class User:
    """User business-entity.🐙
    Fields:
        name (str): Unique username of the user.
        email (str): User's email address.
        _password (str): Encoded user password.
        _role (Role): The role of the user that determines the levels of access to business logic.
        _email_status (EmailStatus): The status of the user's email, which restricts access to the system only to confirmed users.
        _registration_date (Date, read_only): The date of the user's registration in the system.
    """
    name: str
    email: str
    _password: str
    _role: Role
    _email_status: EmailStatus
    _registration_date: datetime.date
    _id: int = ...

    @property
    def id(self):
        return self._id

    @property
    def password(self):
        return self._password

    @property
    def role(self):
        return self._role

    @property
    def email_status(self):
        return self._email_status

    @property
    def registration_date(self):
        return self._registration_date

    def update_email(self, value: str) -> NoReturn:
        if not re.match(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", value):
            raise EmailError(value)
        self.email = value
        self._email_status = EmailStatus.NOT_CONFIRMED

    def update_password(self, value: str):
        self._password = generate_password_hash(value)

    def check_password(self, value: str) -> NoReturn:
        if not check_password_hash(self.password, value):
            raise PasswordError()

    def check_email_confirm(self) -> NoReturn:
        if self.email_status != EmailStatus.CONFIRMED:
            raise UnconfirmedEmailError(self.email)

    def confirm_email(self) -> NoReturn:
        self._email_status = EmailStatus.CONFIRMED

    def refuse_email(self) -> NoReturn:
        self._email_status = EmailStatus.REFUSED

    def admin_access(self) -> NoReturn:
        if self._role not in (Role.ADMIN, Role.OWNER) or self._email_status != EmailStatus.CONFIRMED:
            raise AdminRequiredError()

    @staticmethod
    def create(name: str, email: str, password: str, role=Role.USER) -> User:
        return User(
            name,
            email,
            generate_password_hash(password),
            role,
            {
                role.USER: EmailStatus.NOT_CONFIRMED,
                role.ADMIN: EmailStatus.REFUSED,
                role.OWNER: EmailStatus.CONFIRMED
            }[role],
            date.today()
        )
