from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache

from server.user import User


@dataclass(order=True)
class Folder:
    """Folder business entity"""
    name: str
    _user: User
    _id: int = ...

    @property
    def id(self):
        return self._id

    @property
    def user(self) -> User:
        return self._user

    class Generator:
        """Folder's subclass to generate folders examples for tests."""

        @staticmethod
        @lru_cache
        def get(folder_id: int, name: str, user_id: int) -> Folder:
            return Folder(name, User.Generator.example(user_id), _id=folder_id)

        @classmethod
        @lru_cache
        def example(cls, folder_id: int, user_id: int) -> Folder:
            return cls.get(folder_id, f'folder_{folder_id}', user_id)
