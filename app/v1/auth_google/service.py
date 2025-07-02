from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from v1.auth_google.schemas import GoogleUserAddDB
from v1.client.google_client import google_client
from v1.users.dao import UserDAO
from v1.users.schemas import EmailModel, UserBase


async def google_auth_service(code: str, session: AsyncSession) -> User:
    user_data = google_client.get_google_user_info(code)
    user_dao = UserDAO(session)
    user = await user_dao.find_one_or_none(filters=EmailModel(email=user_data.email))
    update_data = GoogleUserAddDB(
        name=user_data.name,
        email=user_data.email,
        google_access_token=user_data.google_access_token,
        is_active=True,
    )
    if not user:
        authorized_user = await user_dao.add(values=update_data)
    else:
        await user_dao.update(filters=EmailModel(email=user_data.email), values=update_data)
        authorized_user = user

    return authorized_user
