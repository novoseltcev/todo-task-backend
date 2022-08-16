from marshmallow import Schema, fields, post_dump

from app.utils.schemas import JavaScriptMixin


class JWTSchema(Schema, JavaScriptMixin):
    access_token = fields.String(required=True, dump_only=True)
    refresh_token = fields.String(required=True, dump_only=True)

    @post_dump
    def extract_token(self, data):
        for key, value in data.items():
            data[key] = value.token
        return data
