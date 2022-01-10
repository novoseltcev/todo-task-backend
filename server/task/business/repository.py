from abc import ABC, abstractmethod
from typing import Tuple

from .entity import Task, Folder, User


class TaskRepository(ABC):
    """Interface of interaction with infrastructure level (ORM, connections, etc.) of the task"""

    @abstractmethod
    def from_id(self, task_id: int) -> Task:
        """Load task by himself ID from the system.
        :raises NotFoundError: the task was not found by ID."""
        pass

    @abstractmethod
    def from_user(self, user_id: int) -> Tuple[Task, ...]:
        """Load tasks by User ID from the system.
        :raises NotFoundError: the user is not found by ID."""
        pass

    @abstractmethod
    def from_folder(self, folder_id: int) -> Tuple[Task, ...]:
        """Load tasks by Folder ID from the system.
        :raises NotFoundError: the folder is not found by ID."""
        pass

    @abstractmethod
    def create(self, user_id: int, task: Task) -> None:
        """Create new task from Task representation and user_id.
        :raises NotFoundError: the task wasn't found by passing User ID."""
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        """Update task in the system from Task representation.
        :raises NotFoundError: the wasn't found by passing ID and User ID."""
        pass

    @abstractmethod
    def delete(self, task: Task) -> None:
        """Delete task from system by himself representation.
        :raises NotFoundError: the task wasn't found by passing ID and User ID."""
        pass
