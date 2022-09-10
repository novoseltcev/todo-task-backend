from __future__ import annotations
from app.rest_lib.repository import Repository, NamedTuple
from app.entities.user.model import User


class PK(NamedTuple):
    id: int


class UserRepository(Repository):
    model: User

    def __init__(self):
        super().__init__(model=User)

    def get_by_pk(self, pk: PK) -> User:
        return self.pk_query(pk).first()

    def get_by_email(self, email: str) -> User:
        return self.query().filter(self.model.email == email).first()

    def insert(self, entity: User) -> User:
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, pk: PK, data: dict) -> None:
        self.pk_query(pk).update(data)
        self.session.commit()

    def delete(self, pk: PK) -> None:
        self.pk_query(pk).delete()
        self.session.commit()
