from dataclasses import dataclass

from server.task import Task
from server.user import User


@dataclass(frozen=True)
class File:
    """Business entity: file pinned to task."""
    name: str
    path: str
    _task: Task
    _user: User
    _id: int = ...

    @property
    def id(self):
        return self._id

    @property
    def task(self):
        return self._task

    @property
    def user(self):
        return self._user


