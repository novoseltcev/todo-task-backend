import uuid
from typing import Tuple

from .interactor import (
    FileInteractor, FileInputData,
    FileRepository, File, NotFoundError
)
from ...task import TaskService


class FileService(FileInteractor):
    """Implementation of the interface for interacting with the File's domain logic"""

    def get(self, identity: int, account_id: int) -> File:
        result = self.files.from_id(identity)
        if result.account != account_id:
            raise NotFoundError()
        return result

    def get_by_task(self, task_id: int, account_id: int) -> Tuple[File, ...]:
        self._external_task(account_id, task_id)
        return self.files.from_task(task_id)

    def get_by_account(self, account_id: int) -> Tuple[File, ...]:
        return self.files.from_account(account_id)

    def unpin_and_delete(self, identity: int, account_id: int) -> None:
        file = self.get(identity, account_id)
        self.files.remove(file)

    def create_and_pin(self, account_id: int, data: FileInputData) -> int:
        metadata = {
            'task': data.task_id,
            'account': account_id,
        }
        path = self.files.transfer(data.data, metadata)
        identity = self.files.insert(
            File(
                name=data.name,
                path=path,
                task=data.task_id,
                account=account_id,
            )
        )
        return identity


    @staticmethod
    def _external_task(account_id, task_id):
        task = TaskService().get(task_id, account_id)  # TODO

