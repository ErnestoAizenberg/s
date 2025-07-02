from settings import settings
from v1.client.interfaces import S3ClientUseCaseProtocol
from v1.client.s3_client import S3ClientImpl


def get_s3_client() -> S3ClientUseCaseProtocol:
    return S3ClientImpl(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_ENDPOINT_URL,
        bucket_name=settings.S3_BUCKET_NAME,
    )
