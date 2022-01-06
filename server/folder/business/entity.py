from dataclasses import dataclass
from typing import Tuple

from server.user import User
from server.task.business.entity import Task


@dataclass
class Folder:
    """"""
    name: str
    _user: User
    tasks: Tuple[Task, ...] = ...

    @property
    def user(self) -> User:
        return self._user
