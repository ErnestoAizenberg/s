from pydantic import BaseModel, ConfigDict
from v1.file.enums import FileTypeEnum, MimeEnum
from v1.project.enums import AbstractStatusEnum


class StatusFilter(BaseModel):
    status: AbstractStatusEnum | None = None


class FundIdFilter(StatusFilter):
    fund_id: int


class RegionInfoSchema(BaseModel):
    name: str
    picture_url: str | None = None


class FileBaseSchema(BaseModel):
    id: int
    name: str
    size: int
    url: str
    type: FileTypeEnum
    mime: MimeEnum

    model_config = ConfigDict(from_attributes=True)


class FundShortSchema(BaseModel):
    id: int
    name: str
    picture_url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class StageShortSchema(BaseModel):
    number: int
    status: AbstractStatusEnum
    model_config = ConfigDict(from_attributes=True)


class StagePaymentsSchema(StageShortSchema):
    name: str
    goal: int
    collected: int
    reports: list[FileBaseSchema]


class ProjectForListAPISchema(BaseModel):
    id: int
    status: AbstractStatusEnum
    pictures_list: list[str]
    fund: FundShortSchema
    active_stage_number: int | None = None
    name: str
    goal: int
    total_collected: int
    unique_sponsors: int
    collected_percentage: int = 0

    model_config = ConfigDict(from_attributes=True)


class ProjectDetailAPISchema(ProjectForListAPISchema):
    region: RegionInfoSchema
    description: str | None = "Описание отсутствует"
    stages: list[StagePaymentsSchema]
    documents: list[FileBaseSchema]


"""
СПИСОК СБОРОВ
# id
# название сбора
# -необходимая сумма
# название фонда (ДОБАВИТЬ)
# этапы (нам нужен последний актуальный по идее только)
                    # платежи
# -собрали
# - количество спонсоров уникальных
# - процент закрытия от этапа
# - кнопка помочь
                    # этап АКТУАЛЬНЫЙ
#
# В БУДУЩЕМ---------------------------------
        Платежи
-собрали через тебя
        # ЛАЙКИ
# -Лайк от тебя на сбор стоит или нет
        # КОММЕНТЫ
# -количество коментов
#№№№ СОЦИАЛЬНЫЕ СЕТИ
# -вацап количество
# -телега количество
# -вк количество
"""

"""
СБОРЫ ДЕТАЛЬНО
"""
