import random
from contextlib import contextmanager
from typing import NoReturn, Tuple

import pytest
from mock import Mock

from server.exec import *
from server.folder.business import *


def folders():
    return [
        Folder.Generator.example(folder_id=0, user_id=1),
        Folder.Generator.example(folder_id=1, user_id=0),
    ]


def id_folders() -> Tuple[int, ...]:
    return tuple(map(lambda folder: folder.id, folders()))


class FoldersMock(FolderRepository, Mock):
    max_id = max(id_folders())

    def from_id(self, folder_id: int) -> Folder:
        self.contain_id(folder_id)
        return self.filter_id(folder_id)[-1]

    def from_user(self, user_id: int) -> Tuple[Folder, ...]:
        self.contain_user(user_id)
        return self.filter_user(user_id)

    def create(self, folder: Folder) -> int:
        self.unique(folder)
        self.max_id += 1
        return self.max_id

    def update(self, folder_id: int, folder: Folder) -> None:
        self.contain_id(folder_id)

    def delete(self, folder_id: int) -> None:
        self.contain_id(folder_id)

    def contain_id(self, folder_id: int) -> NoReturn:
        if len(self.filter_id(folder_id)) == 0:
            raise NotFoundError()

    def contain_user(self, user_id: int) -> NoReturn:
        if len(self.filter_user(user_id)) == 0:
            raise NotFoundError()

    @staticmethod
    def unique(folder: Folder) -> NoReturn:
        if folders().count(folder) != 0:
            raise DataUniqueError()

    @staticmethod
    def filter_id(_id: int) -> Tuple[Folder, ...]:
        return tuple(filter(lambda folder: folder.id == _id, folders()))

    @staticmethod
    def filter_user(_id: int) -> Tuple[Folder, ...]:
        return tuple(filter(lambda folder: folder.user.id == _id, folders()))


def id_users() -> Tuple[int, ...]:
    return tuple(set(map(lambda folder: folder.user.id, folders())))


def invalid_id_users() -> Tuple[Tuple[int, int], ...]:
    return (
        (random.choice(id_folders()), -1),
        (random.choice(id_folders()), max(id_users()) + 1),
    )


def invalid_id_sets() -> Tuple[Tuple[int, int], ...]:
    return invalid_id_users() + (
        (-1, random.choice(id_users())),
        (max(id_folders()) + 1, random.choice(id_users()))
    )


def folders_by_user_id(user_id: int) -> Tuple[Folder, ...]:
    return tuple(filter(
        lambda folder: folder.user.id == user_id, folders()
    ))


@contextmanager
def not_raises(*exception):
    try:
        yield
    except exception:
        raise pytest.fail("DIDN'T RAISE {0}".format(exception))


@pytest.fixture(scope='module')
def service() -> FolderService:
    return FolderService(FoldersMock)


class TestFolderService:
    @pytest.mark.parametrize('folder_id, user_id, folder',
                             [(folder.id, folder.user.id, folder) for folder in folders()])
    def test_get__found(self, service, folder_id: int, user_id: int, folder: Folder):
        assert service.get(folder_id, user_id) == folder

    @pytest.mark.parametrize('folder_id, user_id', invalid_id_sets())
    def test_get__not_found_error(self, service, folder_id: int, user_id: int):
        with pytest.raises(NotFoundError):
            service.get(folder_id, user_id)

    @pytest.mark.parametrize('user_id, folders_tuple',
                             [(user_id, folders_by_user_id(user_id)) for user_id in id_users()])
    def test_get_all__found(self, service, user_id, folders_tuple):
        assert service.get_all(user_id) == folders_tuple

    @pytest.mark.parametrize('user_id', map(lambda x: x[1], invalid_id_users()))
    def test_get_all__not_found_error(self, service, user_id):
        with pytest.raises(NotFoundError):
            service.get_all(user_id)

    def test_create__done(self, service):
        user_id: int = random.choice(id_users())
        last_folder_id: int = max(id_folders())
        assert service.create(user_id, FolderInputData("example")) == last_folder_id + 1

    @pytest.mark.parametrize('user_id', [user_id for folder_id, user_id in invalid_id_users()])
    def test_create__not_found_error(self, service, user_id: int):
        with pytest.raises(NotFoundError):
            service.create(user_id, FolderInputData("example"))

    @pytest.mark.parametrize('folder_id, user_id, name',
                             [(folder.id, folder.user.id, folder.name) for folder in folders()])
    def test_update__no_changes(self, service, folder_id: int, user_id: int, name: str):
        data = FolderInputData(name)
        with not_raises(NotFoundError, DataUniqueError):
            service.update(folder_id, user_id, data)

    @pytest.mark.parametrize('folder_id, user_id, counter',
                             [(folder.id, folder.user.id, i) for i, folder in enumerate(folders())])
    def test_update__with_changes(self, service, folder_id: int, user_id: int, counter: int):
        data = FolderInputData(f'new_folder-{counter}')
        with not_raises(NotFoundError):
            service.update(folder_id, user_id, data)

    @pytest.mark.parametrize('folder_id, user_id', invalid_id_sets())
    def test_update__not_found_error(self, service, folder_id: int, user_id: int):
        data = FolderInputData('example')
        with pytest.raises(NotFoundError):
            service.update(folder_id, user_id, data)

    @pytest.mark.parametrize('folder_id, user_id', [(folder.id, folder.user.id) for folder in folders()])
    def test_delete__done(self, service, folder_id, user_id):
        with not_raises(NotFoundError):
            service.delete(folder_id, user_id)

    @pytest.mark.parametrize('folder_id, user_id', invalid_id_sets())
    def test_delete__not_found_error(self, service, folder_id, user_id):
        with pytest.raises(NotFoundError):
            service.delete(folder_id, user_id)
