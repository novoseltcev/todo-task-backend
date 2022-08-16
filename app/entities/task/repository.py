from typing import NamedTuple

from .model import Task

from app.db import db
from app.rest_lib.repository import Repository


class TaskRepository(Repository):

    class PrimaryKey(NamedTuple):
        user_id: int
        id: int

    model: Task

    def __init__(self):
        super().__init__(model=Task)

    def pk_query(self, pk: PrimaryKey) -> db.Query:
        return self.query().filter(self.model.user_id == pk.user_id, self.model.id == pk.id)

    def get_by_pk(self, pk: PrimaryKey):
        return self.pk_query(pk).first()

    def insert(self, entity: Task):
        self.session.add(entity)
        self.session.commit()

    def update(self, pk: PrimaryKey, data: dict):
        self.pk_query(pk).edit(**data)
        self.session.commit()

    def delete(self, pk: PrimaryKey):
        self.pk_query(pk).delete()
        self.session.commit()
