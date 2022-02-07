from dataclasses import dataclass
from datetime import date
from typing import Tuple

from src.task.adapters.repository import TaskRepository, Task
from src.error import NotFoundError

@dataclass
class TaskInputData:
    """Input DTO to service with contain data of the task"""
    name: str
    description: str
    deadline: date
    category_id: int = ...


class Service:
    def __init__(self, repository: TaskRepository):
        self.tasks = repository

    def get_task(self, identity: str, account_id: str) -> Task:
        result = self.tasks.from_id(identity)
        if result.account != account_id:
            raise NotFoundError()
        return result

    def add_new_task(self, to_account: int, data: TaskInputData) -> str:
        self.get_category
        task = Task(
            name=data.name,
            description=data.description,
            deadline=data.deadline,
            category=data.category_id,
            account=to_account
        )
        self.tasks.add(task)


class TaskService(TaskInteractor):
    """Implementation of the interface for interacting with the Task's domain logic"""

    def get(self, identity: int, account_id: int) -> Task:
        result = self.tasks.from_id(identity)
        if result.account != account_id:
            raise NotFoundError()
        return result

    def get_by_category(self, category_id: int, account_id: int) -> Tuple[Task, ...]:
        self._external_category(category_id, reaccount_id)
        result = self.tasks.from_category(category_id)
        return result

    def get_by_account(self, account_id: int) -> Tuple[Task, ...]:
        return self.tasks.from_account(account_id)

    def create(self, account_id: int, data: TaskInputData) -> int:
        self._external_category(data.category_id, account_id)
        return self.tasks.insert(
            Task(
                data.name,
                data.description,
                data.deadline,
                data.category_id,
                account_id
            )
        )

    def update(self, identity: int, account_id: int, data: TaskInputData) -> None:
        task = self.get(identity, account_id)
        task.name = data.name
        task.description = data.description
        task.deadline = data.deadline
        self.tasks.save(task)

    def move_to_category(self, identity: int, account_id: int, new_category_id: int):
        category = self._external_category(new_category_id, account_id)
        task = self.get(identity, account_id)
        task.category = category.reference
        self.tasks.save(task)

    def delete(self, identity: int, account_id: int) -> None:
        self.tasks.remove(self.get(identity, account_id))

    @staticmethod
    def _external_category(category_id: int, account_id: int) -> Category:
        return CategoryService().get(category_id, account_id)  # TODO
