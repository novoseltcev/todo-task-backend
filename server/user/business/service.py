from entity import (
    User,
    PasswordError,
    UnconfirmedEmailError,
)
from interactor import UserInteractor

from server.exec.errors import (
    NotFoundError,
    LoginError,
)


class UserService(UserInteractor):  # TODO - add docstring
    def get_account(self, user_id):
        return self.users.from_id(user_id)

    def get_accounts(self, admin_id):
        user = self.users.from_id(admin_id)
        user.admin_access()
        return self.users.all()

    def update_account(self, user_id, data):
        user = self.users.from_id(user_id)
        user.password = data.password
        user.email = data.email
        self.users.update(user_id, user)

    def delete_account(self, user_id):
        self.users.delete(user_id)

    def register(self, data):
        user = User.create(name=data.name, email=data.email, password=data.password)
        self.users.create(user)

    def login_by_name(self, data):
        try:
            user_id, user = self.users.from_name(data.name)
            user.check_password(data.password)
            user.check_email()
            return user_id
        except (NotFoundError, PasswordError) as exc:
            raise LoginError("Not found account") from exc
        except UnconfirmedEmailError as exc:
            raise UnconfirmedEmailError("Account not confirmed") from exc

    def login_by_email(self, data):
        try:
            user_id, user = self.users.from_email(data.email)
            user.check_password(data.password)
            user.check_email()
            return user_id
        except (NotFoundError, PasswordError) as exc:
            raise LoginError("Not found account") from exc
        except UnconfirmedEmailError as exc:
            raise UnconfirmedEmailError("Account not confirmed") from exc

    def reset_password(self, uuid, password):
        user_id, user = self.users.from_uuid(uuid)
        user.password = password
        self.users.update(user_id, user)

    def confirm_email(self, uuid):
        user_id, user = self.users.from_uuid(uuid)
        user.confirm()
        self.users.update(user_id, user)
