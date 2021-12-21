import random
import re
from string import ascii_letters
import unittest

from marshmallow.schema import ValidationError

from server.services.user.schema import UserSchema


def rand_str(length):
    return ''.join(random.choice(ascii_letters) for i in range(length))


class UserSchemaTestCase(unittest.TestCase):
    def test_load(self):
        valid_data = {
            'id': 0,
            'name': 'name',
            'email': 'example@domen.com',
            'password': 'Pa$$w0rd'
        }
        UserSchema().load(valid_data)

        data = valid_data.copy()
        data.pop('id')
        self.assertRaises(ValidationError, UserSchema().load, data)

        data = valid_data.copy()
        data.pop('name')
        self.assertRaises(ValidationError, UserSchema().load, data)

        data = valid_data.copy()
        data.pop('email')
        self.assertRaises(ValidationError, UserSchema().load, data)

        data = valid_data.copy()
        data.pop('password')
        self.assertRaises(ValidationError, UserSchema().load, data)

    def test_load_id(self):
        schema = UserSchema(only=('id',))
        self.assertRaises(ValidationError, schema.load, {})
        for value in (0, 1, -1, 2, -3):
            if value >= 0:
                self.assertEqual(value, schema.load({'id': value}).get('id'))
                self.assertEqual(value, schema.load({'id': str(value)}).get('id'))
            else:
                self.assertRaises(ValidationError, schema.load, {'id': value})
                self.assertRaises(ValidationError, schema.load, {'id': str(value)})

        for _ in range(200):
            value = random.randint(-100000000000, 1000000000000)
            if value >= 0:
                self.assertEqual(value, schema.load({'id': value}).get('id'))
                self.assertEqual(value, schema.load({'id': str(value)}).get('id'))
            else:
                self.assertRaises(ValidationError, schema.load, {'id': value})
                self.assertRaises(ValidationError, schema.load, {'id': str(value)})

    def test_load_name(self):
        schema = UserSchema(only=('name',))
        self.assertRaises(ValidationError, schema.load, {})
        for length in range(100):
            value = 'a' * length
            if len(value) >= 3:
                self.assertEqual(value, schema.load({'name': value}).get('name'))
            else:
                self.assertRaises(ValidationError, schema.load, {'name': value})

    def test_load_email(self):
        schema = UserSchema(only=('email',))
        self.assertRaises(ValidationError, schema.load, {})
        for domen in ('@gmail.com', '@ya.ru', '@outlook.com', '@gmail.ru'):
            value = rand_str(random.randint(0, 100)) + domen
            self.assertEqual(value, schema.load({'email': value}).get('email'))
        for _ in range(0, 100):
            value = rand_str(random.randint(0, 100))
            self.assertRaises(ValidationError, schema.load, {'email': value})

    def test_load_password(self):
        schema = UserSchema(only=('password',))
        self.assertRaises(ValidationError, schema.load, {})
        tests = [
            (True, 'Pa$$w0rd'),
            (False, 'Pa$$w0r d '),

            (False, 'Passw0rd'),
            (False, 'pa$sw0rd'),
            (False, 'p@asw0rd'),
            (True, 'P@ssw0rd'),
            (True, 'Pa$sw0rd'),
            (True, 'P@Ssw0rd'),

            (False, 'passwor'),
            (False, 'Passwor'),
            (False, 'pa$swor'),
            (False, 'p@aswor'),
            (False, 'P@sswor'),
            (False, 'Pa$swor'),
            (False, 'P@Sswor'),

            (False, 'password'),
            (False, 'Password'),
            (False, 'pa$sword'),
            (False, 'p@asword'),
            (False, 'P@ssword'),
            (False, 'Pa$sword'),
            (False, 'P@Ssword'),
        ]

        for expected, value in tests:
            if expected:
                value = schema.load({'password': value}).get('password')
                self.assertGreaterEqual(8, len(value))
                self.assertRegex(value, r'[0-9]')
                self.assertRegex(value, r'[a-z]')
                self.assertRegex(value, r'[A-Z]')
                self.assertRegex(value, r'[@#$%^&+=]')
                self.assertNotRegex(value, r'[^\S\n\t]+')
            else:
                self.assertRaises(ValidationError, schema.load, {'password': value})

    def test_load_uuid(self):
        schema = UserSchema(only=('uuid',))



if __name__ == '__main__':
    unittest.main()
