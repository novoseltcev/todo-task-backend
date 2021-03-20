# Валидация данных, простая сериализация
from marshmallow import Schema, fields, validates, ValidationError

from server.config import Config


class FileSchema(Schema):
    id = fields.Integer(required=True)
    id_task = fields.Integer(required=True)
    name = fields.String(required=True)
    path = fields.String(required=True, dump_only=True)
    data = fields.Raw(load_only=True)

    @validates('id')
    @validates('id_task')
    def validate_id_or_task(self, value):
        if value < 1:
            raise ValidationError('field must be greater or equal 1')

    @staticmethod
    def validate_text_field(value, max_size):
        length = len(value)
        if length > max_size or length < 1:
            raise ValidationError('text-field should have size = {1, .., ' + str(max_size) + '}')

    @validates('name')
    def validate_filename(self, value):
        self.validate_text_field(value, Config.filename_len)

    @validates('path')
    def validate_filename(self, value):
        self.validate_text_field(value, Config.files_dir_len + Config.filename_len)
