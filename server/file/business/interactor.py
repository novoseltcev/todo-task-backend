from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, Tuple

from .repository import (
    FileRepository,
    File, User, Task,
)


@dataclass(frozen=True)
class FileInputData:
    """Input DTO to service with contain data of the file"""
    name: str


class FileInteractor(ABC):
    """Interface of interaction with file business logics"""

    def __init__(self, repository: Type[FileRepository]):
        self.files = repository

    @abstractmethod
    def get(self, file_id: int, user: User) -> File:
        """Getting File from the system.
        :raises NotFoundError: the File wasn't found or the current User isn't the owner of File."""
        pass

    @abstractmethod
    def get_by_task(self, task: Task) -> Tuple[File, ...]:
        """Getting all Files containing in the Task."""
        pass

    @abstractmethod
    def get_all(self, user: User) -> Tuple[File, ...]:
        """Getting all Files for User."""
        pass

    @abstractmethod
    def pin_and_create(self, user: User, data: FileInputData) -> int:
        """Create new File to User from external data."""
        pass

    @abstractmethod
    def unpin_and_delete(self, file_id: int, user: User) -> None:
        """Deleting File from the system.
        :raises NotFoundError: the File wasn't found or the current User isn't the owner of File."""
        pass
