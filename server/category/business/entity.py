from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Category:
    """Domain entity: category combining tasks"""

    name: str
    account: int
    identity: int = ...

    def __hash__(self):
        return hash(self.identity)

    def __eq__(self, other: Category):
        return self.identity == self.identity and self.identity is not None
