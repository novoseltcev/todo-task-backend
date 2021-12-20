from abc import ABC, abstractmethod
from typing import Tuple, NoReturn

from server.services.user.entity import User


class UserRepo(ABC):
    @classmethod
    @abstractmethod
    def load(cls, user_id: int) -> User:
        pass

    @classmethod
    @abstractmethod
    def load_all(cls) -> Tuple[User, ...]:
        pass

    @classmethod
    @abstractmethod
    def load_by_name(cls, name: str) -> User:
        pass

    @classmethod
    @abstractmethod
    def load_by_email(cls, email: str) -> User:
        pass

    @classmethod
    @abstractmethod
    def load_by_uuid(cls, token: int) -> User:
        pass

    @classmethod
    @abstractmethod
    def save(cls, user: User) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, user_id: int) -> NoReturn:
        pass
