from __future__ import annotations

import uuid
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class File:
    """Business entity: file pinned to task."""
    name: str
    path: str
    task: int
    account: int
    identity: int = ...

    class Generator:
        """File's subclass to generate file examples for tests."""

        @classmethod
        @lru_cache
        def example(cls, identity: int, account_id: int, task_id: int) -> File:
            return File(
                name=f'File<{identity}>.ext',
                path=f'remote.resource.com/files_bucket/{uuid.uuid4()}.ext',
                task=task_id,
                account=account_id,
                identity=identity
            )
