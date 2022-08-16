from marshmallow import Schema, fields, EXCLUDE

from app.utils.schemas import JavaScriptMixin


class UserSchema(Schema, JavaScriptMixin):
    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    created_at = fields.Date(dump_only=True)
