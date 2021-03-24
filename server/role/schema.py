from marshmallow import Schema, fields


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String(required=True)

