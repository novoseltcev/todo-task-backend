from abc import abstractmethod, ABC
from typing import List

from .entity import File, Task


class FileRepository(ABC):
    """Interface of interaction with infrastructure level (ORM, connections, etc.) of the file."""

    @abstractmethod
    def from_id(self, file_identity: int) -> File:
        """Load file by himself ID from the system.
        :raises NotFoundError: the file is not found by ID."""
        pass

    @abstractmethod
    def from_task(self, task_identity: int) -> List[File, ]:
        """Load files by Task ID from the system.
        :raises NotFoundError: the task is not found by ID."""
        pass

    @abstractmethod
    def from_user(self, user_id: int) -> List[File, ]:
        """Load files by User ID from the system.
        :raises NotFoundError: the account is not found by ID."""
        pass

    @abstractmethod
    def create(self, user_id: int, file: File) -> int:
        """Create new file in the system by File representation and User ID.
        :raises NotFoundError: the file wasn't found by passing ID and user_id."""
        pass

    @abstractmethod
    def delete(self, file: File) -> None:
        """Delete file from system by himself representation.
        :raises NotFoundError: the file wasn't found by passing ID and User ID."""
        pass
