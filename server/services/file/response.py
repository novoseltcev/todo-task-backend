from __future__ import annotations
from typing import Tuple

from .schema import FileSchema
from .model import File


class FileResponse(dict):
    @staticmethod
    def dump(file: File | Tuple[File], many=False):
        return FileResponse(FileSchema(many=many).dump(file))

    @staticmethod
    def success():
        return FileResponse(success=True)
