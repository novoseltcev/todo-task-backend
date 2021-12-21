from marshmallow import Schema, SchemaOpts, fields, validate, RAISE, INCLUDE
from marshmallow_enum import EnumField

from .entity import Role, EmailStatus


class UserSchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(min=0))
    name = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True, validate=validate.Email())

    password = fields.String(required=True, load_only=True, validate=validate.Regexp(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,}$"))
    uuid = fields.UUID(required=False, load_only=True, missing=INCLUDE, load_default=0)

    registration_date = fields.Date(required=True, dump_only=True)
    role = EnumField(Role, dump_only=True, dump_by=EnumField.VALUE)
    email_status = EnumField(EmailStatus, dump_only=True, dump_by=EnumField.VALUE)

    class Meta(SchemaOpts):
        missing = RAISE
