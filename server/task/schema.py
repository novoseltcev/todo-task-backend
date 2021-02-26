# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validates, ValidationError

from server import config


class TaskSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
    status = fields.Integer(default=0)
    category = fields.Integer(default=1)
    files = fields.List(fields.Nested('FileSchema'), dump_only=True)

    @staticmethod
    def validates_int_field(value, field):
        try:
            value = int(value)
        except ValueError:
            raise ValidationError(field + ' must be Integer type')

        if value < 1:
            raise ValidationError(field + ' must be >=1')

    @staticmethod
    def validate_text_field(value, max_size):
        length = len(value)
        if length > max_size or length < 1:
            raise ValidationError('text-field should have size = {1, .., ' + str(max_size) + '}')

    @validates('id')
    def validate_id(self, value):
        self.validates_int_field(value, 'id')

    @validates('category')
    def validate_category(self, value):
        self.validates_int_field(value, 'category')

    @validates('title')
    def validate_filename(self, value):
        max_size = config.task_title_len
        length = len(value)
        if length > max_size or length < 1:
            raise ValidationError('title should have size = {1, .., ' + str(max_size) + '}')
