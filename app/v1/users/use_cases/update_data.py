from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from v1.geo.validators import city_id_validator
from v1.users.dao import UserDAO
from v1.users.schemas import EmailModel, UserDataUpdateSchema


class UserDataUpdateUseCase:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users_dao = UserDAO(session=session)

    async def __call__(self, user: User, update_data: UserDataUpdateSchema) -> UserDataUpdateSchema:
        if hasattr(update_data, "city_id") and update_data.city_id:
            await city_id_validator(city_id=update_data.city_id, session=self.session)

        await self.users_dao.update(filters=EmailModel(email=user.email), values=update_data)

        updated_user = await self.users_dao.find_one_or_none_by_id(data_id=user.id)
        validated_data = UserDataUpdateSchema(
            name=updated_user.name,
            city_id=updated_user.city_id,
            email=updated_user.email,
            language=updated_user.language,
        )
        return validated_data
