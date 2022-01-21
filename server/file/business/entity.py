from __future__ import annotations

import uuid
from dataclasses import dataclass
from functools import lru_cache

from server.task import Task
from server.account import Account


@dataclass(frozen=True)
class File:
    """Business entity: file pinned to task."""
    name: str
    path: str
    task: Task
    identity: int = ...

    @property
    def identity(self):
        return self.identity

    @property
    def task(self):
        return self.task

    class Generator:
        """File's subclass to generate file examples for tests."""

        @staticmethod
        @lru_cache
        def _get(identity: int, account_id: int, task_id: int, name: str, path: str) -> File:
            return File(
                name,
                path,
                Task.Generator.example(task_id, account_id),
                identity
            )

        @classmethod
        @lru_cache
        def example(cls, identity: int, account_id: int, task_id: int) -> File:
            path = f'remote.resource.com/files_bucket/{uuid.uuid4()}.ext'
            return cls._get(identity, account_id, task_id, f'File<{identity}>.ext', path)
