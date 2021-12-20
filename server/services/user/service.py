from .abstract import (
    UserInteractor,
    UserRepo,
)
from .entity import (
    User,
    LoginError,
    NotFoundError,
    PasswordError,
    UnconfirmedEmailError,
)


class UserService(UserInteractor):
    Users: UserRepo = UserRepo

    @classmethod
    def get_account(cls, id):
        return cls.Users.from_id(id)

    @classmethod
    def get_accounts(cls, admin_id):
        user = cls.Users.from_id(admin_id)
        user.admin_access()
        return cls.Users.all()

    @classmethod
    def update_account(cls, id, data):
        user = cls.Users.from_id(id)
        user.name = data.name
        user.update_password(data.password)
        user.update_email(data.email)
        cls.Users.update(id, user)

    @classmethod
    def delete_account(cls, id):
        cls.Users.delete(id)

    @classmethod
    def register(cls, data):
        user = User.create(name=data.name, email=data.email, password=data.password)
        cls.Users.create(user)

    @classmethod
    def login(cls, data):
        try:
            user = cls.Users.from_email(data.email) if data.name is None else cls.Users.from_name(data.name)
            user.check_password(data.password)
            user.check_email_confirm()
            return user.id
        except (NotFoundError, PasswordError):
            raise LoginError("Not found account")
        except UnconfirmedEmailError:
            raise UnconfirmedEmailError("Account not confirmed")

    @classmethod
    def reset_password(cls, uuid, password):
        user = cls.Users.from_uuid(uuid)
        user.update_password(password)
        cls.Users.update(user.id, user)

    @classmethod
    def confirm_email(cls, uuid):
        user = cls.Users.from_uuid(uuid)
        user.confirm_email()
        cls.Users.update(user.id, user)
