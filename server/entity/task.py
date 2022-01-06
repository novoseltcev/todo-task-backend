from dataclasses import dataclass
from datetime import date
from typing import Tuple

from user_entity import User
from file import File


@dataclass
class Task:
    """"""
    name: str
    description: str
    deadline: date
    _user: User
    folder_id: int  # In order to avoid recursive dependency and optimize queries to system.
    # Id is selected instead of the folder entity.
    files: Tuple[File, ...] = ...

    @property
    def user(self) -> User:
        return self._user
