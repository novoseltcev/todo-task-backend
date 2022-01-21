import unittest

from server.account.business.entity import (
    Account, Role, AccountStatus,
    AccessError,
    PasswordError,
    UnconfirmedEmailError,
)


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Account) and isinstance(right, Account) and op == "==":
        return [
            "Comparing Foo instances:",
            "   vals: {} != {}".format(left.id, right.id),
        ]


class UserEntityTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_user = Account.create(
            'name',
            'example@domen.com',
            'password'
        )

    def test_change_password(self):
        self.test_user.check_password("password")
        self.test_user.password = "new_password"
        with self.assertRaises(PasswordError):
            self.test_user.check_password("password")
        self.test_user.check_password("new_password")

    def test_refuse_email(self):
        self.assertEqual(AccountStatus.NOT_CONFIRMED, self.test_user.email_status)
        self.test_user.refuse()
        self.assertEqual(AccountStatus.REFUSED, self.test_user.email_status)

    def test_confirm_email(self):
        self.assertEqual(AccountStatus.NOT_CONFIRMED, self.test_user.email_status)
        self.test_user.confirm()
        self.assertEqual(AccountStatus.CONFIRMED, self.test_user.email_status)

    def test_change_email(self):
        self.test_confirm_email()
        self.assertEqual("example@domen.com", self.test_user.email)
        self.test_user.email = "st.a.novoseltcev@gmail.com"
        self.assertEqual("st.a.novoseltcev@gmail.com", self.test_user.email)
        self.assertEqual(AccountStatus.NOT_CONFIRMED, self.test_user.email_status)
        with self.assertRaises(UnconfirmedEmailError):
            self.test_user.check_email()

    def test_owner_access(self):
        with self.assertRaises(AccessError):
            self.test_user.owner_access()

        with self.assertRaises(AccessError):
            user = Account.create("name", "example@domen.com", "password", Role.ADMIN)
            self.assertEqual(AccountStatus.REFUSED, user.email_status)
            user.owner_access()

        user = Account.create("name", "example@domen.com", "password", Role.OWNER)
        self.assertEqual(AccountStatus.CONFIRMED, user.email_status)
        user.owner_access()

    def test_admin_access(self):
        with self.assertRaises(UnconfirmedEmailError):
            self.test_user.admin_access()

        self.test_user.confirm()
        with self.assertRaises(AccessError):
            self.test_user.admin_access()

        with self.assertRaises(UnconfirmedEmailError):
            user = Account.create("name", "example@domen.com", "password", Role.ADMIN)
            self.assertEqual(AccountStatus.REFUSED, user.email_status)
            user.admin_access()

        user.confirm()
        user.admin_access()

        user = Account.create("name", "example@domen.com", "password", Role.OWNER)
        self.assertEqual(AccountStatus.CONFIRMED, user.email_status)
        user.admin_access()


if __name__ == '__main__':
    unittest.main()
