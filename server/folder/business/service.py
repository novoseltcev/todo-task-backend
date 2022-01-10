from typing import Tuple

from .interactor import (
    FolderInteractor, FolderInputData,
    FolderRepository, Folder, User,
)


class FolderService(FolderInteractor):
    """Not working folder service"""

    def get(self, folder_id: int, user: User) -> Folder:  # TODO
        return Folder.Generator.example(-1, -1)

    def get_all(self, user: User) -> Tuple[Folder, ...]:  # TODO
        return (Folder.Generator.example(-1, -1),)

    def create(self, user: User, data: FolderInputData) -> int:  # TODO
        return -1

    def update(self, folder_id: int, user: User, data: FolderInputData) -> None:  # TODO
        assert False

    def delete(self, folder_id: int, user: User) -> None:  # TODO
        assert False
