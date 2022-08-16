from marshmallow import Schema, fields, pre_load, post_dump
from stringcase import camelcase, snakecase


class AuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class JavaScriptMixin:
    @pre_load
    def to_snakecase(self, data, **kwargs):
        return {snakecase(key): value for key, value in data.items()}

    @post_dump
    def to_camelcase(self, data, **kwargs):
        return {camelcase(key): value for key, value in data.items()}

