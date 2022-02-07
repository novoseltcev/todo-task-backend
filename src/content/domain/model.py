from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List


@dataclass(frozen=True, unsafe_hash=True)
class ContentOwner:
    reference: str


@dataclass
class Category:
    """Domain aggregator-entity: aggregates content within a single task category."""
    name: str
    color: Optional[str]
    owner: ContentOwner
    reference: str = ...
    tasks: List[Task, ...] = ...

    def __hash__(self):
        return hash(self.reference)

    def __eq__(self, other):
        return self.reference is not None \
               and self.reference == other.reference

    def check_actor(self, actor: ContentOwner):
        if self.owner != actor:
            raise Exception()


class Status(Enum):
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


@dataclass
class Task:
    """Domain entity: associated with Files"""
    title: str
    status: Status
    description: Optional[str]
    deadline: Optional[datetime]
    reference: str = ...
    files: List[File] = ...

    def __hash__(self):
        return hash(self.reference)

    def __eq__(self, other: Task):
        return self.reference is not None \
               and self.reference == other.reference

    def __gt__(self, other: Task):
        return self.remaining_seconds() < other.remaining_seconds()

    def remaining_seconds(self) -> float:
        if self.deadline is None:
            return float('inf')
        return (datetime.now(timezone.utc) - self.deadline).total_seconds()


@dataclass(frozen=True)
class File:
    """Domain entity: pinned to Task."""
    filename: str
    external_path: str
    reference: str = ...
