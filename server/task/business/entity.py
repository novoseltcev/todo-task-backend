from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from functools import lru_cache

from server.category import Category


@dataclass(eq=True)
class Task:
    """Task business entity"""
    name: str
    description: str
    deadline: date
    category: Category
    identity: int = ...

    @property
    def identity(self):
        return self.identity

    class Generator:
        """Folder's subclass to generate task examples for tests."""

        @staticmethod
        @lru_cache
        def _get(task_id: int, folder_id: int, user_id: int,
                 name: str, description: str, deadline: date) -> Task:
            return Task(
                name,
                description,
                deadline,
                Category.Generator.example(folder_id, user_id),
                task_id
            )

        @classmethod
        @lru_cache
        def example(cls, task_id: int, folder_id: int, user_id: int) -> Task:
            return cls._get(task_id, folder_id, user_id,
                            f'Task<{task_id}>', 'bla-bla-bla', date.fromisocalendar(2022, 1, 1))
