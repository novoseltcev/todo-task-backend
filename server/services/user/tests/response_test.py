import unittest
from datetime import date

from server.services.user.entity import Role
from server.services.user.response import *


def example_user():
    user = User.create(
        "name",
        "example@domen.com",
        "password"
    )
    User.set_id(user, 1)
    return user


class UserResponseTestCase(unittest.TestCase):
    def test_dump_not_confirmed_user(self):
        user = example_user()
        expected_dump = {
            'id': 1,
            'name': 'name',
            'email': 'example@domen.com',
            'email_status': 'not_confirmed',
            'role': 'user',
            'registration_date': str(date.today())
        }
        self.assertEqual(expected_dump, UserSerializer.dump(user))

    def test_dump_confirmed(self):
        user = example_user()
        user.confirm_email()
        expected_dump = {
            'id': 1,
            'name': 'name',
            'email': 'example@domen.com',
            'email_status': 'confirmed',
            'role': 'user',
            'registration_date': str(date.today())
        }
        self.assertEqual(expected_dump, UserSerializer.dump(user))

    def test_dump_refused(self):
        user = example_user()
        user.refuse_email()
        expected_dump = {
            'id': 1,
            'name': 'name',
            'email': 'example@domen.com',
            'email_status': 'refused',
            'role': 'user',
            'registration_date': str(date.today())
        }
        self.assertEqual(expected_dump, UserSerializer.dump(user))

    def test_dump_admin(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password",
            Role.ADMIN
        )
        User.set_id(user, 2)

        expected_dump = {
            'id': 2,
            'name': 'name',
            'email': 'example@domen.com',
            'email_status': 'refused',
            'role': 'admin',
            'registration_date': str(date.today())
        }

        self.assertEqual(expected_dump, UserSerializer.dump(user))

    def test_dump_owner(self):
        user = User.create(
            "name",
            "example@domen.com",
            "password",
            Role.OWNER
        )
        User.set_id(user, 3)

        expected_dump = {
            'id': 3,
            'name': 'name',
            'email': 'example@domen.com',
            'email_status': 'refused',
            'role': 'owner',
            'registration_date': str(date.today())
        }

        self.assertEqual(expected_dump, UserSerializer.dump(user))

    def test_dump_many(self):
        user: User = example_user()
        expected_dump = {
            'id': 1,
            'name': 'name',
            'email': 'example@domen.com',
            'email_status': 'not_confirmed',
            'role': 'user',
            'registration_date': str(date.today())
        }
        self.assertEqual([expected_dump] * 3, UserSerializer.dump_many((user,) * 3))


if __name__ == '__main__':
    unittest.main()
