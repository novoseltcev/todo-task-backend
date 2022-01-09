from abc import ABC, abstractmethod
from typing import Tuple, Type
from dataclasses import dataclass

from .repository import FolderRepository
from .entity import Folder


@dataclass(frozen=True)
class FolderInputData:
    """Input DTO to service with contain data of the folder"""
    name: str


class FolderInteractor(ABC):
    """Interface of interaction with folder business logics"""

    def __init__(self, repository: Type[FolderRepository]):
        """Initialization by the repository."""
        self.categories = repository

    @abstractmethod
    def get(self, folder_id: int, user_id: int) -> Folder:
        """Getting information about folder.
        :raises NotFoundError: not found folder or user; or current user isn't folder's owner."""
        pass

    @abstractmethod
    def get_all(self, user_id: int) -> Tuple[Folder, ...]:
        """Getting information about folders.
        :raises NotFoundError: the user was not found."""
        pass

    @abstractmethod
    def create(self, user_id: int, data: FolderInputData) -> None:
        """Creating new folder in the system.
        :raises NotFoundError: the user was not found."""
        pass

    @abstractmethod
    def update(self, folder_id: int, user_id: int, data: FolderInputData) -> None:
        """Updating the folder based on the received data.
        :raises NotFoundError: not found folder or user; or current user isn't folder's owner."""
        pass

    @abstractmethod
    def delete(self, folder_id: int, user_id: int) -> None:
        """Deleting the folder from the system.
        :raises NotFoundError: not found folder or user; or current user isn't folder's owner."""
        pass
