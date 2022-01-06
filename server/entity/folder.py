from dataclasses import dataclass
from typing import Tuple

from .user_entity import User
from .task import Task


@dataclass
class Folder:
    """"""
    name: str
    _user: User
    tasks: Tuple[Task, ...] = ...

    @property
    def user(self) -> User:
        return self._user
