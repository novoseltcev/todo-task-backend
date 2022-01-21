from typing import Tuple

from server.error.errors import (
    NotFoundError,
    LoginError,
)

from .entity import UnconfirmedEmailError
from .interactor import (
    AccountInteractor, AccountInputData,
    AccountRepository, Account,
)


class AccountService(AccountInteractor):
    """Implementation of the interface for interacting with the User's business logic"""

    def get(self, identity: int) -> Account:
        return self.accounts.from_id(identity)

    def get_all(self, admin_identity: int) -> Tuple[Account, ...]:
        user = self.accounts.from_id(admin_identity)
        user.admin_access()
        return self.accounts.all()

    def update(self, identity: int, data: AccountInputData):
        user = self.accounts.from_id(identity)
        user.password = data.password
        user.email = data.email
        self.accounts.update(user)

    def mark_for_deletion(self, identity: int):
        account = self.accounts.from_id(identity)
        account.status = Account.Status.DELETED
        # account.delete_date =
        self.accounts.update(account)

    def delete(self, identity):
        self.accounts.delete(self.accounts.from_id(identity))

    def register(self, data: AccountInputData):
        user = Account.create(name=data.name, email=data.email, password=data.password)
        self.accounts.create(user)

    def login_by_name(self, data: AccountInputData) -> int:
        try:
            user = self.accounts.from_name(data.name)
            user.check_password(data.password)
            user.check_email()
            return user.id
        except (NotFoundError, PasswordError) as exc:
            raise LoginError("Not found account") from exc
        except UnconfirmedEmailError as exc:
            raise UnconfirmedEmailError("Account not confirmed") from exc

    def login_by_email(self, data: AccountInputData) -> int:
        try:
            user = self.accounts.from_email(data.email)
            user.check_password(data.password)
            user.check_email()
            return user.id
        except (NotFoundError, PasswordError) as exc:
            raise LoginError("Not found account") from exc
        except UnconfirmedEmailError as exc:
            raise UnconfirmedEmailError("Account not confirmed") from exc

    def reset_password(self, token: str, password: str):
        user = self.accounts.from_uuid(token)
        user.password = password
        self.accounts.update(user.id, user)

    def confirm_email(self, uuid: str):
        user = self.accounts.from_uuid(uuid)
        user.confirm()
        self.accounts.update(user.id, user)
