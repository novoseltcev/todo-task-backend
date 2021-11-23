from marshmallow import Schema, fields


class MailSchema(Schema):
    consumers = fields.Tuple(fields.Email(required=True), required=True)
    html = fields.String(required=True)
    subject = fields.String(required=True)
