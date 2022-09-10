from marshmallow import Schema, fields, EXCLUDE

from app.entities.task.schema import TaskSchema
from app.utils.schemas import JavaScriptMixin


class CategorySchema(Schema, JavaScriptMixin):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=False, dump_only=True)
    name = fields.String(required=True)
    color = fields.String(required=True)

    tasks = fields.List(
        fields.Nested(TaskSchema(exclude=('category_id', 'files')))
    )
