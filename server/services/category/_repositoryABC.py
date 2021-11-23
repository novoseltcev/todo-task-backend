from abc import ABC, abstractmethod
from typing import Tuple, NoReturn

from .model import Category


class Categories(ABC):
    @classmethod
    @abstractmethod
    def load(cls, category_id: int) -> Category:
        pass

    @classmethod
    @abstractmethod
    def save(cls, category: Category) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def load_all(cls) -> Tuple[Category]:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, category_id: int) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def load_by_user(cls, id_user: int) -> Tuple[Category]:
        pass
