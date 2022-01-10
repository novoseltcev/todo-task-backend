from typing import Tuple

from .interactor import (
    TaskInteractor, TaskInputData,
    TaskRepository, Task, User, Folder
)


class TaskService(TaskInteractor):  # TODO - realize working interface
    """Implementation of the interface for interacting with the Task's business logic"""

    def get(self, task_id: int, user: User) -> Task:
        pass

    def get_by_folder(self, folder: Folder) -> Tuple[Task, ...]:
        pass

    def get_all(self, user: User) -> Tuple[Task, ...]:
        pass

    def create(self, user: User, data: TaskInputData) -> int:
        pass

    def move_to_folder(self, task_id: int, folder: Folder):
        pass

    def update(self, task_id: int, user: User, data: TaskInputData) -> None:
        pass

    def delete(self, task_id: int, user: User) -> None:
        pass
