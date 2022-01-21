from typing import Tuple

from .interactor import (
    FileInteractor, FileInputData,
    FileRepository, File, Task
)


class FileService(FileInteractor):  # TODO - realize working interface
    """Implementation of the interface for interacting with the File's business logic"""

    def get(self, file_identity: int, account_identity: int) -> File:
        pass

    def get_by_task(self, task_identity: int) -> Tuple[File, ...]:
        pass

    def get_all(self, account_identity: int) -> Tuple[File, ...]:
        pass

    def pin_and_create(self, account_identity: int, data: FileInputData) -> int:
        pass

    def unpin_and_delete(self, file_identity: int, account_identity: int) -> None:
        pass

