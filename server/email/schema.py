from marshmallow import Schema, fields


class EmailSchema(Schema):
    emails = fields.List(fields.Email())
    html = fields.String()
    confirm_uuid = fields.UUID()
