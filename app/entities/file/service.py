from uuid import uuid4 as generate_uuid, UUID

from app.errors import NoSuchEntityError
from app.rest_lib.services import Service
from app.adapters.persistent_storage import PersistentStorage, S3Storage

from .repository import FileRepository, File, PK
from ..task.service import TaskService


class FileService(Service):
    repository: FileRepository

    def __init__(
            self,
            repository: FileRepository = FileRepository(),
            persistent_storage: PersistentStorage = S3Storage()
    ):
        super().__init__(repository=repository)
        self.persistent_storage = persistent_storage
        self.task_service = TaskService()

    def get_by_pk(self, uuid: UUID, user_id: int):
        file = self.repository.get_by_pk(PK(uuid=uuid, user_id=user_id))
        if not file:
            raise NoSuchEntityError('Файл не существует')

        file.download_url = self.persistent_storage.get_download_url(file.path)
        return file

    def create(self, task_id: int, user_id: int, filename: str, size: int) -> File:
        self.task_service.get_by_pk(user_id=user_id, entity_id=task_id)

        file = File(
            uuid=generate_uuid(),
            filename=filename,
            user_id=user_id,
            task_id=task_id,
            path=generate_uuid()
        )
        file.upload_url = self.persistent_storage.create_upload_url(file.path, size=size)
        try:
            self.repository.insert(file)

            self.repository.session.commit()
            return file
        except Exception as e:
            self.persistent_storage.delete(file.path)
            self.repository.session.rollback()
            raise e

    def delete(self, uuid: UUID, user_id: int):
        pk = PK(uuid=uuid, user_id=user_id)
        file = self.repository.get_by_pk(pk)
        if file:
            try:
                self.repository.delete(pk)
                self.persistent_storage.delete(file.path)
                self.repository.session.commit()
            except Exception as e:
                self.repository.session.rollback()
                raise e
