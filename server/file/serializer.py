# Серилазизация данных
from server.file.schema import FileSchema
from server.file.model import File


def serialize_file(file: File, many=False):
    return FileSchema(many=many).dump(file)
