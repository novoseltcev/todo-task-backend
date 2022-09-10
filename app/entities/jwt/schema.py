from marshmallow import Schema, fields, post_dump, EXCLUDE

from app.utils.schemas import JavaScriptMixin


class JWTSchema(Schema, JavaScriptMixin):
    class Meta:
        unknown = EXCLUDE

    access_token = fields.String(required=True, dump_only=True)
    refresh_token = fields.String(required=True, dump_only=True)

    # @post_dump
    # def extract_token(self, data, **kwargs):
    #     for key, value in data.items():
    #         data[key] = value.token
    #     return data
