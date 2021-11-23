from abc import ABC, abstractmethod
from typing import Tuple, NoReturn

from .model import File


class Files(ABC):
    @classmethod
    @abstractmethod
    def load(cls, file_id: int) -> File:
        pass

    @classmethod
    @abstractmethod
    def save(cls, file: File) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def load_all(cls) -> Tuple[File]:
        pass

    @classmethod
    @abstractmethod
    def load_by_task(cls, task_id: int) -> Tuple[File]:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, file_id: int) -> NoReturn:
        pass
