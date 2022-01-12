from typing import Tuple

from server.exec.errors import (
    NotFoundError,
    LoginError,
)

from .entity import PasswordError, UnconfirmedEmailError
from .interactor import (
    UserInteractor, UserInputData,
    UserRepository, User,
)


class UserService(UserInteractor):  # TODO - realize working interface
    """Implementation of the interface for interacting with the User's business logic"""

    def get_account(self, user_id: int) -> User:
        return self.users.from_id(user_id)

    def get_accounts(self, admin_id: int) -> Tuple[User, ...]:
        user = self.users.from_id(admin_id)
        user.admin_access()
        return self.users.all()

    def update_account(self, user_id: int, data: UserInputData):
        user = self.users.from_id(user_id)
        user.password = data.password
        user.email = data.email
        self.users.update(user_id, user)

    def delete_account(self, user_id: int):
        self.users.delete(user_id)

    def register(self, data: UserInputData):
        user = User.create(name=data.name, email=data.email, password=data.password)
        self.users.create(user)

    def login_by_name(self, data: UserInputData) -> int:
        try:
            user = self.users.from_name(data.name)
            user.check_password(data.password)
            user.check_email()
            return user.id
        except (NotFoundError, PasswordError) as exc:
            raise LoginError("Not found account") from exc
        except UnconfirmedEmailError as exc:
            raise UnconfirmedEmailError("Account not confirmed") from exc

    def login_by_email(self, data: UserInputData) -> int:
        try:
            user = self.users.from_email(data.email)
            user.check_password(data.password)
            user.check_email()
            return user.id
        except (NotFoundError, PasswordError) as exc:
            raise LoginError("Not found account") from exc
        except UnconfirmedEmailError as exc:
            raise UnconfirmedEmailError("Account not confirmed") from exc

    def reset_password(self, uuid: str, password: str):
        user = self.users.from_uuid(uuid)
        user.password = password
        self.users.update(user.id, user)

    def confirm_email(self, uuid: str):
        user = self.users.from_uuid(uuid)
        user.confirm()
        self.users.update(user.id, user)
