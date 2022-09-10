from abc import ABC, abstractmethod
import boto3

from app.config import config


class PersistentStorage(ABC):
    @abstractmethod
    def create_upload_url(self, filename: str, size: int) -> str:
        pass

    @abstractmethod
    def get_download_url(self, path: str) -> str:
        pass

    @abstractmethod
    def delete(self, path: str) -> None:
        pass


class S3Storage(PersistentStorage):
    def __init__(self, bucket_name=config.AWS_BUCKET_NAME):
        self._s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def create_upload_url(self, filename: str, size: int) -> str:
        return self._s3.generate_presigned_post(
            Bucket=self.bucket_name,
            Key=str(filename)
        ).url

    def get_download_url(self, filename: str) -> str:
        return self._s3.generate_presigned_url(
            Bucket=self.bucket_name,
            Key=str(filename)
        ).url

    def delete(self, filename: str) -> None:
        self._s3.Object(bicket_name=self.bucket_name, key=filename).delete()
