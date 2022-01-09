from abc import ABC, abstractmethod
from typing import Tuple

from entity import Folder


class FolderRepository(ABC):
    """Interface of interaction with infrastructure level of the folder."""

    @abstractmethod
    def from_id(self, folder_id: int) -> Folder:
        """Load folder by id from the system.
        :raises NotFoundError: the folder was not found by ID."""
        pass

    @abstractmethod
    def from_user(self, user_id: int) -> Tuple[Folder, ...]:
        """Load folders by user from the system.
        :raises NotFoundError: the user is not found by ID."""
        pass

    @abstractmethod
    def create(self, folder: Folder) -> None:
        """Create new folder from Folder representation.
        :raises InvalidUserError: the user wasn't found by ID, or user isn't the folder's owner."""
        pass

    @abstractmethod
    def update(self, folder_id: int, folder: Folder) -> None:
        """Update folder by id from Folder representation.
        :raises NotFoundError: the folder wasn't found by ID or passed user's link is incorrect."""
        pass

    @abstractmethod
    def delete(self, folder_id: int) -> None:
        """Delete folder by id.
        :raises NotFoundError: the folder was not found by ID."""
        pass
