from marshmallow import Schema, fields, EXCLUDE
from app.utils.schemas import JavaScriptMixin


class CategorySchema(Schema, JavaScriptMixin):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True)
