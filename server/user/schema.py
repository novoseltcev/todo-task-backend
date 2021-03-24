from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    login = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    reg_date = fields.Date(dump_only=True)

