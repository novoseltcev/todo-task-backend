from typing import NamedTuple
from uuid import UUID

from app.rest_lib.repository import Repository

from .model import File


class PK(NamedTuple):
    uuid: UUID
    user_id: int


class FileRepository(Repository):
    model: File

    def __init__(self):
        super().__init__(model=File)

    def get_by_pk(self, pk: PK) -> File:
        return self.pk_query(pk).first()

    def insert(self, entity: File) -> None:
        self.session.add(entity)
        self.session.commit()

    def delete(self, pk: PK) -> None:
        self.pk_query(pk).delete()

    def update(self, pk: PK, data: dict):
        self.pk_query(pk).update(data)
