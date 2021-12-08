from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from .entity import Role, EmailStatus


class UserSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

    uuid = fields.UUID(load_only=True, required=True)

    registration_date = fields.Date(required=True, dump_only=True)
    role = EnumField(Role, dump_only=True)
    email_status = EnumField(EmailStatus, dump_only=True)
