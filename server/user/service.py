from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from server.errors.exc import LoginError, RegistrationError
from server.user.repository import UserRepository
from server.user.serializer import serialize_user, UserSchema
from server.category import service as category_service
from server.async_tasks.email import confirm_registration


def create_account(login: str, email: str, password: str):
    password_hash = generate_password_hash(password)
    reg_date = datetime.now()
    try:

        user = UserRepository.insert(login, email, password_hash, reg_date)
        return user
    except IntegrityError:
        raise RegistrationError()


def login(schema):
    try:
        user = UserRepository.get_by_login(schema['login'])
        result = check_password_hash(user.password, schema['password'])
        if not result:
            raise LoginError()
    except NoResultFound:
        raise LoginError()

    return user


def change_profile(user_id, schema):
    user = UserRepository.get_by_id(user_id)
    if not check_password_hash(user.password, schema['password']) or user.email != schema['email']:
        UserRepository.update(schema, user_id)
    else:
        raise
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
