import uuid
from copy import deepcopy, copy
from typing import Callable, List

from mock import Mock
import pytest

from server.user.business import (
    UserService, UserInputData,
    UserRepository, User, EmailStatus, Role,
)
from server.user.business.entity import PasswordHash, UserAccessError, UnconfirmedEmailError
from server.exec.errors import NotFoundError, LoginError, DataUniqueError

list_users = [
    User.Generator.owner(0, EmailStatus.CONFIRMED),
    User.Generator.admin(1, EmailStatus.CONFIRMED),
    User.Generator.admin(2, EmailStatus.REFUSED),
    User.Generator.user(3, EmailStatus.CONFIRMED),
    User.Generator.user(4, EmailStatus.NOT_CONFIRMED),
    User.Generator.user(5, EmailStatus.REFUSED),
]
id_users = [user.id for user in list_users]
users_by_uuid = {uuid.uuid4(): user for user in list_users}
invalid_ids = [-1, max(id_users) + 1]
confirmed_users = list(filter(lambda user: user.email_status == EmailStatus.CONFIRMED, list_users))
unconfirmed_users = list(filter(lambda user: user.email_status != EmailStatus.CONFIRMED, list_users))

admin_ids = [
    user.id for user in list_users if
    user.role == Role.ADMIN and user.email_status == EmailStatus.CONFIRMED or user.role == Role.OWNER
]

not_admin_ids = [
    user.id for user in list_users if
    not (user.role == Role.ADMIN and user.email_status == EmailStatus.CONFIRMED or user.role == Role.OWNER)
]


class FakeUsers(UserRepository, Mock):
    """Mocked object, which inherited UserRepository interface."""

    def __init__(self):
        super().__init__()
        self.users = deepcopy(list_users)
        self.key_value_storage = deepcopy(users_by_uuid)

    def from_id(self, user_id):
        return copy(self.get_by_id(user_id))

    def all(self):
        return deepcopy(self.users)

    def from_name(self, name):
        return self.get(lambda user: user.name == name)

    def from_email(self, email):
        return self.get(lambda user: user.email == email)

    def from_uuid(self, token):
        try:
            return self.key_value_storage[token]
        except KeyError as error:
            raise NotFoundError() from error

    def create(self, user):
        self.not_contain_name(user.name)
        self.not_contain_email(user.email)
        user._id = self.generate_id()
        self.users.append(user)
        return user.id

    def generate_id(self):
        return max(self.users, key=lambda user: user.id).id + 1

    def not_contain_name(self, name: str):
        self.not_contain(lambda user: user.name == name)

    def not_contain_email(self, email: str):
        self.not_contain(lambda user: user.email == email)

    def update(self, user_id, user):
        old_user = self.get_by_id(user_id)
        if old_user.email != user.email:
            self.not_contain_email(user.email)
            old_user.email = user.email
        old_user._password = user.password
        old_user._email_status = user.email_status

    def delete(self, user_id):
        self.users.remove(self.get_by_id(user_id))

    def get(self, pred: Callable) -> User:
        result = list(filter(pred, self.users))
        if len(result) == 0:
            raise NotFoundError()
        return result[0]

    def get_by_id(self, user_id: int) -> User:
        return self.get(lambda user: user.id == user_id)

    def not_contain(self, pred: Callable) -> None:
        result = list(filter(pred, self.users))
        if len(result) > 0:
            raise DataUniqueError()


class TestUserService:
    """Test UserService with mocked repository"""

    def setup_method(self, method):
        self.service = UserService(FakeUsers)

    @pytest.mark.parametrize('user_id, user', [(user.id, user) for user in list_users])
    def test_get_account__found(self, user_id: int, user: User):
        assert self.service.get_account(user_id) == user

    @pytest.mark.parametrize('user_id', invalid_ids)
    def test_get_account__not_found_error(self, user_id: int):
        with pytest.raises(NotFoundError):
            self.service.get_account(user_id)

    @pytest.mark.parametrize('admin_id', admin_ids)
    def test_get_accounts__accessed(self, admin_id: int):
        assert self.service.get_accounts(admin_id=admin_id) == list_users

    @pytest.mark.parametrize('user_id', not_admin_ids)
    def test_get_accounts__user_access_error(self, user_id: int):
        with pytest.raises(UserAccessError):
            self.service.get_accounts(user_id)

    @pytest.mark.parametrize('user_id', invalid_ids)
    def test_get_accounts__not_found_error(self, user_id: int):
        with pytest.raises(NotFoundError):
            self.service.get_accounts(user_id)

    @pytest.mark.parametrize('user, email, password',
                             [(user, 'new_email-{user.id}@domen.com', user.name) for user in list_users] +
                             [(user, user.email, 'new-password') for user in list_users]
                             )
    def test_update_account__success(self, user: User, email: str, password: str):
        assert self.service.update_account(user.id, UserInputData(password, email=email)) is None
        user = self.service.get_account(user.id)
        assert user.email == email
        assert PasswordHash.check(user.password, password)

    @pytest.mark.parametrize('user_id, email, password', [(user.id, user.email, user.name) for user in list_users])
    def test_update_account__no_change(self, user_id: int, email: str, password: str):
        assert self.service.update_account(user_id, UserInputData(password, email=email)) is None
        assert self.service.get_account(user_id).email == email

    @pytest.mark.parametrize('user_id', invalid_ids)
    def test_update_account__not_found_error(self, user_id):
        with pytest.raises(NotFoundError):
            self.service.update_account(user_id, UserInputData(password='unique', email='unique'))

    def test_update_account__data_unique_error(self):
        with pytest.raises(DataUniqueError):
            self.service.update_account(1, UserInputData(password='unique', email=list_users[-1].email))

    @pytest.mark.parametrize('user_id', id_users)
    def test_delete_account__success(self, user_id: int):
        self.service.delete_account(user_id)
        with pytest.raises(NotFoundError):
            self.service.get_account(user_id)

    @pytest.mark.parametrize('user_id', invalid_ids)
    def test_delete_account__not_found_error(self, user_id: int):
        with pytest.raises(NotFoundError):
            self.service.get_account(user_id)

    def test_register__success(self):
        self.service.register(UserInputData(name='unique', email='unique@mail.com', password='password'))
        with pytest.raises(UnconfirmedEmailError):
            self.service.login_by_name(UserInputData(name='unique', password='password'))

    @pytest.mark.parametrize('name, email', [(user.name, user.email) for user in list_users])
    def test_register__data_unique_error(self, name: str, email: str):
        with pytest.raises(DataUniqueError):
            self.service.register(UserInputData(name=name, email='unique@domen.ru', password="password"))
        with pytest.raises(DataUniqueError):
            self.service.register(UserInputData(name='unique', email=email, password="password"))
        with pytest.raises(DataUniqueError):
            self.service.register(UserInputData(name=name, email=email, password="password"))

    @pytest.mark.parametrize('name, password, user_id',
                             [(user.name, user.name, user.id) for user in confirmed_users])
    def test_login_by_name__success(self, name: str, password: str, user_id: int):
        assert self.service.login_by_name(UserInputData(password, name=name)) == user_id

    @pytest.mark.parametrize('email, password, user_id',
                             [(user.email, user.name, user.id) for user in confirmed_users])
    def test_login_by_email__success(self, email: str, password: str, user_id: int):
        assert self.service.login_by_email(UserInputData(password, email=email)) == user_id

    @pytest.mark.parametrize('name, password', [(user.name, user.name) for user in unconfirmed_users])
    def test_login_by_name__unconfirmed_email_error(self, name: str, password: str):
        with pytest.raises(UnconfirmedEmailError):
            self.service.login_by_name(UserInputData(password, name=name))

    @pytest.mark.parametrize('email, password', [(user.email, user.name) for user in unconfirmed_users])
    def test_login_by_email__unconfirmed_email_error(self, email: str, password: str):
        with pytest.raises(UnconfirmedEmailError):
            self.service.login_by_email(UserInputData(password, email=email))

    @pytest.mark.parametrize('name, password',
                             [(user.name, "invalid") for user in list_users] +
                             [('invalid', user.name) for user in list_users] +
                             [('invalid', 'invalid') for user in list_users]
                             )
    def test_login_by_name__login_error(self, name: str, password: str):
        with pytest.raises(LoginError):
            self.service.login_by_name(UserInputData(name, password))

    @pytest.mark.parametrize('email, password',
                             [(user.email, "invalid") for user in list_users] +
                             [('invalid', user.name) for user in list_users] +
                             [('invalid', 'invalid') for user in list_users]
                             )
    def test_login_by_email__login_error(self, email: str, password: str):
        with pytest.raises(LoginError):
            self.service.login_by_email(UserInputData(email, password))

    @pytest.mark.parametrize('token, user', users_by_uuid.items())
    def test_reset_password__done(self, token, user):
        self.service.reset_password(token, 'new_password')
        self.service.get_account(user.id).check_password('new_password')

    @pytest.mark.parametrize('token', [str(uuid.uuid4()) for _ in range(10)])
    def test_reset_password__not_found_error(self, token: str):
        with pytest.raises(NotFoundError):
            self.service.reset_password(token, 'new_password')

    @pytest.mark.parametrize('token, user', users_by_uuid.items())
    def test_confirm_email__done(self, token, user):
        self.service.confirm_email(token)
        self.service.get_account(user.id).check_email()

    @pytest.mark.parametrize('token', [str(uuid.uuid4()) for _ in range(10)])
    def test_confirm_email__not_found_error(self, token: str):
        with pytest.raises(NotFoundError):
            self.service.confirm_email(token)
