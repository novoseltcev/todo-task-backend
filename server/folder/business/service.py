from typing import Tuple

from .interactor import FolderInputData, Folder, FolderInteractor


class FolderService(FolderInteractor):
    def get(self, folder_id: int, user_id: int) -> Folder:  # TODO
        return Folder.Generator.example(-1, -1)

    def get_all(self, user_id: int) -> Tuple[Folder, ...]:  # TODO
        return (Folder.Generator.example(-1, -1), )

    def create(self, user_id: int, data: FolderInputData) -> int:  # TODO
        return -1

    def update(self, folder_id: int, user_id: int, data: FolderInputData) -> None:  # TODO
        assert False

    def delete(self, folder_id: int, user_id: int) -> None:  # TODO
        assert False
