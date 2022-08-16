from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.rest_lib.services import Service
from app.errors import NoSuchEntityError, Forbidden, LogicError
from app.entities.user.repository import UserRepository

from .model import User, Status


class UserService(Service):
    repository: UserRepository

    def __init__(self, repository: UserRepository = UserRepository()):
        super().__init__(repository=repository)

    def get_by_pk(self, entity_id: int) -> User:
        user = self.repository.get_by_pk(entity_id)
        if not user:
            raise NoSuchEntityError('Пользователь не существует.')

        return user

    def register(self, data: dict) -> User:
        user = User(
                **data,
                password=generate_password_hash(data['password']),
                reg_date=datetime.now()
            )
        self.repository.insert(user)
        return user

    def authorize(self, data: dict) -> User:
        user = self.repository.get_by_email(data['email'])
        if not user or not check_password_hash(user.password, data['password']):
            raise NoSuchEntityError('Пользователь не существует.')

        if user.status in [Status.unconfirmed, Status.blocked]:
            raise Forbidden()

        return user

    def edit(self, entity_id: int, data: dict) -> None:
        user = self.repository.get_by_pk(entity_id)
        if check_password_hash(user.password, data['password']) and user.email == data['email']:
            self.repository.update(entity_id, data)
        else:
            raise LogicError()

    def delete(self, entity_id: int) -> None:
        self.repository.delete(entity_id)
