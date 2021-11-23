from abc import ABC, abstractmethod

from .schema import UserSchema
from .response import UserResponse


class UserService(ABC):
    @classmethod
    @abstractmethod
    def get(cls, schema: UserSchema) -> UserResponse:
        pass

    @classmethod
    @abstractmethod
    def get_all(cls, schema: UserSchema) -> UserResponse:
        pass

    @classmethod
    @abstractmethod
    def create(cls, schema: UserSchema) -> UserResponse:
        pass

    @classmethod
    @abstractmethod
    def login(cls, schema: UserSchema) -> UserResponse:
        pass

    @classmethod
    @abstractmethod
    def edit(cls, schema: UserSchema) -> UserResponse:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, schema: UserSchema) -> UserResponse:
        pass

    @classmethod
    @abstractmethod
    def confirm_email(cls, schema: UserSchema) -> UserResponse:
        pass
