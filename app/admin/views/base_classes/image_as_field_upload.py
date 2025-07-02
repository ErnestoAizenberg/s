from admin.views.base_classes.image_as_file_singular_preview import AdminPicturePreview
from fastapi import Request, UploadFile
from v1.dependencies.s3 import get_s3_client
from v1.s3_storage.use_cases.s3_upload import S3UploadUseCaseImpl
from wtforms import FileField


class FileModelPictureUploadField(AdminPicturePreview):
    def __init__(self):
        super().__init__()
        self.s3_client = get_s3_client()

    async def scaffold_form(self, form_rules=None):
        form_class = await super().scaffold_form()
        form_class.upload = FileField()  # we always have it, but without file it size == 0
        return form_class

    async def insert_model(self, request: Request, data: dict):
        file: UploadFile = data.pop("upload")

        if file and file.filename:
            use_case = S3UploadUseCaseImpl(s3_client=self.s3_client)
            s3_file = await use_case(file=file)
            data["url"] = s3_file.url

        return await super().insert_model(request, data)

    async def update_model(self, request, pk, data):
        file: UploadFile = data.pop("upload")

        if file.size != 0:
            use_case = S3UploadUseCaseImpl(s3_client=self.s3_client)
            s3_file = await use_case(file=file)
            data["url"] = s3_file.url

        return await super().update_model(request, pk, data)
