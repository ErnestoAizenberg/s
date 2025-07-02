from exceptions import ProjectNotFoundException
from fastapi import APIRouter, Depends, Query
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from v1.api_utils.pagination import Pagination, PaginationParams, PaginationResponseSchema
from v1.dependencies.auth_dep import get_current_user
from v1.dependencies.dao_dep import get_session_with_commit
from v1.project.enums import AbstractStatusEnum
from v1.project.schemas import ProjectDetailAPISchema, ProjectForListAPISchema
from v1.project.use_cases.list import ProjectListUseCase
from v1.users.dao import ProjectDAO

v1_projects_router = APIRouter()


@v1_projects_router.get("/all/{status_of_project}", response_model=PaginationResponseSchema[ProjectForListAPISchema])
async def get_projects_list(
    status_of_project: AbstractStatusEnum,
    fund_id: int = Query(default=None, alias="fund_id"),
    pagination: PaginationParams = Depends(),
    user_data: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
) -> PaginationResponseSchema[ProjectForListAPISchema]:
    project_list_use_case = ProjectListUseCase()
    projects = await project_list_use_case(status_of_project, fund_id, session)
    return await Pagination.execute(projects, pagination.page, pagination.limit)


@v1_projects_router.get("/detail/{project_id}", response_model=ProjectDetailAPISchema)
async def get_project_detail_by_id(
    project_id: int,
    user_data: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
) -> ProjectDetailAPISchema:
    project = await ProjectDAO(session=session).find_one_or_none_by_id(data_id=project_id)

    if project is not None:
        return ProjectDetailAPISchema.model_validate(project)

    else:
        raise ProjectNotFoundException
