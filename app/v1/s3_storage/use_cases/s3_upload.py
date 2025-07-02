from exceptions import FileNotProvidedException
from fastapi import HTTPException, UploadFile, status
from settings import settings
from v1.client.interfaces import S3ClientUseCaseProtocol
from v1.file.enums import FileTypeEnum, MimeEnum
from v1.s3_storage.schemas import S3UploadedFileSchema


class S3UploadUseCaseImpl:
    def __init__(self, s3_client: S3ClientUseCaseProtocol):
        self.s3_client = s3_client
        self.max_size_mb: int = 2
        # Маппинг расширений -> (MimeEnum, FileTypeEnum)
        self.supported_file_types = {
            "png": (MimeEnum.PNG, FileTypeEnum.PICTURE),
            "jpg": (MimeEnum.JPEG, FileTypeEnum.PICTURE),
            "jpeg": (MimeEnum.JPEG, FileTypeEnum.PICTURE),
            "pdf": (MimeEnum.PDF, FileTypeEnum.DOCUMENT),
        }

    async def __call__(self, file: UploadFile) -> S3UploadedFileSchema:
        if not file:
            raise FileNotProvidedException()

        contents = await file.read()

        # Проверка размера файла
        if not 0 < len(contents) <= self.max_size_mb * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Supported file size is 0 - {self.max_size_mb} MB",
            )

        # Извлекаем расширение
        extension = file.filename.split(".")[-1].lower()

        if extension not in self.supported_file_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f'Неподдерживаемый тип файла: {extension if extension else "Unknown"}. '
                    f'Поддерживаются только следующие типы {", ".join(self.supported_file_types.keys())}'
                ),
            )

        mime, file_type = self.supported_file_types[extension]

        await self.s3_client.upload_file(key=file.filename, contents=contents)

        validated_data = S3UploadedFileSchema(
            name=f'{file.filename.rsplit(".", 1)[0]}',
            size=len(contents),
            url=settings.S3_FILE_BASE_URL + file.filename,
            type=file_type,
            mime=mime,
        )

        return validated_data
