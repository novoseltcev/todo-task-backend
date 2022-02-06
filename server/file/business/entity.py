from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class File:
    """Domain entity: file pinned to task."""

    name: str
    path: str
    task: int
    account: int
    identity: int = ...
