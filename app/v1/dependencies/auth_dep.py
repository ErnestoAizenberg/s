from datetime import datetime, timezone

from exceptions import (
    ForbiddenException,
    NoJwtException,
    NoUserIdException,
    TokenExpiredException,
    TokenNoFound,
    UserNotFoundException,
)
from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from models.user import User
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from v1.dependencies.dao_dep import get_session_without_commit
from v1.users.dao import UserDAO


def get_access_token(request: Request) -> str:
    """Извлекаем access_token из кук."""
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenNoFound
    return token


def get_access_token_from_session_for_admin_panel(request: Request) -> str:
    token = request.session.get("cookies").get("user_access_token")
    if not token:
        raise TokenNoFound
    return token


def get_refresh_token(request: Request) -> str:
    """Извлекаем refresh_token из кук."""
    token = request.cookies.get("user_refresh_token")
    if not token:
        raise TokenNoFound
    return token


async def check_refresh_token(
    token: str = Depends(get_refresh_token),
    session: AsyncSession = Depends(get_session_without_commit),
) -> User:
    """Проверяем refresh_token и возвращаем пользователя."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise NoJwtException

        user = await UserDAO(session).find_one_or_none_by_id(data_id=int(user_id))
        if not user:
            raise NoJwtException

        return user
    except JWTError:
        raise NoJwtException


async def get_current_user(
    token: str = Depends(get_access_token),
    session: AsyncSession = Depends(get_session_without_commit),
) -> User:
    """Проверяем access_token и возвращаем пользователя."""
    try:
        # Декодируем токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        # Общая ошибка для токенов
        raise NoJwtException

    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get("user_id")
    if not user_id:
        raise NoUserIdException

    user = await UserDAO(session).find_one_or_none_by_id(data_id=int(user_id))
    if not user:
        raise UserNotFoundException
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Проверяем права пользователя как администратора."""
    if current_user.role.value in ["superuser", "fund_admin"]:
        return current_user
    raise ForbiddenException
