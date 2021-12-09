from abc import ABC, abstractmethod
from typing import NoReturn, List

from server.services.user.schema import UserSchema
from server.services.user.response import UserResponse


class UserInteractor(ABC):
    @classmethod
    @abstractmethod
    def get(cls, schema: UserSchema) -> UserResponse:
        pass

    @classmethod
    @abstractmethod
    def get_all(cls, schema: UserSchema) -> List[UserResponse]:
        pass

    @classmethod
    @abstractmethod
    def update(cls, schema: UserSchema) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, schema: UserSchema) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def register(cls, schema: UserSchema) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def login(cls, schema: UserSchema) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def confirm_email(cls, schema: UserSchema) -> NoReturn:
        pass
