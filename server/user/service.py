from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import flask
from flask_login import login_user, logout_user

from .repository import UserRepository
from .serializer import serialize_user


user_repository = UserRepository()


def get_profile(id):
    user = user_repository.get_by_primary(id=id)
    return serialize_user(user)


def create_account(login: str, email: str, password: str):
    checked_user1 = user_repository.get_by_login(login)
    checked_user2 = user_repository.get_by_email(email)
    if len(checked_user1) == 0 and len(checked_user2) == 0:
        password_hash = generate_password_hash(password)
        reg_date = datetime.now()

        response_obj = {
            'login': login,
            'email': email,
            'password': password_hash,
            'reg_date': reg_date
        }
        user_repository.insert(**response_obj)
        user = user_repository.get_by_login(login)
        return user


def login(password: str, auth_method):
    user = user_repository.get_by_login(auth_method)

    result = check_password_hash(user.password, password)
    if result:
        return user
