from .repository import UserRepository
from .serializer import serialize_user


user_rep = UserRepository()


def get_profile(**kwargs):
    user = user_rep._get_by(**kwargs)
    return serialize_user(user)


def create_account(**kwargs):
    user_rep.insert(**kwargs)


def login(**kwargs):
    password = kwargs['password']
    kwargs.pop('password')
    user = user_rep._get_by(**kwargs)
    return user.check_password(password)
