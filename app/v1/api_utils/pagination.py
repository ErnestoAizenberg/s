import math
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, conint

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: conint(gt=0) = Query(1, description="Page number")
    limit: conint(gt=0) = Query(5, description="Number of items per page")


class PaginationResponseStateSchema(BaseModel):
    page: int
    size: int
    total_pages: int
    total_items: int


class PaginationResponseSchema(BaseModel, Generic[T]):
    items: list[T]
    state: PaginationResponseStateSchema


class Pagination:
    @staticmethod
    async def execute(queryset: list[T], page: int, limit: int) -> PaginationResponseSchema[T]:
        offset = (page - 1) * limit
        paginated_queryset = queryset[offset : offset + limit]

        return PaginationResponseSchema[T](
            items=paginated_queryset,
            state=PaginationResponseStateSchema(
                page=page,
                size=limit,
                total_pages=math.ceil(len(queryset) / limit),
                total_items=len(queryset),
            ),
        )
