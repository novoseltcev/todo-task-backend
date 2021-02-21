# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validates, ValidationError

from server.initialize_db import config


class CategorySchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    tasks = fields.List(fields.Nested('TaskSchema'), dump_only=True)

    @validates('id')
    def validate_id(self, value):
        if value < 1:
            raise ValidationError('field must be greater or equal 1')

    @staticmethod
    def validate_text_field(value, max_size):
        length = len(value)
        if length > max_size or length < 1:
            raise ValidationError('text-field should have size = {1, .., ' + str(max_size) + '}')

    @validates('name')
    def validate_filename(self, value):
        self.validate_text_field(value, config.category_name_len)
