from datetime import datetime as dt

from app.rest_lib.repository import Repository
from .model import JWTToken


class JWTRepository(Repository):
    model: JWTToken

    def __init__(self):
        super().__init__(model=JWTToken)

    def get_by_pk(self, token: str) -> JWTToken:
        return self.query().filter(self.model.token == token).first()

    def insert(self, entity: JWTToken) -> JWTToken:
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, token: str, data: dict) -> None:
        self.query().filter(self.model.token == token).update(**data)
        self.session.commit()

    def update_by_user(self, user_id: int, data: dict) -> None:
        self.query().filter(self.model.user_id == user_id).update(**data)
        self.session.commit()

    def delete(self, token: str) -> None:
        self.query().filter(self.model.token == token).delete()

    def delete_expired(self) -> None:
        self.query().filter(dt.now() > self.model.end_life).delete()

