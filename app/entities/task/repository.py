from typing import NamedTuple

from .model import Task

from app.rest_lib.repository import Repository


class PK(NamedTuple):
    id: int
    user_id: int


class TaskRepository(Repository):
    model: Task

    def __init__(self):
        super().__init__(model=Task)

    def get_by_pk(self, pk: PK):
        return self.pk_query(pk).first()

    def insert(self, entity: Task):
        self.session.add(entity)
        self.session.commit()

    def update(self, pk: PK, data: dict):
        self.pk_query(pk).update(data)
        self.session.commit()

    def delete(self, pk: PK):
        self.pk_query(pk).delete()
        self.session.commit()
