from exceptions import FileNameNotProvidedException, FileNotFoundS3Exception
from v1.client.interfaces import S3ClientUseCaseProtocol


class S3DownloadUseCaseImpl:
    def __init__(self, s3_client: S3ClientUseCaseProtocol):
        self.s3_client = s3_client

    async def __call__(self, file_name: str) -> bytes:
        if not file_name:
            raise FileNameNotProvidedException

        contents = await self.s3_client.get_file(object_name=file_name)

        if contents is None:
            raise FileNotFoundS3Exception

        return contents
