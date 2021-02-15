# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validate

from server.initialize_db import DB_config


category_name_len = DB_config['category_name_len']


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[
        validate.Length(max=category_name_len)])
