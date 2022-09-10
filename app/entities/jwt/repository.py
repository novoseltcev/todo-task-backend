from __future__ import annotations
from datetime import datetime as dt

from app.rest_lib.repository import Repository, NamedTuple
from .model import JWTToken


class PK(NamedTuple):
    jti: str


class JWTRepository(Repository):
    model: JWTToken

    def __init__(self):
        super().__init__(model=JWTToken)

    def get_by_pk(self, pk: PK) -> JWTToken:
        return self.pk_query(pk).first()

    def insert(self, entity: JWTToken) -> JWTToken:
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, pk: PK, data: dict) -> None:
        self.pk_query(pk).update(data)
        self.session.commit()

    def update_by_user(self, user_id: int, data: dict) -> None:
        self.query().filter(self.model.user_id == user_id).update(data)
        self.session.commit()

    def delete(self, pk: PK) -> None:
        self.pk_query(pk).delete()

    def delete_expired(self) -> None:
        self.query().filter(dt.now() > self.model.end_life).delete()
