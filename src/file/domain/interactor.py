from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, ByteString

from .repository import (
    FileRepository,
    File,
    NotFoundError,
)


@dataclass(frozen=True)
class FileInputData:
    """Input DTO to service with contain data of the file"""
    name: str
    task_id: int = ...
    data: ByteString = ...


class FileInteractor(ABC):
    """Interface of interaction with file domain logics"""

    def __init__(self, repository: FileRepository):
        self.files = repository

    @abstractmethod
    def get(self, identity: int, account_id: int) -> File:
        """Getting File from the system.
        :raises NotFoundError: the File by ID associated with the Account was not found."""

    @abstractmethod
    def get_by_task(self, task_id: int, account_id: int) -> Tuple[File, ...]:
        """Getting all Files containing in the Task.
        :raises NotFoundError: the Task by ID associated with the Account was not found."""

    @abstractmethod
    def get_by_account(self, account_id: int) -> Tuple[File, ...]:
        """Getting all Files for Account.
        :raises NotFoundError: the Account not found"""

    @abstractmethod
    def create_and_pin(self, account_id: int, data: FileInputData) -> int:
        """Create new File to Account from external data.
        :raises NotFoundError: the Task by ID associated with the Account was not found."""

    @abstractmethod
    def unpin_and_delete(self, file_identity: int, account_identity: int) -> None:
        """Deleting File from the system.
        :raises NotFoundError: the File by ID associated with the Account was not found."""
