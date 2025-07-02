from exceptions import ForbiddenException
from fastapi import Request
from jose import jwt
from loguru import logger
from pydantic.v1 import EmailStr
from settings import settings
from sqladmin.authentication import AuthenticationBackend
from v1.auth.service_auth import authenticate_user, create_tokens
from v1.dependencies.dao_dep import get_session_without_commit
from v1.users.dao import UserDAO
from v1.users.schemas import EmailModel


class MyAuthenticationBackend(AuthenticationBackend):
    """Класс аутентификации для админ-панели с использованием JWT токенов."""

    async def login(self, request: Request) -> bool:
        """Обработка входа пользователя."""
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        if not email or not password:
            return False

        # Получаем сессию для работы с БД
        session_gen = get_session_without_commit()
        session = await session_gen.__anext__()

        try:
            # Ищем пользователя по email
            user_dao = UserDAO(session)
            user = await user_dao.find_one_or_none(filters=EmailModel(email=EmailStr(email)))

            if not user:
                logger.info(f"Пользователь админ панели по данному email не найден - {email}")
                return False

            # Проверяем пароль и роль пользователя
            if not await authenticate_user(user=user, password=password):
                logger.info(f"Пароль для админ панели некорректный для пользователя {user.email}")
                return False

            # Проверяем, имеет ли пользователь права администратора
            if user.role.value not in ["superuser", "fund_admin"]:
                logger.info(f"У вас недостаточно прав для доступа к админ панели. текущая роль - {user.role.value}")
                raise ForbiddenException

            new_tokens = create_tokens(data={"user_id": str(user.id), "user_role": user.role.value})
            request.session.update(
                {
                    "cookies": {
                        "user_access_token": new_tokens.get("access_token"),
                        "user_refresh_token": new_tokens.get("refresh_token"),
                    }
                }
            )
            return True

        except Exception:
            return False

        finally:
            await session.close()

    async def logout(self, request: Request) -> bool:
        # Удаляем cookies с токенами
        request.session.update({"cookies": {}})

        return True

    async def authenticate(self, request: Request) -> bool:
        """Проверка аутентификации для каждого запроса к админке."""
        # Проверяем наличие токена
        cookies = request.session.get("cookies", None)
        if cookies is not None:
            token = cookies.get("user_access_token", None)
        else:
            return False
        if not token:
            return False

        try:
            # Декодируем токен
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("user_id")
            user_role = payload.get("user_role")

            if not user_id:
                return False

            # Получаем сессию для работы с БД
            session_gen = get_session_without_commit()
            session = await session_gen.__anext__()

            try:
                # Проверяем роль пользователя
                if user_role not in ["superuser", "fund_admin"]:
                    return False

                return True

            finally:
                await session.close()

        except Exception:
            return False
