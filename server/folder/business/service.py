from typing import Tuple

from .interactor import (
    FolderInteractor, FolderInputData,
    FolderRepository, Folder, User,
)


class FolderService(FolderInteractor):  # TODO - realize working interface
    """Implementation of the interface for interacting with the Folder's business logic"""

    def get(self, folder_id: int, user: User) -> Folder:
        return Folder.Generator.example(-1 * folder_id, -1 * user.id)

    def get_all(self, user: User) -> Tuple[Folder, ...]:
        return (
            Folder.Generator.example(-1, -1 * user.id),
            Folder.Generator.example(-2, -2 * user.id),
        )

    def create(self, user: User, data: FolderInputData) -> int:
        _ = data
        return -1 * user.id

    def update(self, folder_id: int, user: User, data: FolderInputData) -> None:
        _ = (folder_id, user, data)
        assert False

    def delete(self, folder_id: int, user: User) -> None:
        _ = (folder_id, user)
        assert False
