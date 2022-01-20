from copy import copy, deepcopy
from random import choice
from typing import List, Callable

import pytest
from mock import Mock

from server.task.business import (
    TaskService, TaskInputData,
    TaskRepository, Task
)
from server.task.business.entity import User, Folder
from server.exec.errors import NotFoundError

list_users = [User.Generator.example(i) for i in range(2)]
list_folders = [Folder.Generator.example(i, list_users[0].id) for i in range(2)]
list_tasks = [Task.Generator.example(i, list_folders[0].id, list_folders[0].user.id) for i in range(2)]


class FakeTasks(Mock, TaskRepository):
    """Mocked object, which inherited TaskRepository interface."""

    def __init__(self):
        super().__init__()
        self.tasks = deepcopy(list_tasks)

    def from_id(self, task_id: int) -> Task:
        return copy(self.get_by_id(task_id)[0])

    def from_user(self, user_id: int) -> List[Task,]:
        return deepcopy(self.get(lambda task: task.user.id == user_id))

    def from_folder(self, folder_id: int) -> List[Task,]:
        return deepcopy(self.get(lambda task: task.folder.id == folder_id))

    def create(self, user_id: int, task: Task) -> int:
        task._id = self.generate_id()
        self.tasks.append(task)
        return task.id

    def update(self, task: Task) -> None:
        old_task = self.get_by_id(task.id)[0]
        old_task.name = task.name
        old_task.description = task.description
        old_task.deadline = task.deadline
        old_task.folder = task.folder

    def delete(self, task: Task) -> None:
        old_task = self.get_by_id(task.id)[0]
        self.tasks.remove(old_task)

    def generate_id(self):
        return max(self.tasks, key=lambda _task: _task.id).id + 1

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
    def setup_method(self, method):
        self.service = TaskService(FakeTasks)

    @pytest.mark.parametrize('task', list_tasks)
    def test_get__found(self, task):
        assert self.service.get(task.id, task.user) == task

    @pytest.mark.parametrize('task_id', [-1, max(list_tasks, key=lambda task: task.id).id + 1] )
    def test_get__not_found_error(self, task_id):
        with pytest.raises(NotFoundError):
            self.service.get(task_id, choice(list_users))

    @pytest.mark.parametrize('folder', list_folders)
    def test_get_by_folder_found(self, folder):
        expected = tuple(filter(lambda task: task.folder.id == folder.id, list_tasks))
        assert self.service.get_by_folder(folder) == expected

    @pytest.mark.parametrize('folder_id', [-1, max(list_folders, key=lambda folder: folder.id).id + 1])
    def test_get_by_folder__not_found_error(self, folder_id):
        folder = Folder.Generator.example(folder_id, choice(list_users).id)
        with pytest.raises(NotFoundError):
            self.service.get_by_folder(folder)

    @pytest.mark.parametrize('user', list_users)
    def test_get_all__found(self, user):
        user_id = user.id
        expected = tuple(filter(lambda task: task.user.id == user_id, list_tasks))
        assert self.service.get_all(user) == expected

    @pytest.mark.parametrize('user_id', [-1, max(list_users, key=lambda user: user.id).id + 1])
    def test_get_all__not_found_error(self, user_id):
        user = User.Generator.example(user_id)
        with pytest.raises(NotFoundError):
            self.service.get_all(user)

    def test_create__done(self, user, data):
        # user =
        self.service.create(user, data)
