from typing import Protocol

from fastapi import UploadFile
from v1.s3_storage.schemas import S3UploadedFileSchema


class S3UploadUseCaseProtocol(Protocol):
    async def __call__(self, file: UploadFile) -> S3UploadedFileSchema:
        ...


class S3DeleteUseCaseProtocol(Protocol):
    async def __call__(self, file_name: str) -> None:
        ...


class S3DownloadUseCaseProtocol(Protocol):
    async def __call__(self, file_name: str) -> bytes:
        ...
