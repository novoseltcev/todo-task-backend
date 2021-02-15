# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validate

from server.initialize_db import DB_config


task_title_len = DB_config['task_title_len']


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(validate=[
        validate.Length(max=task_title_len)])

    status = fields.Integer()
    category = fields.Integer(dump_only=True)





