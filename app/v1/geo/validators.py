from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from v1.users.dao import CityDAO


async def city_id_validator(city_id: int, session: AsyncSession):
    city_dao = CityDAO(session=session)
    city = await city_dao.find_one_or_none_by_id(data_id=city_id)
    if city is None:
        raise HTTPException(status_code=422, detail="Нет города с данным city_id.")
