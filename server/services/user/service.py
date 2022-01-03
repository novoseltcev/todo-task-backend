from .interactor import UserInteractor
from .entity import (
    User,
    LoginError,
    NotFoundError,
    PasswordError,
    UnconfirmedEmailError,
)


class UserService(UserInteractor):
    def get_account(self, id):
        return self.users.from_id(id)

    def get_accounts(self, admin_id):
        user = self.users.from_id(admin_id)
        user.admin_access()
        return self.users.all()

    def update_account(self, id, data):
        user = self.users.from_id(id)
        user.name = data.name
        user.update_password(data.password)
        user.update_email(data.email)
        self.users.update(id, user)

    def delete_account(self, id):
        self.users.delete(id)

    def register(self, data):
        user = User.create(name=data.name, email=data.email, password=data.password)
        self.users.create(user)

    def login_by_name(self, data):
        try:
            user = self.users.from_name(data.name)
            user.check_password(data.password)
            user.check_email_confirm()
            return user.id
        except (NotFoundError, PasswordError):
            raise LoginError("Not found account")
        except UnconfirmedEmailError:
            raise UnconfirmedEmailError("Account not confirmed")

    def login_by_email(self, data):
        try:
            user = self.users.from_email(data.email)
            user.check_password(data.password)
            user.check_email_confirm()
            return user.id
        except (NotFoundError, PasswordError):
            raise LoginError("Not found account")
        except UnconfirmedEmailError:
            raise UnconfirmedEmailError("Account not confirmed")

    def reset_password(self, uuid, password):
        user = self.users.from_uuid(uuid)
        user.update_password(password)
        self.users.update(user.id, user)

    def confirm_email(self, uuid):
        user = self.users.from_uuid(uuid)
        user.confirm_email()
        self.users.update(user.id, user)
