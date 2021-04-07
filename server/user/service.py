from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from server.errors.exc import LoginError, RegistrationError, UnconfirmedEmailError
from server.user.repository import UserRepository
from server.user.serializer import serialize_user, UserSchema
from server.category import service as category_service


def create_account(email: str, password: str):
    password_hash = generate_password_hash(password)
    reg_date = datetime.now()
    try:

        user = UserRepository.insert(email, password_hash, reg_date)
        return user
    except IntegrityError:
        raise RegistrationError()


def login(schema):
    try:
        user = UserRepository.get_by_email(schema['email'])
        result = check_password_hash(user.password, schema['password'])
        if not result:
            raise LoginError()
        if not user.confirmed_email:
            raise UnconfirmedEmailError(user.email)
    except NoResultFound:
        raise LoginError()

    return user


def change_profile(user_id, schema):
    user = UserRepository.get_by_id(user_id)
    if check_password_hash(user.password, schema['password']) and user.email == schema['email']:
        UserRepository.update(schema, user_id)
    else:
        raise LoginError()
    return serialize_user(user)


def delete_account(user_id):
    user = UserRepository.delete(user_id)
    categories_by_user = user.categories
    for category in categories_by_user:
        category_service.delete(user_id, category.id)

    return serialize_user(user)


def get_all():
    users = UserRepository.get_all()
    return serialize_user(users, many=True)


def confirm_email(id):
    UserRepository.confirm_email(id)


