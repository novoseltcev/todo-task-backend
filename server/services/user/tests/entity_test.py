import unittest

from server.services.user.entity import *


class UserEntityTestCase(unittest.TestCase):
    def test_property_id(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual(-1, user.id)
        User.set_id(user, 1)
        self.assertNotEqual(-1, user.id)
        self.assertEqual(1, user.id)

    def test_property_name(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual("name", user.name)
        user.name = "new name"
        self.assertNotEqual("name", user.name)
        self.assertEqual("new name", user.name)

    def test_property_email(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertEqual("example@domen.com", user.email)

    def test_property_password(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password"
        )
        self.assertTrue(check_password_hash(user.password_hash, "password"))

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
        user.update_email("st.a.novoseltcev@gmail.com", "password")
        self.assertEqual("st.a.novoseltcev@gmail.com", user.email)
        self.assertRaises(InvalidEmailError, user.update_email, "invalid_email", "password")
        self.assertRaises(InvalidPasswordError, user.update_email, "st.a.novoseltcev@gmail.com", "invalid_password")

    def test_change_password(self):
        user = User.create(
            "name",
            "example@domen.com",
            "old_password"
        )
        user.update_password("new_password", "old_password")
        self.assertTrue(check_password_hash(user.password_hash, "new_password"))
        self.assertRaises(InvalidPasswordError, user.update_password, "new2_password", "old_password")

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
