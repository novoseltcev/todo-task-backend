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
        return cls.Users.load(id)

    @classmethod
    def get_accounts(cls, admin_id):
        user = cls.Users.load(admin_id)
        user.admin_access()
        return cls.Users.load_all()

    @classmethod
    def update_account(cls, id, data):
        user = cls.Users.load(id)
        password = data.password
        user.name = data.name
        user.update_email(data.email)
        user.update_password(password)
        cls.Users.save(user)

    @classmethod
    def delete_account(cls, id):
        cls.Users.delete(id)

    @classmethod
    def register(cls, data):
        user = User.create(name=data.name, email=data.email, password=data.password)
        cls.Users.save(user)

    @classmethod
    def login(cls, data):
        if data.email is None and data.name is None or data.password is None:
            raise LoginError()
        try:
            user = cls.Users.load_by_email(data.email) if data.name is None else cls.Users.load_by_name(data.name)
            user.check_password(data.password)
            user.check_email_confirm()
            return user.id
        except NotFoundError or PasswordError:
            raise LoginError("Not found account")
        except UnconfirmedEmailError:
            raise UnconfirmedEmailError("Account not confirmed")

    @classmethod
    def reset_password(cls, uuid, password):
        ...

    @classmethod
    def confirm_email(cls, uuid):
        user = cls.Users.load_by_uuid(uuid)
        user.confirm_email()
        cls.Users.save(user)
