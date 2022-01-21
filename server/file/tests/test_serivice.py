from copy import deepcopy, copy
from random import choice
from typing import Tuple, Callable, List

import pytest
from mock.mock import Mock

from server.file.business import (
    FileService, FileInputData,
    FileRepository, File
)
from server.error.errors import NotFoundError

list_files = [
    File.Generator.example(0, 0, 0),
    File.Generator.example(1, 0, 0)
]


class FakeFiles(Mock, FileRepository):
    """Mocking repository class to service"""

    def __init__(self):
        super().__init__()
        self.folders = deepcopy(list_files)

    def from_id(self, file_id: int) -> File:
        return copy(self.contain(lambda file: file.id == file_id)[0])

    def from_task(self, task_id: int) -> List[File, ]:
        return deepcopy(self._custom_filter(lambda file: file.task.id == task_id))

    def from_user(self, user_id: int) -> List[File, ]:
        return deepcopy(self._custom_filter(lambda file: file.account.id == user_id))

    def create(self, user_id: int, file: File) -> int:
        newest_id = 1 + max(self.files, key=lambda _file: _file.id, default=-1)
        # file._id = newest_id
        self.files.append(copy(file))
        return newest_id

    def delete(self, file: File) -> None:
        pass

    # def create(self, user_id: int, category: File) -> int:
    #     # newest_id = 1 + max(self.folders, key=lambda _folder: _folder.id, default=-1)
    #     # f9i._id = newest_id
    #     # self.folders.append(copy(category))
    #     # return newest_id
    #
    # def update(self, file: File) -> None:
    #     folder_in_system = self.contain(lambda _folder: _folder.id == category.id)
    #     folder_in_system.name = category.name
    #
    # def delete(self, category: Folder) -> None:
    #     folder_in_system = self.contain(lambda _folder: _folder.id == category.id)
    #     self.folders.remove(folder_in_system)

    def contain(self, pred: Callable) -> List[File, ]:
        result = self._custom_filter(pred)
        if len(result) == 0:
            raise NotFoundError()
        return result

    def _custom_filter(self, pred: Callable) -> List[File, ]:
        return list(filter(pred, self.files))


class TestFileService:
    """Test UserService with mocked repository"""

    def setup_method(self, method):
        self.service = FileService(FakeFiles)

    def test_some(self):
        assert self.service
