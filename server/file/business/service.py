from typing import Tuple

from .interactor import (
    FileInteractor, FileInputData,
    FileRepository, File, User, Task
)


class FileService(FileInteractor):  # TODO - realize working interface
    """Implementation of the interface for interacting with the File's business logic"""

    def get(self, file_id: int, user: User) -> File:
        pass

    def get_by_task(self, task: Task) -> Tuple[File, ...]:
        pass

    def get_all(self, user: User) -> Tuple[File, ...]:
        pass

    def pin_and_create(self, user: User, data: FileInputData) -> int:
        pass

    def unpin_and_delete(self, file_id: int, user: User) -> None:
        pass
