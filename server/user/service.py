from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from server.user.repository import UserRepository
from server.user.serializer import serialize_user, UserSchema


def get_profile(id):
    user = UserRepository.get_by_id(id=id)
    return serialize_user(user)


def create_account(login: str, email: str, password: str):
    checked_user1 = UserRepository.get_by_login(login)
    checked_user2 = UserRepository.get_by_email(email)
    if len(checked_user1) == 0 and len(checked_user2) == 0:
        password_hash = generate_password_hash(password)
        reg_date = datetime.now()

        response_obj = {
            'login': login,
            'email': email,
            'password': password_hash,
            'reg_date': reg_date
        }
        UserRepository.insert(**response_obj)
        user = UserRepository.get_by_login(login)
        return user


def login(password: str, auth_method):
    user = UserRepository.get_by_login(auth_method)

    result = check_password_hash(user.password, password)
    if result:
        return user
