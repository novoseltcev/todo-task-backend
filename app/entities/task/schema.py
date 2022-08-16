from marshmallow import Schema, fields, EXCLUDE

from app.utils.schemas import JavaScriptMixin


class TaskSchema(Schema, JavaScriptMixin):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True)
    category_name = fields.String(required=True)

    title = fields.String(required=True)
    status = fields.Boolean(required=True, default=False)
    files = fields.List(fields.Nested('FileSchema'), dump_only=True)
