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

    class Generator:
        """Folder's subclass to generate task examples for tests."""

        @staticmethod
        @lru_cache
        def _get(task_id: int, folder_id: int, user_id: int,
                 name: str, description: str, deadline: date) -> Task:
            folder = Folder.Generator.example(folder_id, user_id)
            return Task(
                name,
                description,
                deadline,
                folder,
                folder.user,
                task_id
            )

        @classmethod
        @lru_cache
        def example(cls, task_id: int, folder_id: int, user_id: int) -> Task:
            return cls._get(task_id, folder_id, user_id,
                            f'Task<{task_id}>', 'bla-bla-bla', date.fromisocalendar(2022, 1, 1))
