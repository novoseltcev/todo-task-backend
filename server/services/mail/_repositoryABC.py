from abc import ABC, abstractmethod
from typing import NoReturn
from uuid import UUID

from marshmallow.validate import Email

from .model import Message


class Mails(ABC):
    @staticmethod
    @abstractmethod
    def send(message: Message) -> NoReturn:
        pass

    @classmethod
    def link(cls, email: Email, uuid: UUID):
        pass

    @classmethod
    def get_confirm_mail(cls, email: Email, uuid: UUID) -> Message:
        pass
