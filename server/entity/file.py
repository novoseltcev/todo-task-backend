from dataclasses import dataclass

from user_entity import User


@dataclass(frozen=True)
class File:
    """"""
    name: str
    path: str
    _user: User

    @property
    def user(self):
        return self._user
