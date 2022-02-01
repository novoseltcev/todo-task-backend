from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Task business entity"""

    name: str
    description: str
    deadline: date
    category: int
    account: int
    identity: int = ...
