from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Type, Tuple

from .repository import TaskRepository, Task, Folder, User


@dataclass
class TaskInputData:
    """Input DTO to service with contain data of the task"""
    name: str
    description: str
    deadline: date


class TaskInteractor(ABC):
    """Interface of interaction with task business logics"""

    def __init__(self, repository: Type[TaskRepository]):
        self.tasks = repository

    @abstractmethod
    def get(self, task_id: int, user: User) -> Task:
        """Getting Task from system.
        :raises NotFoundError: the Task wasn't found or the current User isn't the owner of Task."""
        pass

    @abstractmethod
    def get_by_folder(self, folder: Folder) -> Tuple[Task, ...]:
        """Get tasks from folder."""
        pass

    @abstractmethod
    def get_all(self, user: User) -> Tuple[Task, ...]:
        """Get tasks for user."""
        pass

    @abstractmethod
    def create(self, user: User, data: TaskInputData) -> int:
        """Create new Task to User from external data."""
        pass

    @abstractmethod
    def move_to_folder(self, task_id: int, folder: Folder):
        """Move Task to another Folder.
        :raises NotFoundError: the Task wasn't found or the Folder's user isn't the owner of Task"""
        pass

    @abstractmethod
    def update(self, task_id: int, user: User, data: TaskInputData) -> None:
        """Updating Task in the system by received data.
        :raises NotFoundError: the Task wasn't found or the current User isn't the owner of Task."""
        pass

    @abstractmethod
    def delete(self, task_id: int, user: User) -> None:
        """Deleting Task from the system.
        :raises NotFoundError: the Task wasn't found or the current User isn't the owner of Task."""
        pass
