from __future__ import annotations
from dataclasses import dataclass, KW_ONLY
from datetime import date
from typing import Optional, List


@dataclass
class Category:
    """Domain entity-aggregator: aggregate Tasks."""
    _: KW_ONLY
    name: str
    color: Optional[str] = ...
    reference: str = ...
    tasks: List[Task, ...] = ...

    def __hash__(self):
        return hash(self.reference)

    def __eq__(self, other):
        return isinstance(other, Category) \
               and self.reference is not None \
               and self.reference == self.reference


@dataclass
class Task:
    """Domain entity: task"""
    _: KW_ONLY
    title: str
    description: str
    deadline: date
    reference: str = ...
    files: List[File] = ...

    def __hash__(self):
        return hash(self.reference)

    def __eq__(self, other: Task):
        return isinstance(other, Task) \
               and self.reference is not None \
               and self.reference == self.reference


@dataclass(frozen=True)
class File:
    """Domain entity: file pinned to task."""
    _: KW_ONLY
    name: str
    path: str
    reference: str = ...
