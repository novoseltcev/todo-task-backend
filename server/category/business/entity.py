from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Category:
    """Category business entity"""

    name: str
    account: int
    identity: int = ...
