from marshmallow import Schema, fields, EXCLUDE

from app.entities.file.schema import FileSchema
from app.utils.schemas import JavaScriptMixin


class TaskSchema(Schema, JavaScriptMixin):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=False, dump_only=True)
    category_id = fields.Integer(required=True)

    name = fields.String(required=True)
    status = fields.Boolean(required=False, default=False)

    files = fields.List(
        fields.Nested(FileSchema(exclude=('task_id',)))
    )
