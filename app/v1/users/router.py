from typing import List

from fastapi import APIRouter, Depends, UploadFile
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from v1.client.interfaces import S3ClientUseCaseProtocol
from v1.dependencies.auth_dep import get_current_admin_user, get_current_user
from v1.dependencies.dao_dep import get_session_with_commit
from v1.dependencies.s3 import get_s3_client
from v1.file.schemas import UploadedFileDataSchema
from v1.users.dao import UserDAO
from v1.users.schemas import SUserInfo, UserDataUpdateSchema
from v1.users.use_cases.delete_user import DeleteUserUseCase
from v1.users.use_cases.get_all_users import GetAllUsersUseCase
from v1.users.use_cases.update_data import UserDataUpdateUseCase
from v1.users.use_cases.update_logo import UserLogoUpdateUseCaseImpl

v1_users_router = APIRouter()


@v1_users_router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)) -> SUserInfo:
    return SUserInfo.model_validate(user_data)


@v1_users_router.put("/update_logo")
async def update_user_logo(
    picture: UploadFile,
    session: AsyncSession = Depends(get_session_with_commit),
    user: User = Depends(get_current_user),
    s3_client: S3ClientUseCaseProtocol = Depends(get_s3_client),
) -> UploadedFileDataSchema:
    use_case = UserLogoUpdateUseCaseImpl(session=session, s3_client=s3_client)
    updated_logo_url = await use_case(user=user, picture=picture)

    return updated_logo_url


@v1_users_router.put("/update_data")
async def update_user_data(
    update_data: UserDataUpdateSchema,
    session: AsyncSession = Depends(get_session_with_commit),
    user: User = Depends(get_current_user),
) -> UserDataUpdateSchema:
    use_case = UserDataUpdateUseCase(session=session)
    validated_data = await use_case(user=user, update_data=update_data)

    return validated_data


@v1_users_router.delete("/me")
async def delete_user(
    session: AsyncSession = Depends(get_session_with_commit),
    user: User = Depends(get_current_user),
) -> dict:
    dao = UserDAO(session)
    use_case = DeleteUserUseCase(dao)
    await use_case(user=user)

    return {"message": "Вы успешно удалили аккаунт!"}


# For admins only
@v1_users_router.get("/all")
async def get_all_users(
    session: AsyncSession = Depends(get_session_with_commit),
    user_data: User = Depends(get_current_admin_user),
) -> List[SUserInfo]:
    dao = UserDAO(session)
    use_case = GetAllUsersUseCase(dao)
    users = await use_case()

    return users
