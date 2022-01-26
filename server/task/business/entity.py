from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from functools import lru_cache


@dataclass(eq=True)
class Task:
    """Task business entity"""
    name: str
    description: str
    deadline: date
    category: int
    account: int
    identity: int = ...

    class Generator:
        """Folder's subclass to generate task examples for tests."""

        @classmethod
        @lru_cache
        def example(cls, identity: int, category_id: int, account_id: int) -> Task:
            return Task(
                f'Task<{identity}>',
                'bla-bla-bla',
                date.fromisocalendar(2023, 1, 1),
                category_id,
                account_id,
                identity
            )
