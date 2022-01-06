import uuid
from copy import deepcopy, copy
from datetime import date
from functools import wraps
from unittest import TestCase
from unittest.mock import Mock

from server.user.business import *
from server.user.business.entity import PasswordHash, PasswordError, UserAccessError, UnconfirmedEmailError
from server.exec import *


def example_user(name: str, status: EmailStatus, role: Role):
    user = User(
        name,
        f'{name}@domen.com',
        PasswordHash.generate("password"),
        role,
        status,
        date(2020, 10, 4)
    )
    return user


def load_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            raise NotFoundError()

    return wrapper


users_by_id = {
    1: example_user("st.a.novoseltcev", EmailStatus.CONFIRMED, Role.OWNER),
    2: example_user("admin", EmailStatus.CONFIRMED, Role.ADMIN),
    3: example_user("new_admin", EmailStatus.REFUSED, Role.ADMIN),
    4: example_user("conf_user", EmailStatus.CONFIRMED, Role.USER),
    5: example_user("ref_user", EmailStatus.REFUSED, Role.USER),
    6: example_user("new_user", EmailStatus.NOT_CONFIRMED, Role.USER),
}
users_by_name = {user.name: user for user in users_by_id.values()}
users_by_email = {user.email: user for user in users_by_id.values()}
users_by_uuid = {uuid.uuid4(): user for user in users_by_id.values()}

invalid_id = (
    -1,
    0,
    100,
    max(users_by_id.keys()) + 1,
)


class UsersMock(UserRepository, Mock):
    @classmethod
    def all(cls):
        return deepcopy(users_by_id)

    @classmethod
    @load_wrapper
    def from_id(cls, user_id):
        return copy(users_by_id[user_id])

    @classmethod
    @load_wrapper
    def from_name(cls, name):
        return copy(users_by_name[name])

    @classmethod
    @load_wrapper
    def from_email(cls, email):
        return copy(users_by_email[email])

    @classmethod
    @load_wrapper
    def from_uuid(cls, token):
        return users_by_uuid[token]

    @classmethod
    def create(cls, user):
        if users_by_name.get(user.name) is not None or users_by_email.get(user.email) is not None:
            raise DataUniqueError()

    @classmethod
    def update(cls, user_id, user):
        _user = cls.from_id(user_id)
        name, email = user.name, user.email
        if _user.name != name and users_by_name.get(name) is not None:
            raise DataUniqueError()

        if _user.email != email and users_by_email.get(email) is not None:
            raise DataUniqueError()

    @classmethod
    @load_wrapper
    def delete(cls, user_id):
        _ = users_by_id[user_id]


class UserServiceTestCase(TestCase):
    mocked_checker = copy(PasswordHash.generate)

    @classmethod
    def setUpClass(cls):
        cls.service = UserService(UsersMock)

        def checker(value):
            if value != 'password':
                raise PasswordError()

        User.check_password = Mock(side_effect=checker)

    @classmethod
    def tearDownClass(cls):
        PasswordHash.generate = copy(cls.mocked_checker)

    def test_get_account(self):
        for id in users_by_id.keys():
            self.assertEqual(users_by_id[id], self.service.get_account(user_id=id))

        for id in invalid_id:
            self.assertRaises(NotFoundError, self.service.get_account, id)

    def test_get_accounts(self):
        for admin_id, user in users_by_id.items():
            if user.email_status == EmailStatus.CONFIRMED and user.role in (Role.OWNER, Role.ADMIN):
                self.assertEqual(users_by_id, self.service.get_accounts(admin_id=admin_id))
            else:
                self.assertRaises(UserAccessError, self.service.get_accounts, admin_id)

        for admin_id in invalid_id:
            self.assertRaises(NotFoundError, self.service.get_accounts, admin_id)

    def test_update_account(self):
        def next_user(_id: int):
            return users_by_id.get(_id + 1, users_by_id[0])

        User.update_password = Mock()
        for id, user in users_by_id.items():
            name, email, password = user.name, user.email, user.password
            self.service.update_account(id, UserInputData(name=name, email=email, password=password))
            self.service.update_account(id, UserInputData(name='name', email=email, password=password))
            self.service.update_account(id, UserInputData(name=name, email='email', password=password))
            self.service.update_account(id, UserInputData(name='name', email='email', password=password))

            self.assertRaises(DataUniqueError,
                              self.service.update_account, id,
                              UserInputData(name=next_user(id).name, email=email, password=password))
            self.assertRaises(DataUniqueError,
                              self.service.update_account, id,
                              UserInputData(name=name, email=next_user(id).email, password=password))
            self.assertRaises(DataUniqueError,
                              self.service.update_account,
                              id, UserInputData(name=next_user(id).name, email=next_user(id).email, password=password))

        for id in invalid_id:
            with self.assertRaises(NotFoundError):
                self.service.update_account(id, UserInputData(name='name', email='email', password='password'))

    def test_delete_account(self):
        for id in users_by_id.keys():
            self.service.delete_account(user_id=id)

        for id in invalid_id:
            self.assertRaises(NotFoundError, self.service.get_account, id)

    def test_register(self):
        for user in users_by_id.values():
            name, email = user.name, user.email
            self.assertRaises(DataUniqueError,
                              self.service.register, UserInputData(name=name, email='email', password="password"))
            self.assertRaises(DataUniqueError,
                              self.service.register, UserInputData(name='name', email=email, password="password"))
            self.assertRaises(DataUniqueError,
                              self.service.register, UserInputData(name=name, email=email, password="password"))
            self.service.register(UserInputData(name='name', email='email', password="password"))

    def test_login_by_name(self):
        self.assertRaises(LoginError,
                          self.service.login_by_name, UserInputData(name="invalid", password="password", email=""))

        self.assertRaises(LoginError,
                          self.service.login_by_name, UserInputData(name="invalid", password="invalid", email=""))

        for name, user in users_by_name.items():
            self.assertRaises(LoginError,
                              self.service.login_by_name,
                              UserInputData(name=name, password="invalid", email=user.email))

            self.assertRaises(LoginError,
                              self.service.login_by_name, UserInputData(name=name, password="invalid", email=""))

            if user.email_status == EmailStatus.CONFIRMED:
                self.assertEqual(user.id,
                                 self.service.login_by_name(UserInputData(name=name, password="password", email="")))
                self.assertEqual(user.id,
                                 self.service.login_by_name(
                                     UserInputData(name=name, password="password", email=user.email)))
            else:
                self.assertRaises(UnconfirmedEmailError,
                                  self.service.login_by_name, UserInputData(name=name, password="password", email=""))

    def test_login_by_email(self):
        self.assertRaises(LoginError,
                          self.service.login_by_email, UserInputData(email="invalid", password="password", name=""))
        self.assertRaises(LoginError,
                          self.service.login_by_email, UserInputData(email="invalid", password="invalid", name=""))
        for email, user in users_by_email.items():
            self.assertRaises(LoginError,
                              self.service.login_by_email, UserInputData(email=email, password="invalid", name=""))
            self.assertRaises(LoginError,
                              self.service.login_by_email,
                              UserInputData(email=email, password="invalid", name=user.name))

            if user.email_status == EmailStatus.CONFIRMED:
                self.assertEqual(
                    user.id,
                    self.service.login_by_email(UserInputData(email=email, password="password", name=""))
                )
                self.assertEqual(
                    user.id,
                    self.service.login_by_email(UserInputData(email=email, password="password", name=user.name))
                )
            else:
                self.assertRaises(UnconfirmedEmailError,
                                  self.service.login_by_email, UserInputData(email=email, password="password", name=""))

    def test_reset_password(self):
        for _uuid, user in users_by_uuid.items():
            self.service.reset_password(_uuid, 'new_password')
            self.assertTrue(check_password_hash(user.password, 'new_password'))
        for _ in range(10):
            self.assertRaises(NotFoundError,
                              self.service.reset_password, uuid.uuid4(), 'new_password')

    def test_confirm_email(self):  # TODO
        for _uuid, user in users_by_uuid.items():
            self.service.confirm_email(_uuid)
            user.check_email_confirm()
        for _ in range(10):
            self.assertRaises(NotFoundError,
                              self.service.confirm_email, uuid.uuid4())
