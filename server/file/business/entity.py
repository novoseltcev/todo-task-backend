from dataclasses import dataclass

from server.user import User


@dataclass(frozen=True)
class File:
    """File pinned to task business entity."""
    name: str
    path: str
    _user: User
    _id: int = ...

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._user
