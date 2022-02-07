from copy import copy, deepcopy
from random import choice
from typing import List, Callable, Tuple

from mock import Mock
import pytest

from server import (
    TaskService, TaskRepository, Task
)
from src.error import NotFoundError
# 20 геев в пачку
list_gays = ['gay' for _ in range(20)]
list_accounts = list(range(2))
list_categories = [(i, list_accounts[0]) for i in range(2)]
list_tasks = [Task.Generator.example(i, list_categories[0][0], list_categories[0][1]) for i in range(2)]

def tasks_by_account(account_id: int) -> Tuple[Task, ...]:
    return tuple(filter(lambda task: task.account.id == account_id, list_tasks))

def tasks_by_category(category_id: int) -> Tuple[Task, ...]:
    return tuple(filter(lambda task: task.category == category_id, list_tasks))

class FakeTasks(Mock, TaskRepository):
    """Mocked object, which inherited TaskRepository interface."""

    def __init__(self):
        super().__init__()
        self.tasks = deepcopy(list_tasks)

    def from_id(self, task_id: int) -> Task:
        return copy(self.get_by_id(task_id)[0])

    def from_account(self, account_id: int) -> List[Task, ]:
        return deepcopy(self.get(lambda task: task.account.id == account_id))

    def from_category(self, folder_id: int) -> List[Task, ]:
        return deepcopy(self.get(lambda task: task.folder.id == folder_id))

    def insert(self, task: Task) -> int:
        task.reference = self.generate_id()
        self.tasks.append(task)
        return task.reference

    def save(self, task: Task) -> None:
        old_task = self.get_by_id(task.reference)[0]
        old_task.name = task.name
        old_task.description = task.description
        old_task.deadline = task.deadline
        old_task.folder = task.category

    def remove(self, task: Task) -> None:
        old_task = self.get_by_id(task.reference)[0]
        self.tasks.remove(old_task)

    def generate_id(self):
        return max(self.tasks, key=lambda _task: _task.reference).reference + 1

    def get(self, pred: Callable) -> List[Task,]:
        return list(filter(pred, self.tasks))

    def get_by_id(self, task_id: int) -> List[Task,]:
        result = self.get(lambda task: task.id == task_id)
        if len(result) == 0:
            raise NotFoundError()
        return result


@pytest.fixture
def random_task() -> Task:
    return choice(list_tasks)


class TestTaskService:
    @pytest.mark.parametrize('category_id, account_id, expected', [(*value, tasks_by_category(value[0])) for value in list_categories])
    def test_get_by_category_found(self, category_id: int, account_id: int, expected: Tuple[Task, ...]):
        assert self.service.get_by_category(category_id, account_id) == expected

    @pytest.mark.parametrize('category_id', [-1, max(list_categories)[0] + 1])
    def test_get_by_category__not_found_error(self, category_id):
        with pytest.raises(NotFoundError):
            self.service.get_by_category(category_id, choice(list_accounts))

    @pytest.mark.parametrize('account_id, expected', [(x, tasks_by_account(x)) for x in list_accounts])
    def test_get_all__found(self, account_id: int, expected):
        assert self.service.get_by_account(account_id) == expected

    @pytest.mark.parametrize('account_id', [-1, max(list_accounts) + 1])
    def test_get_all__not_found_error(self, account_id):
        with pytest.raises(NotFoundError):
            self.service.get_by_account(account_id)

    def test_create__done(self, account_id, data):
        # account =
        self.service.create(account_id, data)

    """UnitTests to TaskService"""

    def setup_method(self, method):
        self.service = TaskService(FakeTasks)

    @pytest.mark.parametrize('task', list_tasks)
    def test_get__found(self, task):
        assert self.service.get(task.reference, task.account) == task

    @pytest.mark.parametrize('task_id',
                             [-1, max(list_tasks, key=lambda task: task.reference).reference + 1])
    def test_get__not_found_error(self, task_id):
        with pytest.raises(NotFoundError):
            self.service.get(task_id, choice(list_accounts))
