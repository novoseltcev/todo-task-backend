# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validates, validate, ValidationError

from server.initialize_db import DB_config


task_title_len = DB_config['task_title_len']


class TaskSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
    status = fields.Integer(default=0, dump_only=True)
    category = fields.Integer(default=1)
    files = fields.List(fields.Nested('FileSchema'), dump_only=True)

    @validates('id')
    @validates('category')
    def validate_id_or_category(self, value):
        if value < 1:
            raise ValidationError('field must be greater or equal 1')

    @staticmethod
    def validate_text_field(value, max_size):
        length = len(value)
        if length > max_size or length < 1:
            raise ValidationError('text-field should have size = {1, .., ' + str(max_size) + '}')

    @validates('title')
    def validate_filename(self, value):
        self.validate_text_field(value, task_title_len)
