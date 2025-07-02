from fastapi import APIRouter, Depends, Response, UploadFile
from models.user import User
from v1.client.interfaces import S3ClientUseCaseProtocol
from v1.dependencies.auth_dep import get_current_user
from v1.dependencies.s3 import get_s3_client
from v1.s3_storage.use_cases.s3_delete import S3DeleteUseCaseImpl
from v1.s3_storage.use_cases.s3_download import S3DownloadUseCaseImpl
from v1.s3_storage.use_cases.s3_upload import S3UploadUseCaseImpl

v1_s3_router = APIRouter()


@v1_s3_router.post("/upload")
async def upload(
    file: UploadFile | None = None,
    user_data: User = Depends(get_current_user),
    s3_client: S3ClientUseCaseProtocol = Depends(get_s3_client),
) -> dict:
    use_case = S3UploadUseCaseImpl(s3_client=s3_client)
    file_data = await use_case(file=file)

    return {"file_data": file_data}


@v1_s3_router.get("/{file_name}")
async def download(
    file_name: str,
    user_data: User = Depends(get_current_user),
    s3_client: S3ClientUseCaseProtocol = Depends(get_s3_client),
) -> Response:
    use_case = S3DownloadUseCaseImpl(s3_client=s3_client)
    contents = await use_case(file_name)

    return Response(
        content=contents,
        headers={"Content-Disposition": f"attachment;filename={file_name}", "Content-Type": "application/octet-stream"},
    )


@v1_s3_router.delete("/{file_name}")
async def delete(
    file_name: str,
    user_data: User = Depends(get_current_user),
    s3_client: S3ClientUseCaseProtocol = Depends(get_s3_client),
) -> dict:
    use_case = S3DeleteUseCaseImpl(s3_client=s3_client)
    await use_case(file_name)

    return {"message": "Запрос на удаление файла отправлен."}
