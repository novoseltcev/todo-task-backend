import unittest

from server.services.user.entity import *


class UserEntityTestCase(unittest.TestCase):
    def test_property_password(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertTrue(check_password_hash(user.password, "password"))

    def test_property_email_status(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual(EmailStatus.NOT_CONFIRMED, user.email_status)

    def test_property_role(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual(Role.USER, user.role)
        self.assertNotEqual(Role.ADMIN, user.role)
        self.assertNotEqual(Role.OWNER, user.role)

    def test_property_reg_date(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual(date.today(), user.registration_date)
        self.assertNotEqual(date(1999, 9, 9), user.registration_date)

    def test_change_email(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual("example@domen.com", user.email)
        user.update_email("st.a.novoseltcev@gmail.com")
        self.assertEqual("st.a.novoseltcev@gmail.com", user.email)
        self.assertRaises(EmailError, user.update_email, "invalid_email")

    def test_change_password(self):
        user = User.create(
            "name",
            "example@domen.com",
            "old_password"
        )
        user.update_password("new_password")
        self.assertTrue(check_password_hash(user.password, "new_password"))

    def test_confirm_email(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertRaises(UnconfirmedEmailError, user.check_email_confirm)

        user.confirm_email()
        user.check_email_confirm()

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
        self.assertRaises(AdminRequiredError, user.admin_access)
        user = User.create(
            "name",
            "example@domen.com",
            "password",
            Role.ADMIN
        )
        self.assertRaises(AdminRequiredError, user.admin_access)
        user = User.create(
            "name",
            "example@domen.com",
            "password",
            Role.ADMIN
        )
        user.confirm_email()
        user.admin_access()
        user = User.create(
            "name",
            "example@domen.com",
            "password",
            Role.OWNER
        )
        user.admin_access()
