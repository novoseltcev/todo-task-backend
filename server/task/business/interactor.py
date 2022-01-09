from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Type, Tuple

from .entity import Task


@dataclass
class TaskInputData:
    """Input DTO to service with contain data of the task"""
    name: str
    description: str
    deadline: date
    id_folder: int


class TaskRepository(ABC):
    """Interface of interaction with infrastructure level of the task"""
    pass


class TaskInteractor(ABC):
    """Interface of interaction with task business logics"""
    def __init__(self, repository: Type[TaskRepository]):
        self.tasks = repository

    @abstractmethod
    def get(self, task_id: int, user_id: int) -> Task:
        """Getting information about task.
        :raises NotFoundError: not found task or user; or the current user isn't task's owner."""
        pass

    @abstractmethod
    def get_recursive(self, task_id: int, user_id: int) -> Task:
        """Getting information about task with recursive getting to folders.
        :raises NotFoundError: not found task or user; or the current user isn't task's owner."""
        pass

    @abstractmethod
    def get_by_folder(self, folder_id: int, user_id: int) -> Tuple[Task, ...]:
        """Get tasks from folder
        :raises NotFoundError: not found folder or user; or the current user isn't folder's owner"""
        pass

    @abstractmethod
    def create(self, user_id: int, data: TaskInputData) -> int:
        """Create new task to user from external data
        """
        pass

    @abstractmethod
    def delete(self, task_id: int, user_id: int) -> None:
        """Delete task by id with user validation
        """
        pass

    @abstractmethod
    def update(self, task_id: int, user_id: int, data: TaskInputData) -> None:
        """Update task by id with user validation"""
        pass
