from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from functools import lru_cache

from server.user import User
from server.folder import Folder


@dataclass(eq=True)
class Task:
    """Task business entity"""
    name: str
    description: str
    deadline: date
    folder: Folder
    _user: User
    _id: int = ...

    @property
    def id(self):
        return self._id

    @property
    def user(self) -> User:
        return self._user

    class Generator:  # TODO - realize
        """Folder's subclass to generate task examples for tests."""

        @staticmethod
        @lru_cache
        def example(task_id: int, user_id: int, *args) -> Task:
            pass
