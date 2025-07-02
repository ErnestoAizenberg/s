from admin.views.auth_permissions import SuperAdminPerm
from admin.views.base_classes.image_as_file_singular_preview import AdminPicturePreview
from models.region import Region
from sqladmin import ModelView


class RegionAdmin(SuperAdminPerm, AdminPicturePreview, ModelView, model=Region):
    icon = "fa-solid fa-map"
    name = "Регион"
    name_plural = "Регионы"

    form_excluded_columns = [
        "created_at",
        "updated_at",
        "funds",
    ]

    """
    Закоменитрованный код отвечает за реализацию юзкейса по замене картинки региона из формы дитейл
    её так и не удалось до конца реализовать в рабочем виде, тк непонятные оштбки с аплоад полем связанные
    предположительно надо как то удалять поле аплоад ДО того как запускается метод по обновлению полей в БД
    """

    # from typing import Any, Union, List
    #
    # from fastapi import UploadFile
    # from sqladmin._queries import Query
    # from sqladmin.fields import FileField
    # from sqlalchemy import Select
    # from starlette.requests import Request
    # from wtforms.validators import Optional
    # from v1.geo.use_cases.region.update_picture import RegionPictureUpdateUseCaseImpl
    # from v1.users.dao import RegionDAO

    # def __init__(self):
    #     super().__init__()
    #     self.s3_client = get_s3_client()

    # async def scaffold_form(self, form_rules=None):
    #     form_class = await super().scaffold_form()
    #     form_class.upload = FileField(default=None)  # we always have it, but without file it size == 0
    #     return form_class

    # async def after_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
    #     file: UploadFile| None = data.pop("upload", None)
    #
    #     if file is not None:
    #         async with self.session_maker(expire_on_commit=False) as session:
    #             region_dao = RegionDAO(session=session)
    #             region = await region_dao.find_one_or_none_by_id(data_id=model.id)
    #
    #             if file.size != 0:
    #                 use_case = RegionPictureUpdateUseCaseImpl(session=session, s3_client=self.s3_client)
    #                 uploaded_picture_url = await use_case(region=region, picture=file)
    #                 data["url"] = uploaded_picture_url.url
    #
    #             await session.commit()
