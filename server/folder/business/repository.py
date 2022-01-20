from abc import ABC, abstractmethod
# from typing import List
from typing import List

from .entity import Folder, User


class FolderRepository(ABC):
    """Interface of interaction with infrastructure level (ORM, connections, etc.) of the folder."""

    @abstractmethod
    def from_id(self, folder_id: int) -> Folder:
        """Load folder by himself ID from the system.
        :raises NotFoundError: the folder was not found by ID."""
        pass

    @abstractmethod
    def from_user(self, user_id: int) -> List[Folder, ]:
        """Load folders by User ID from the system.
        :raises NotFoundError: the user is not found by ID."""
        pass

    @abstractmethod
    def create(self, user_id: int, folder: Folder) -> int:
        """Create new folder from Folder representation and User ID.
        :raises NotFoundError: the folder wasn't found by passing User ID."""
        pass

    @abstractmethod
    def update(self, folder: Folder) -> None:
        """Update folder in the system from Folder representation.
        :raises NotFoundError: the folder wasn't found by passing ID and User ID."""
        pass

    @abstractmethod
    def delete(self, folder: Folder) -> None:
        """Delete folder from system by himself representation.
        :raises NotFoundError: the folder wasn't found by passing ID and User ID."""
        pass
