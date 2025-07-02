from unittest.mock import MagicMock, patch

import pytest
from v1.auth import google_auth_service
from v1.users.schemas import EmailModel, UserActiveModel


@pytest.fixture
def mock_requests_post():
    with patch("requests.post") as mock:
        yield mock


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock:
        yield mock


@pytest.fixture
def mock_google_api_responses(mock_requests_post, mock_requests_get):
    # Мокаем response от requests.post (для получения access_token)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "test_access_token"}
    mock_requests_post.return_value = mock_response

    # Мокаем response от requests.get (для получения данных пользователя)
    mock_user_info_response = MagicMock()
    mock_user_info_response.status_code = 200
    mock_user_info_response.json.return_value = {
        "name": "test_user",
        "email": "test@example.com",
        "picture": "https://www.testpicture.ru/test",
    }
    mock_requests_get.return_value = mock_user_info_response

    yield mock_requests_post, mock_requests_get


class TestGoogleAuthService:
    async def test_new_user(self, mock_google_api_responses, session, user_dao):
        mock_requests_post, mock_requests_get = mock_google_api_responses

        assert await user_dao.count() == 5

        # Вызываем функцию google_auth_service
        res = await google_auth_service(
            code="4/0AQSTgQERCWY2JwjFlIXv56vTwtVQO6NGdyIZ2J4j4tKAhzkdyAdGAxxJ-8RZIGvIrstTHQ",
            session=session,
        )

        # Проверяем, что возвращенные данные соответствуют ожиданиям
        assert res.name == "test_user"
        assert res.email == "test@example.com"
        assert res.google_access_token == "test_access_token"
        assert res.picture == "https://www.testpicture.ru/test"

        # Проверяем, что запросы к API Google были вызваны
        mock_requests_post.assert_called_once()
        mock_requests_get.assert_called_once()
        assert await user_dao.count() == 6

    async def test_update_old_user(self, mock_google_api_responses, session, user_dao):
        mock_requests_post, mock_requests_get = mock_google_api_responses

        assert await user_dao.count() == 6

        # Мокаем response от requests.get (для получения данных пользователя)
        mock_user_info_response = MagicMock()
        mock_user_info_response.status_code = 200
        mock_user_info_response.json.return_value = {
            "name": "test_user",
            "email": "superadmin@test.com",
            "picture": "https://www.testpicture.ru/test",
        }
        mock_requests_get.return_value = mock_user_info_response

        # Вызываем функцию google_auth_service
        res = await google_auth_service(
            code="4/0AQSTgQERCWY2JwjFlIXv56vTwtVQO6NGdyIZ2J4j4tKAhzkdyAdGAxxJ-8RZIGvIrstTHQ",
            session=session,
        )

        # Проверяем, что возвращенные данные соответствуют ожиданиям
        assert res.name == "test_user"
        assert res.email == "superadmin@test.com"
        assert res.google_access_token == "test_access_token"
        assert res.picture == "https://www.testpicture.ru/test"

        # Проверяем, что запросы к API Google были вызваны
        mock_requests_post.assert_called_once()
        mock_requests_get.assert_called_once()
        assert await user_dao.count() == 6

    async def test_login_after_deleting(self, mock_google_api_responses, session, user_dao):
        mock_requests_post, mock_requests_get = mock_google_api_responses

        await user_dao.update(
            filters=EmailModel(email="superadmin@test.com"),
            values=UserActiveModel(is_active=False),
        )

        current_user = await user_dao.find_one_or_none(filters=EmailModel(email="superadmin@test.com"))
        assert not current_user.is_active

        # Мокаем response от requests.get (для получения данных пользователя)
        mock_user_info_response = MagicMock()
        mock_user_info_response.status_code = 200
        mock_user_info_response.json.return_value = {
            "name": "test_user",
            "email": "superadmin@test.com",
            "picture": "https://www.testpicture.ru/test",
        }
        mock_requests_get.return_value = mock_user_info_response

        await google_auth_service(
            code="4/0AQSTgQERCWY2JwjFlIXv56vTwtVQO6NGdyIZ2J4j4tKAhzkdyAdGAxxJ-8RZIGvIrstTHQ",
            session=session,
        )

        # Проверяем, что возвращенные данные соответствуют ожиданиям
        assert current_user.is_active
