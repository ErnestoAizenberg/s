from typing import Protocol


class S3ClientUseCaseProtocol(Protocol):
    async def upload_file(self, contents: bytes, key: str) -> None:
        ...

    async def delete_file(self, object_name: str) -> None:
        ...

    async def get_file(self, object_name: str) -> bytes:
        ...
