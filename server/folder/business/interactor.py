from abc import ABC, abstractmethod
from typing import Tuple, Type
from dataclasses import dataclass

from .repository import (
    FolderRepository,
    Folder, User,
)


@dataclass(frozen=True)
class FolderInputData:
    """Input DTO to service with contain data of the folder"""
    name: str


class FolderInteractor(ABC):
    """Interface of interaction with folder business logics"""

    def __init__(self, repository: Type[FolderRepository]):
        self.categories = repository

    @abstractmethod
    def get(self, folder_id: int, user: User) -> Folder:
        """Getting information about folder.
        :raises NotFoundError: the Folder wasn't found or the current User isn't the owner of Folder."""
        pass

    @abstractmethod
    def get_all(self, user: User) -> Tuple[Folder, ...]:
        """Getting information about folders by User."""
        pass

    @abstractmethod
    def create(self, user: User, data: FolderInputData) -> None:
        """Creating new folder in the system."""
        pass

    @abstractmethod
    def update(self, folder_id: int, user: User, data: FolderInputData) -> None:
        """Updating the folder based on the received data.
        :raises NotFoundError: the Folder wasn't found or the current User isn't the owner of Folder."""
        pass

    @abstractmethod
    def delete(self, folder_id: int, user: User) -> None:
        """Deleting the folder from the system.
        :raises NotFoundError: the Folder wasn't found or the current User isn't the owner of Folder."""
        pass
