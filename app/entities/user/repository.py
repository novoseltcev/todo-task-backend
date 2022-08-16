from app.rest_lib.repository import Repository
from app.entities.user.model import User


class UserRepository(Repository):
    model: User

    def __init__(self):
        super().__init__(model=User)
        
    def pk_query(self, pk: int):
        return self.query().filter(self.model.id == pk)

    def get_by_pk(self, id: int) -> User:
        return self.pk_query(id).first()

    def get_by_email(self, email: str) -> User:
        return self.query().filter(self.model.email == email).first()

    def insert(self, entity: User) -> User:
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, id: int, data: dict) -> None:
        self.pk_query(id).update(**data)
        self.session.commit()

    def delete(self, id: int) -> None:
        self.pk_query(id).delete()
        self.session.commit()
