from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache


@dataclass(init=True)
class Category:
    """Category business entity"""
    name: str
    account: int
    identity: int = ...

    class Generator:
        """Category's subclass to generate category examples for tests."""

        @classmethod
        @lru_cache
        def example(cls, identity: int, account_id: int) -> Category:
            return Category(
                identity=identity,
                name=f'Category<{identity}>',
                account=account_id
            )
