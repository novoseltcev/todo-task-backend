import random
from contextlib import contextmanager
from typing import NoReturn, Tuple

from mock import Mock
import pytest

from server.exec.errors import NotFoundError
from server.folder.business.service import (
    FolderRepository, Folder, User,
    FolderService, FolderInputData,
)


def folders():
    return [
        Folder.Generator.example(folder_id=0, user_id=1),
        Folder.Generator.example(folder_id=1, user_id=0),
    ]


def id_folders() -> Tuple[int, ...]:
    return tuple(map(lambda folder: folder.id, folders()))


class FakeFolders(FolderRepository, Mock):
    """Mocking repository class to service"""
    max_id = max(id_folders())

    def from_id(self, folder_id: int) -> Folder:
        self.contain_id(folder_id)
        return self.filter_id(folder_id)[-1]

    def from_user(self, user_id: int) -> Tuple[Folder, ...]:
        self.contain_user(user_id)
        return self.filter_user(user_id)

    def create(self, user_id: int, folder: Folder) -> int:
        self.contain_user(user_id)
        self.max_id += 1
        return self.max_id

    def update(self, folder: Folder) -> None:
        self.contain_id(folder.id)

    def delete(self, folder: Folder) -> None:
        self.contain_id(folder.id)

    def contain_id(self, folder_id: int) -> NoReturn:
        if len(self.filter_id(folder_id)) == 0:
            raise NotFoundError()

    def contain_user(self, user_id: int) -> NoReturn:
        if len(self.filter_user(user_id)) == 0:
            raise NotFoundError()

    @staticmethod
    def filter_id(_id: int) -> Tuple[Folder, ...]:
        return tuple(filter(lambda folder: folder.id == _id, folders()))

    @staticmethod
    def filter_user(_id: int) -> Tuple[Folder, ...]:
        return tuple(filter(lambda folder: folder.user.id == _id, folders()))


def users() -> Tuple[User, ...]:
    return tuple(set(map(lambda folder: folder.user, folders())))


# def invalid_id_users() -> Tuple[Tuple[int, int], ...]:
#     return (
#         (random.choice(id_folders()), -1),
#         (random.choice(id_folders()), max(users()) + 1),
#     )


def invalid_sets() -> Tuple[Tuple[int, User], ...]:
    return (
        (-1, random.choice(users())),
        (max(id_folders()) + 1, random.choice(users()))
    )


def folders_by_user_id(user_id: int) -> Tuple[Folder, ...]:
    return tuple(filter(
        lambda folder: folder.user.id == user_id, folders()
    ))


@contextmanager
def not_raises(*exception):
    try:
        yield
    except exception as ex:
        raise pytest.fail(f'DID NOT RAISE {exception}') from ex


@pytest.fixture(scope='module')
def service() -> FolderService:
    return FolderService(FakeFolders)


class TestFolderService:
    """UnitTests to FolderService"""

    @pytest.mark.parametrize('folder_id, user, folder',
                             [(folder.id, folder.user, folder) for folder in folders()])
    def test_get__found(self, service, folder_id: int, user: User, folder: Folder):
        assert service.get(folder_id, user) == folder

    @pytest.mark.parametrize('folder_id, user', invalid_sets())
    def test_get__not_found_error(self, service, folder_id: int, user: User):
        with pytest.raises(NotFoundError):
            service.get(folder_id, user)

    @pytest.mark.parametrize('user, folders_tuple',
                             [(user, folders_by_user_id(user.id)) for user in users()])
    def test_get_all__found(self, service, user, folders_tuple):
        assert service.get_all(user) == folders_tuple

    def test_create__done(self, service):
        user: User = random.choice(folders()).user
        last_folder_id: int = max(id_folders())
        assert service.create(user, FolderInputData("example")) == last_folder_id + 1

    @pytest.mark.parametrize('folder_id, user, name',
                             [(folder.id, folder.user, folder.name) for folder in folders()])
    def test_update__no_changes(self, service, folder_id: int, user: User, name: str):
        data = FolderInputData(name)
        with not_raises(NotFoundError):
            service.update(folder_id, user, data)

    @pytest.mark.parametrize('folder_id, user, counter',
                             [(folder.id, folder.user, i) for i, folder in enumerate(folders())])
    def test_update__with_changes(self, service, folder_id: int, user: User, counter: int):
        data = FolderInputData(f'new_folder-{counter}')
        with not_raises(NotFoundError):
            service.update(folder_id, user, data)

    @pytest.mark.parametrize('folder_id, user', invalid_sets())
    def test_update__not_found_error(self, service, folder_id: int, user: User):
        data = FolderInputData('example')
        with pytest.raises(NotFoundError):
            service.update(folder_id, user, data)

    @pytest.mark.parametrize('folder_id, user', [(folder.id, folder.user) for folder in folders()])
    def test_delete__done(self, service, folder_id: int, user: User):
        with not_raises(NotFoundError):
            service.delete(folder_id, user)

    @pytest.mark.parametrize('folder_id, user', invalid_sets())
    def test_delete__not_found_error(self, service, folder_id, user: User):
        with pytest.raises(NotFoundError):
            service.delete(folder_id, user)
