from dataclasses import dataclass


@dataclass
class Folder:
    name: str
    _user_id: int
    _id:  int = ...

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id
