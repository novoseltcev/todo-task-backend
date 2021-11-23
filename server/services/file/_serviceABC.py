from abc import ABC, abstractmethod

from .response import FileResponse, FileSchema


class FileService(ABC):
    @classmethod
    @abstractmethod
    def get(cls, schema: FileSchema) -> FileResponse:
        pass

    @classmethod
    @abstractmethod
    def get_all(cls, schema: FileSchema) -> FileResponse:
        pass

    @classmethod
    @abstractmethod
    def pin(cls, schema: FileSchema) -> FileResponse:
        pass

    @classmethod
    @abstractmethod
    def unpin(cls, schema: FileSchema) -> FileResponse:
        pass
