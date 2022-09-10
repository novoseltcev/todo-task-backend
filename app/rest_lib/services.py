from typing import TypeVar, Iterable, NamedTuple

from .repository import Repository

T = TypeVar('T')


class Page(NamedTuple):
    items: Iterable[T]
    pages: int


class Service:
    def __init__(self, repository: Repository):
        self.repository = repository
