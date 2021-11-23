from datetime import date

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ._serviceABC import UserService, UserSchema, UserResponse
from ._repositoryABC import Users
from .model import User

from server.errors.exc import LoginError, RegistrationError, UnconfirmedEmailError  # TODO - optimize dependency


class UserLogic(UserService):
    @classmethod
    def get(cls, schema: UserSchema) -> UserResponse:
        user = Users.load(schema.id)
        return UserResponse.dump(user)

    @classmethod
    def get_all(cls, schema: UserSchema) -> UserResponse:
        user = Users.load(schema.id)
        cls.is_admin(user)

        users = Users.load_all()
        return UserResponse.dump(users, many=True)

    @classmethod
    def create(cls, schema: UserSchema) -> UserResponse:
        try:
            password_hash = generate_password_hash(schema.password)
            user = User(email=schema.email, password=password_hash, reg_date=date.today())
            Users.save(user)
            return UserResponse.success()
        except IntegrityError:
            raise RegistrationError()

    @classmethod
    def login(cls, schema: UserSchema) -> UserResponse:
        try:
            user = Users.load_by_email(schema.email)
            if not check_password_hash(user.password, schema.password):
                raise LoginError()
            if not user.confirmed_email:
                raise UnconfirmedEmailError(user.email)
            return UserResponse.success()
        except NoResultFound:
            raise LoginError('No User')

    @classmethod
    def edit(cls, schema: UserSchema) -> UserResponse:
        user = cls.check_access(schema)
        #  TODO - edit User
        Users.save(user)
        return UserResponse.success()

    @classmethod
    def delete(cls, schema: UserSchema) -> UserResponse:
        Users.delete(schema.id)  # TODO - add refuse all data
        return UserResponse.success()

    @classmethod
    def confirm_email(cls, schema: UserSchema) -> UserResponse:
        user = Users.load_by_uuid(schema.uuid)
        user.confirmed_email = True
        Users.save(user)
        return UserResponse.success()

    @classmethod
    def is_admin(cls, user: User):
        from .schema import Role
        if user.role not in (Role.admin, Role.owner):
            pass  # TODO - raise AuthError

    @classmethod
    def check_access(cls, schema: UserSchema) -> User:
        user = Users.load_by_email(schema.email)
        if not check_password_hash(user.password, schema.password):
            raise LoginError()
        return user
