from random import choice
from copy import deepcopy, copy
from typing import List, Callable

from mock import Mock
import pytest

from server.folder.business.service import (
    FolderRepository, Folder, User,
    FolderService, FolderInputData,
)
from server.exec.errors import NotFoundError


def folder_id_pred(folder: Folder):
    return folder.id


def user_id_pred(folder: Folder):
    return folder.user.id


list_users = [User.Generator.example(i) for i in range(2)]
list_folders = [Folder.Generator.example(i, list_users[0].id) for i in range(2)]

invalid_folders_id = [
    (-1, choice(list_folders).user),
    (1 + max(list_folders, key=folder_id_pred).id, choice(list_folders).user),
]
invalid_users_id = [
    (choice(list_folders).id, User.Generator.example(-1)),
    (choice(list_folders).id, User.Generator.example(max(list_folders, key=user_id_pred).user.id + 1)),
]

invalid_sets = invalid_folders_id + invalid_users_id


def folders_by_tuple(user: User):
    return filter(lambda folder: folder.user == user, list_folders)


class FakeFolders(FolderRepository, Mock):
    """Mocking repository class to service"""

    def __init__(self):
        super().__init__()
        self.folders = deepcopy(list_folders)

    def from_id(self, folder_id: int) -> Folder:
        return copy(self.contain(lambda folder: folder.id == folder_id)[0])

    def from_user(self, user_id: int) -> List[Folder, ]:
        return deepcopy(self._custom_filter(lambda folder: folder.user.id == user_id))

    def create(self, user_id: int, folder: Folder) -> int:
        newest_id = 1 + max(self.folders, key=lambda _folder: _folder.id, default=-1)
        folder._id = newest_id
        self.folders.append(copy(folder))
        return newest_id

    def update(self, folder: Folder) -> None:
        folder_in_system = self.contain(lambda _folder: _folder.id == folder.id)
        folder_in_system.name = folder.name

    def delete(self, folder: Folder) -> None:
        folder_in_system = self.contain(lambda _folder: _folder.id == folder.id)[0]
        self.folders.remove(folder_in_system)

    def contain(self, pred: Callable):
        result = self._custom_filter(pred)
        if len(result) == 0:
            raise NotFoundError()
        return result

    def _custom_filter(self, pred: Callable):
        return list(filter(pred, self.folders))


@pytest.fixture
def random_folder():
    return choice(list_folders)


@pytest.fixture
def last_id():
    return max(list_folders, key=lambda folder: folder.id)


class TestFolderService:
    """UnitTests to FolderService"""

    def setup_method(self, method):
        self.service = FolderService(FakeFolders)

    @pytest.mark.parametrize(
        'folder_id, user, folder',
        [(folder.id, folder.user, folder) for folder in list_folders])
    def test_get__found(self, folder_id: int, user: User, folder: Folder):
        assert self.service.get(folder_id, user) == folder

    @pytest.mark.parametrize('folder_id, user', invalid_sets)
    def test_get__not_found_error(self, folder_id: int, user: User):
        with pytest.raises(NotFoundError):
            self.service.get(folder_id, user)

    @pytest.mark.parametrize(
        'user, folders_tuple',
        [(user, folders_by_tuple(user)) for user in set(map(lambda folder: folder.user, list_folders))])
    def test_get_all__found(self, user, folders_tuple):
        assert self.service.get_all(user) == folders_tuple

    def test_create__done(self, random_folder, last_folder_id):
        user: User = random_folder.user
        data: FolderInputData = FolderInputData("example")
        assert self.service.create(user, data) == last_folder_id + 1
        folder = self.service.get(last_folder_id + 1, user)
        assert folder.name == data.name

    @pytest.mark.parametrize(
        'folder_id, user, name',
        [(folder.id, folder.user, folder.name) for folder in list_folders] +
        [(folder.id, folder.user, 'new_folder-{i}') for i, folder in enumerate(list_folders)])
    def test_update__done(self, folder_id: int, user: User, name: str):
        data = FolderInputData(name)
        self.service.update(folder_id, user, data)
        folder = self.service.get(folder_id, user)
        assert folder.name == data.name

    @pytest.mark.parametrize('folder_id, user', invalid_sets)
    def test_update__not_found_error(self, folder_id: int, user: User):
        with pytest.raises(NotFoundError):
            self.service.update(folder_id, user, FolderInputData('example'))

    @pytest.mark.parametrize(
        'folder_id, user',
        [(folder.id, folder.user) for folder in list_folders])
    def test_delete__done(self, folder_id: int, user: User):
        self.service.delete(folder_id, user)
        with pytest.raises(NotFoundError):
            self.service.get(folder_id, user)

    @pytest.mark.parametrize('folder_id, user', invalid_sets)
    def test_delete__not_found_error(self, folder_id, user: User):
        with pytest.raises(NotFoundError):
            self.service.delete(folder_id, user)
