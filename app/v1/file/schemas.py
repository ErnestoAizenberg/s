from pydantic import BaseModel
from v1.file.enums import FileTypeEnum, MimeEnum


class UploadedFileDataSchema(BaseModel):
    id: int
    name: str
    size: int
    url: str
    type: FileTypeEnum
    mime: MimeEnum

    # @model_validator(mode="after")
    # def validate_avatar(self, model):
    #     if model.mime != MimeEnum.JPEG:
    #         raise ValueError("Аватарка должна быть только в формате JPEG")
    #
    #     max_size = 2 * 1024 * 1024  # 2MB
    #     if model.size > max_size:
    #         raise ValueError("Размер аватара не должен превышать 2 MB")
    #
    #     if model.type != FileTypeEnum.PICTURE:
    #         raise ValueError('Тип файла для аватара должен быть "PICTURE"')
    #
    #     validate_link_url(model.url)
    #
    #     return model


# class UploadUserAvatarSchema
