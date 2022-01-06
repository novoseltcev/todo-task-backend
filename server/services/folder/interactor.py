from abc import ABC, abstractmethod
from typing import Tuple, NoReturn, Type
from dataclasses import dataclass

from .repository import FolderRepository
from server.entity import Folder


@dataclass(frozen=True)
class FolderInputData:
    name: str


class FolderInteractor(ABC):
    def __init__(self, repository: Type[FolderRepository]):
        """Initialization by the repository.
        :param repository: inherited from FolderRepository used to access business-entities.
        """
        self.categories = repository

    @abstractmethod
    def get(self, folder_id: int, user_id: int) -> Folder:
        """Getting information about folder.
        :param folder_id: unique Category identifier.
        :param user_id: unique User identifier.
        :return: Folder representation based on ID.
        :raises NotFoundError: the folder was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the folder.
        """
        pass

    @abstractmethod
    def get_all(self, user_id: int) -> Tuple[Folder, ...]:
        """Getting information about categories.
        :param user_id: unique User identifier.
        :return: all user folders.
        :raises NotFoundError: the folder was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the folder.
        """
        pass

    @abstractmethod
    def create(self, user_id: int, data: FolderInputData) -> NoReturn:
        """Creating new folder in the system.
        :param user_id: unique User identifier.
        :param data: data from which a new folder for tasks is created.
        :raises InvalidUserError: the user was not found by ID.
        """
        pass

    @abstractmethod
    def update(self, folder_id: int, user_id: int, data: FolderInputData) -> NoReturn:
        """Updating the folder based on the received data.
        :param folder_id: unique Category identifier.
        :param user_id: unique User identifier.
        :param data: contains the folder's fields to be changed.
        :raises NotFoundError: the folder was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the folder.
        """
        pass

    @abstractmethod
    def delete(self, folder_id: int, user_id: int) -> NoReturn:
        """Deleting the folder from the system.
        :param folder_id: unique Category identifier.
        :param user_id: unique User identifier.
        :raises NotFoundError: the folder was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the folder.
        """
        pass
