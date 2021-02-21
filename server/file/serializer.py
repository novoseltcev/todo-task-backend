# Серилазизация данных
from .schema import FileSchema
from .model import File


def serialize_file(file: File, many=False):
    return FileSchema(many=many).dump(file)
