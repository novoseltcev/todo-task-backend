import unittest

from server.services.user.entity import *


class UserEntityTestCase(unittest.TestCase):
    def test_change_email(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual("example@domen.com", user.email)
        user.change_email("st.a.novoseltcev@gmail.com", "password")
        self.assertEqual("st.a.novoseltcev@gmail.com", user.email)

        with self.assertRaises(InvalidEmailError):
            user.change_email("invalid_email", "password")

        with self.assertRaises(InvalidPasswordError):
            user.change_email("st.a.novoseltcev@gmail.com", "invalid_password")

    def test_change_password(self):
        user = User.create(
            "name",
            "example@domen.com",
            "old_password"
        )
        user.change_password("new_password", "old_password")
        with self.assertRaises(InvalidPasswordError):
            self.assertTrue(check_password_hash(user.password_hash, "new_password"))
            user.change_password("new2_password", "old_password")

    def test_confirm_email(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        with self.assertRaises(UnconfirmedEmailError):
            user.check_email_confirm()

        user.confirm_email()
        user.check_email_confirm()

    def test_reg_date(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual(date.today(), user.registration_date)
        self.assertNotEqual(date(1999, 9, 9), user.registration_date)

    def test_refuse_email(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual(EmailStatus.NOT_CONFIRMED, user.email_status)
        user.refuse_email()
        self.assertEqual(EmailStatus.REFUSED, user.email_status)

    def test_admin_access(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        with self.assertRaises(AdminRequiredError):
            user.admin_access()
        user = User.create(
            "name",
            "example@domen.com",
            "password",
            Role.ADMIN
        )
        user.admin_access()
        user = User.create(
            "name",
            "example@domen.com",
            "password",
            Role.OWNER
        )
        user.admin_access()


if __name__ == '__main__':
    unittest.main()
