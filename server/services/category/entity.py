from dataclasses import dataclass


@dataclass
class Category:
    name: str
    _user_id: int
    _id:  int = ...

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id


class Category