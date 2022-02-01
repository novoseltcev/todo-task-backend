import uuid

from .. import File


class FileGenerator:
    """Generate file examples for tests."""

    @classmethod
    def example(cls, identity: int, account_id: int, task_id: int) -> File:
        return File(
            name=f'File<{identity}>.ext',
            path=f'remote.resource.com/files_bucket/{uuid.uuid4()}.ext',
            task=task_id,
            account=account_id,
            identity=identity
        )
