from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Type, Tuple, NoReturn

from .entity import Task


@dataclass
class TaskInputData:
    name: str
    description: str
    deadline: date
    id_folder: int


class TaskRepository(ABC):
    pass


class TaskInteractor(ABC):
    def __init__(self, repository: Type[TaskRepository]):
        self.tasks = repository

    @abstractmethod
    def get(self, id: int, user_id: int) -> Task:
        """Get task by id with user validation
        :raises UserValidationException: sda"""
        pass

    @abstractmethod
    def get_recursive(self, id: int, user_id: int) -> Task:
        """"""
        pass

    @abstractmethod
    def get_by_folder(self, folder_id: int) -> Tuple[Task, ...]:
        """Get tasks from folder"""
        pass

    @abstractmethod
    def get_all(self, user_id: int) -> Tuple[Task, ...]:
        """Get all user's tasks"""
        pass

    @abstractmethod
    def create(self, user_id: int, data: TaskInputData) -> NoReturn:
        """Create new Task to user from external data"""
        pass

    @abstractmethod
    def delete(self, id: int, user_id: int) -> NoReturn:
        """Delete task by id with user validation"""
        pass

    @abstractmethod
    def update(self, id: int, user_id: int, data: TaskInputData) -> NoReturn:
        """Update task by id with user validation"""
        pass
