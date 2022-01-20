from __future__ import annotations

import uuid
from dataclasses import dataclass
from functools import lru_cache

from server.task import Task
from server.user import User


@dataclass(frozen=True)
class File:
    """Business entity: file pinned to task."""
    name: str
    path: str
    _task: Task
    _id: int = ...

    @property
    def id(self):
        return self._id

    @property
    def task(self):
        return self._task

    class Generator:
        """File's subclass to generate file examples for tests."""

        @staticmethod
        @lru_cache
        def _get(file_id: int, user_id: int, task_id: int, name: str, path: str) -> File:
            return File(
                name,
                path,
                Task.Generator.example(task_id, user_id),
                file_id
            )

        @classmethod
        @lru_cache
        def example(cls, file_id: int, user_id: int, task_id: int) -> File:
            path = f'remote.resource.com/files_bucket/{uuid.uuid4()}.ext'
            return cls._get(file_id, user_id, task_id, f'File<{file_id}>.ext', path)
