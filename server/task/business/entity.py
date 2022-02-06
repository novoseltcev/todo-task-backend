from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Domain entity: task """

    name: str
    description: str
    deadline: date
    category: int
    account: int
    identity: int = ...

    def __hash__(self):
        return hash(self.identity)

    def __eq__(self, other: Task):
        return self.identity == self.identity and self.identity is not None
