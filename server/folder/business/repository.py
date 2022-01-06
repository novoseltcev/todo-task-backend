from abc import ABC, abstractmethod
from typing import NoReturn, Tuple

from .entity import Folder


class FolderRepository(ABC):
    @abstractmethod
    def from_id(self, folder_id: int) -> Folder:
        """Load folder by id from the system.
        :param folder_id: the ID by which the folder is searched in the system.
        :return: Folder business-entity.
        :raises NotFoundError: the folder was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the folder.
        """
        pass

    @abstractmethod
    def from_user(self, user_id: int) -> Tuple[Folder, ...]:
        """Load folders by user from the system.
        :param user_id: the user ID by which the folders searched in the system.
        :return: Folder business-entities.
        :raises NotFoundError: the user is not found by ID.
        """
        pass

    @abstractmethod
    def create(self, folder: Folder) -> NoReturn:
        """Create new folder from Folder representation.
        :param folder: data for creating a new folder.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the folder.
        :raises DataUniqueError: the transmitted data is already contained in unique folder fields.
        """
        pass

    @abstractmethod
    def update(self, folder_id: int, folder: Folder) -> NoReturn:
        """Update folder by id from Folder representation.
        :param folder_id: the ID by which the folder is searched in the system.
        :param folder: data for updating an existing folder.
        :raises NotFoundError: the folder was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the folder.
        :raises DataUniqueError: the transmitted data is already contained in unique folder fields.
        """
        pass

    @abstractmethod
    def delete(self, folder_id: int) -> NoReturn:
        """Delete folder by id.
        :param folder_id: the ID by which the folder is searched in the system.
        :raises NotFoundError: the folder was not found by ID.
        :raises InvalidUserError: the user was not found by ID, or the current user is not the owner of the folder.
        """
        pass
