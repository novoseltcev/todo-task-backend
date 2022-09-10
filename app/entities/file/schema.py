from marshmallow import fields, EXCLUDE, Schema

from app.utils.schemas import JavaScriptMixin


class FileSchema(Schema, JavaScriptMixin):
    class Meta:
        unknown = EXCLUDE

    uuid = fields.UUID(required=False, dump_only=True)
    filename = fields.String(required=True)
    task_id = fields.Integer(required=True)

    size = fields.Integer(required=True, load_only=True)
    download_url = fields.String(required=False, dump_only=True)
    upload_url = fields.String(required=False, dump_only=True)
