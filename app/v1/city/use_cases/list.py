from sqlalchemy.ext.asyncio import AsyncSession
from v1.city.schemas import CityForListSchema
from v1.users.dao import CityDAO


class CityListUseCase:
    async def execute(self, session: AsyncSession) -> list[CityForListSchema]:
        filtered_cities = await CityDAO(session=session).find_all()
        return [CityForListSchema.model_validate(project) for project in filtered_cities]
