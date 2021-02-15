# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validate

from server.initialize_db import DB_config


filename_len = DB_config['filename_len']
files_dir_len = DB_config['files_dir_len']


class FileSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[
        validate.Length(max=filename_len)])
    path = fields.String(required=True, validate=[
        validate.Length(max=files_dir_len + filename_len)])
