from server.api.file.schema import FileSchema
from server.api.file.model import File


def serialize_file(file: File, many=False):
    return FileSchema(many=many).dump(file)
