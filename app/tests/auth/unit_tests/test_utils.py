import datetime

import pytest
from jose import jwt
from models.user import User
from settings import settings
from v1.auth.service_auth import authenticate_user, create_tokens
from v1.users.schemas import EmailModel, SUserAddDB


class TestUtils:
    @pytest.mark.parametrize("user_id", ["123", "456"])
    async def test_create_token_success(self, user_id):
        # Данные для теста
        data = {"user_id": user_id}

        # Создание токенов
        new_tokens = create_tokens(data)

        # Проверка, что токены были созданы
        assert new_tokens.get("access_token")
        assert new_tokens.get("refresh_token")

        now = datetime.datetime.now(datetime.timezone.utc)

        # Проверка времени истечения токенов
        access_expire = now + datetime.timedelta(days=1)
        refresh_expire = now + datetime.timedelta(days=7)

        # Декодируем access_token и проверяем его содержимое
        decoded_access = jwt.decode(
            new_tokens.get("access_token"),
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        assert decoded_access["user_id"] == user_id
        assert decoded_access["type"] == "access"
        assert decoded_access["exp"] == int(access_expire.timestamp())

        # Декодируем refresh_token и проверяем его содержимое
        decoded_refresh = jwt.decode(
            new_tokens.get("refresh_token"),
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        assert decoded_refresh["user_id"] == user_id
        assert decoded_refresh["type"] == "refresh"
        assert decoded_refresh["exp"] == int(refresh_expire.timestamp())

    async def test_authenticate_user(self, user_dao):
        user_data_dict = {
            "email": "test12@test.com",
            "name": "test12",
            "password": "12345",
        }

        await user_dao.add(values=SUserAddDB(**user_data_dict, is_active=True))
        user = await user_dao.find_one_or_none(filters=EmailModel(email="test12@test.com"))

        authenticated = await authenticate_user(user=user, password="12345")
        assert isinstance(authenticated, User)

        authenticated = await authenticate_user(user=user, password="1234")
        assert authenticated is None
