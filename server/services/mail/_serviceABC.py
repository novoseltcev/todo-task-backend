from abc import ABC, abstractmethod
from typing import NoReturn

from .schema import MailSchema


class MailService(ABC):
    @staticmethod
    @abstractmethod
    def notify(schema: MailSchema) -> NoReturn:
        pass

    @staticmethod
    @abstractmethod
    def confirm(schema: MailSchema) -> NoReturn:
        pass
