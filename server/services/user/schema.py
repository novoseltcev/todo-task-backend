import enum

from marshmallow import Schema, fields
from marshmallow_enum import EnumField


class Role(enum.Enum):
    owner = enum.auto()
    admin = enum.auto()
    customer = enum.auto()


class UserSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    reg_date = fields.Date(dump_only=True)
    role = EnumField(Role)
    confirmed_email = fields.Boolean(dump_only=True)

    uuid = fields.UUID(load_only=True, required=True)
