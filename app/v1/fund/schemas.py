"""
дитейл
-айди
-название
-название региона
----фонд собрал всего
----проектов всего
-о фонде
-горячая линия тел
-адрес
-документы
-сборы активные
-сборы завершенные

ДУМАТЬ
-отчёты
"""
from pydantic import BaseModel, ConfigDict
from v1.project.schemas import FileBaseSchema, ProjectForListAPISchema


class FundDetailAPISchema(BaseModel):
    id: int
    name: str
    region_name: str
    total_collected: int
    projects_count: int
    description: str
    hot_line: str
    address: str
    documents: list[FileBaseSchema]
    projects: list[ProjectForListAPISchema]

    model_config = ConfigDict(from_attributes=True)
