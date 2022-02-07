from abc import ABC, abstractmethod
from typing import ByteString, List


class AbstractStorage(ABC):
    loaded_paths: List[str, ...]

    @abstractmethod
    def send(self, filename: str, data: ByteString) -> str:
        """Send binary to the storage."""

    @abstractmethod
    def delete(self, path: str) -> None:
        """Delete binary on the path from storage."""


class S3Storage(AbstractStorage):  # TODO - realize
    pass
