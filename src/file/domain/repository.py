from abc import abstractmethod
from typing import List, ByteString

from ...types import CRUD, NotFoundError
from .entity import File


class FileRepository(CRUD[File]):
    """Interface of interaction with infrastructure level (ORM, connections, etc.) of the file."""

    @abstractmethod
    def from_task(self, task_id: int) -> List[File, ]:
        """Load files by Task ID from the system.
        :raises NotFoundError: the task is not found by ID."""

    @abstractmethod
    def from_account(self, account_id: int) -> List[File, ]:
        """Load files by Account ID from the system.
        :raises NotFoundError: the account is not found by ID."""

    @abstractmethod
    def transfer(self, data: ByteString, metadata: dict[str, str]) -> str:
        """Save data
        :returns: path of saving data
        """
