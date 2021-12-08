from typing import NoReturn

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from .abstract import UserInteractor, Users
from .response import UserSerializer, UserResponse, UserSchema
from .entity import User, LoginError, RegistrationError, ConfirmationError

# from server.repositories.user import UserRepository as Users


class UserService(UserInteractor):
    @classmethod
    def register(cls, schema: UserSchema) -> NoReturn:
        try:
            user = User.create(name=schema.name, email=schema.email, password=schema.password)
            Users.save(user)
        except IntegrityError:
            raise RegistrationError()

    @classmethod
    def get(cls, schema: UserSchema) -> UserResponse:
        user = Users.load(schema.id)
        return UserSerializer.dump(user)

    @classmethod
    def get_all(cls, schema: UserSchema) -> UserResponse:
        user = Users.load(schema.id)
        user.admin_access()
        users = Users.load_all()
        return UserSerializer.dump_many(users)

    @classmethod
    def update(cls, schema: UserSchema) -> NoReturn:
        user = cls.check_access(schema)
        password = schema.password
        user.name = schema.name
        user.change_email(schema.email, password)
        user.change_password(password, password)
        Users.save(user)

    @classmethod
    def delete(cls, schema: UserSchema) -> NoReturn:  # TODO
        Users.delete(schema.id)  # TODO - add refuse all data

    @classmethod
    def login(cls, schema: UserSchema) -> NoReturn:
        try:
            user = Users.load_by_email(schema.email)
            user.check_password(schema.password)
            user.check_email_confirm()
        except NoResultFound:
            raise LoginError()

    @classmethod
    def confirm_email(cls, schema: UserSchema) -> NoReturn:
        try:
            user = Users.load_by_uuid(schema.uuid)
            user.confirm_email()
            Users.save(user)
        except NoResultFound:
            raise ConfirmationError(schema.uuid)

    @classmethod
    def check_access(cls, schema: UserSchema) -> User:
        user = Users.load_by_email(schema.email)
        user.check_password(schema.password)
        return user
