# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validate

from server.initialize_db import DB_config


category_name_len = DB_config['category_name_len']


class CategorySchema(Schema):
    id = fields.Integer(required=True, validate=validate.Range(1))
    name = fields.String(required=True, validate=[
        validate.Length(max=category_name_len)])
    tasks = fields.List(fields.Nested('TaskSchema'),
                        dump_only=True)
