from typing import Tuple

from .interactor import (
    TaskInteractor, TaskInputData,
    TaskRepository, Task, Account, Category
)


class TaskService(TaskInteractor):  # TODO - realize working interface
    """Implementation of the interface for interacting with the Task's business logic"""

    def get(self, task_id: int, user: Account) -> Task:
        pass

    def get_by_category(self, folder: Category) -> Tuple[Task, ...]:
        pass

    def get_all(self, user: Account) -> Tuple[Task, ...]:
        pass

    def create(self, folder: Category, data: TaskInputData) -> int:
        pass

    def move_to_folder(self, task_id: int, folder: Category):
        pass

    def update(self, task_id: int, folder: Category, data: TaskInputData) -> None:
        pass

    def delete(self, task_id: int, user: Account) -> None:
        pass
