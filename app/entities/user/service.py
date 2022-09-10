from werkzeug.security import generate_password_hash, check_password_hash

from app.rest_lib.services import Service
from app.errors import NoSuchEntityError, Forbidden, EmailAlreadyExists

from .repository import UserRepository, User, PK
from .model import Status


class UserService(Service):
    repository: UserRepository

    def __init__(self, repository: UserRepository = UserRepository()):
        super().__init__(repository=repository)

    def get_by_pk(self, entity_id: int) -> User:
        user = self.repository.get_by_pk(PK(id=entity_id))
        if not user:
            raise NoSuchEntityError('Пользователь не существует.')

        return user

    def register(self, data: dict) -> None:
        data['password'] = generate_password_hash(data['password'])
        if self.repository.get_by_email(data['email']):
            raise EmailAlreadyExists()

        user = User(**data)
        self.repository.insert(user)

    def authorize(self, data: dict) -> User:
        user = self.repository.get_by_email(data['email'])
        if not user or not check_password_hash(user.password, data['password']):
            raise NoSuchEntityError('Пользователь не существует.')
        return user

    @staticmethod
    def check_usable(user):
        if user.status in [Status.unconfirmed, Status.blocked]:
            raise Forbidden(
                {
                    Status.blocked: 'Аккаунт заблокирован',
                    Status.common: 'Аккаунт не подтверждён'
                }[user.status]
            )

        return user

    def edit(self, entity_id: int, data: dict) -> None:
        self.repository.update(PK(id=entity_id), data)

    def delete(self, entity_id: int) -> None:
        self.repository.delete(PK(id=entity_id))

    def change_password(self, entity_id: int, password: str) -> None:
        self.repository.update(PK(id=entity_id), data=dict(
            password=generate_password_hash(password)
        ))
