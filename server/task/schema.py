# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validate

from server.initialize_db import DB_config


task_title_len = DB_config['task_title_len']


class TaskSchema(Schema):
    id = fields.Integer(validate=validate.Range(1))
    title = fields.String(required=True, validate=[
        validate.Length(max=task_title_len)])

    status = fields.Integer(default=0, dump_only=True)
    category = fields.Integer(default=1, validate=validate.Range(1))
    files = fields.List(fields.Nested('FileSchema'),
                        dump_only=True)





