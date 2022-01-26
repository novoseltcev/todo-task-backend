from abc import abstractmethod
from typing import List

from .entity import Task
from ...types import CRUD


class TaskRepository(CRUD[Task]):
    """Interface of interaction with infrastructure level (ORM, connections, etc.) of the task"""

    @abstractmethod
    def from_account(self, account_id: int) -> List[Task, ]:
        """Load tasks by Account ID from the system.
        :raises NotFoundError: the account is not found by ID."""

    @abstractmethod
    def from_category(self, folder_id: int) -> List[Task, ]:
        """Load tasks by Category ID from the system.
        :raises NotFoundError: the category is not found by ID."""
