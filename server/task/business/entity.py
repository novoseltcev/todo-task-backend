from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from typing import Tuple

from server.user import User
from server.file import File


@dataclass
class Task:
    """Task business entity"""
    name: str
    description: str
    deadline: date
    _user: User
    folder_id: int  # In order to avoid recursive dependency and optimize queries to system.
    # Id is selected instead of the folder entity.
    files: Tuple[File, ...] = ...
    _id: int = ...

    @property
    def id(self):
        return self._id

    @property
    def user(self) -> User:
        return self._user

    class Generator:  # TODO - realize
        """Folder's subclass to generate folders examples for tests."""

        @staticmethod
        @lru_cache
        def example(task_id: int, user_id: int, *args) -> Task:
            pass
