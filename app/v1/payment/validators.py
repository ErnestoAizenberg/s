from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from v1.users.dao import ProjectDAO


async def project_id_validator(project_id: int, session: AsyncSession):
    project_dao = ProjectDAO(session=session)
    city = await project_dao.find_one_or_none_by_id(data_id=project_id)
    if city is None:
        raise HTTPException(status_code=422, detail="Нет сущности с данным project_id.")
