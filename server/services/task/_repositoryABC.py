from abc import ABC, abstractmethod
from typing import NoReturn, Tuple

from .model import Task


class Tasks(ABC):
    @classmethod
    @abstractmethod
    def load(cls, task_id: int) -> Task:
        pass

    @classmethod
    @abstractmethod
    def save(cls, task: Task) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def load_all(cls) -> Tuple[Task]:
        pass

    @classmethod
    @abstractmethod
    def load_by_category(cls, category_id: int) -> Tuple[Task]:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, task_id: int) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def check_category(cls, id_category: int) -> NoReturn:
        pass
