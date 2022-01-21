from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache

from server.error import NotFoundError


@dataclass(init=True)
class Category:
    """Category business entity"""
    name: str
    account: int
    identity: int = ...

    def check(self, account_id: int):
        if self.account != account_id:
            raise NotFoundError()

    class Generator:
        """Category's subclass to generate category examples for tests."""

        @staticmethod
        @lru_cache
        def get(identity: int, name: str, account_id: int) -> Category:
            print(identity, name, account_id)
            return Category(name=name, account=account_id, identity=identity)

        @classmethod
        @lru_cache
        def example(cls, identity: int, account_id: int) -> Category:
            return cls.get(identity, f'Category<{identity}>', account_id)
