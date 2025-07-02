import pytest
from tests.conftest import auth_by
from v1.users.schemas import EmailModel


class TestApi:
    @pytest.mark.parametrize(
        "email, name, password, confirm_password, status_code, response_message",
        [
            (
                "user@rain.com",
                "string",
                "password",
                "password",
                200,
                {"message": "Вы успешно зарегистрированы!"},
            ),
            (
                "user@rain.com",
                "string",
                "password",
                "password1",
                422,
                None,
            ),  # password confirm validation
            ("abcde", "string", "password", "password", 422, None),  # email validation
        ],
    )
    async def test_register_by_email(
        self,
        user_dao,
        ac,
        email,
        name,
        password,
        confirm_password,
        status_code,
        response_message,
    ):
        if status_code == 200:
            assert await user_dao.count() == 5

        user_data = {
            "email": email,
            "name": name,
            "password": password,
            "confirm_password": confirm_password,
        }
        response = await ac.post("/app/v1/auth/register/", json=user_data)
        assert response.status_code == status_code
        if response_message:
            assert response.json() == response_message

        if status_code == 200:
            assert await user_dao.count() == 6

    async def test_register_by_email_after_deleting(self, session, user_dao, ac):
        assert await user_dao.count() == 6
        user_data = {
            "email": "user_after_deleting@test.com",
            "name": "string",
            "password": "password",
            "confirm_password": "password",
        }

        # Создаем пользака
        await ac.post("/app/v1/auth/register/", json=user_data)
        assert await user_dao.count() == 7
        current_user = await user_dao.find_one_or_none(filters=EmailModel(email="user_after_deleting@test.com"))
        assert current_user.is_active

        # Удаляем и проверяем что он деактивировался
        authorized_client = await auth_by(ac, current_user)
        client = authorized_client.client
        response = await client.delete("/app/v1/users/me", cookies=authorized_client.cookies.dict())
        assert response.status_code == 200
        me_response = await client.get("/app/v1/users/me", cookies=authorized_client.cookies.dict())
        assert me_response.status_code == 200
        assert not me_response.json()["is_active"]

        # На ту же почту регаем занова и проверяем что активировался
        response_after_deleting = await ac.post("/app/v1/auth/register/", json=user_data)
        assert response_after_deleting.status_code == 200
        assert response_after_deleting.json() == {"message": "Вы успешно зарегистрированы!"}

        me_response = await client.get("/app/v1/users/me", cookies=authorized_client.cookies.dict())
        assert me_response.status_code == 200
        assert me_response.json()["is_active"]

    async def test_login_anonymous(self, ac, user_dao):
        assert await user_dao.count() == 7
        response = await ac.post("/app/v1/auth/login_anonymous/")
        assert response.status_code == 200
        assert response.json() == {"message": "Анонимный пользователь добавлен"}
        assert await user_dao.count() == 8

        users = await user_dao.find_all()
        last_user = users[-1]
        assert last_user.is_anonymous

        assert response.cookies.get("user_access_token")
        assert response.cookies.get("user_refresh_token")

    @pytest.mark.parametrize(
        "email, password, status_code, response_message",
        [
            (
                "user1@test.com",
                "wrong_password",
                400,
                {"detail": "Неверная почта или пароль"},
            ),
            (
                "user1@test.com",
                "password",
                200,
                {"ok": True, "message": "Авторизация успешна!"},
            ),
        ],
    )
    async def test_login(self, ac, email, password, status_code, response_message):
        user_data = {"email": email, "password": password}
        response = await ac.post("/app/v1/auth/login/", json=user_data)
        assert response.status_code == status_code
        if response_message:
            assert response.json() == response_message

        if status_code == 200:
            assert response.cookies.get("user_access_token")
            assert response.cookies.get("user_refresh_token")

    async def test_logout(self, auth_ac):
        client = auth_ac.client

        user_access_token = client.cookies.get("user_access_token")
        user_refresh_token = client.cookies.get("user_refresh_token")
        assert user_access_token is not None
        assert user_refresh_token is not None

        response = await client.get("/app/v1/auth/logout")
        assert response.status_code == 200
        assert response.json() == {"message": "Пользователь успешно вышел из системы"}

        user_access_token = client.cookies.get("user_access_token")
        user_refresh_token = client.cookies.get("user_refresh_token")
        assert user_access_token is None
        assert user_refresh_token is None

    @pytest.mark.parametrize(
        "is_authorized, status_code, response_message",
        [
            (True, 200, {"message": "Токены успешно обновлены"}),
            (False, 400, {"detail": "Токен отсутствует в заголовке"}),
        ],
    )
    async def test_refresh_token(self, ac, auth_ac, is_authorized, status_code, response_message):
        if is_authorized:
            client = auth_ac.client
            response = await client.post("/app/v1/auth/refresh", cookies=auth_ac.cookies.dict())

        else:
            client = ac
            response = await client.post("/app/v1/auth/refresh")

        assert response.status_code == status_code
        assert response.json() == response_message

    @pytest.mark.usefixtures("prepare_database_manually")
    @pytest.mark.parametrize(
        "email, status_code, users_count, response_message",
        [  # AUTHORIZED USERS
            ("superadmin@test.com", 200, 5, None),
            ("admin@test.com", 200, 5, None),
            ("moderator@test.com", 403, None, {"detail": "Недостаточно прав"}),
            ("user1@test.com", 403, None, {"detail": "Недостаточно прав"}),
            # NOT AUTHORIZED USERS
            (None, 400, None, {"detail": "Токен отсутствует в заголовке"}),
        ],
    )
    async def test_all_users(self, ac, user_dao, email, status_code, users_count, response_message):
        if email:
            current_user = await user_dao.find_one_or_none(filters=EmailModel(email=email))
            if current_user is None:
                raise ValueError("User not found")
            authorized_client = await auth_by(ac, current_user)
            client = authorized_client.client
            response = await client.get("/app/v1/users/all", cookies=authorized_client.cookies.dict())
        else:
            response = await ac.get("/app/v1/users/all")

        assert response.status_code == status_code
        if users_count:
            assert len(response.json()) == users_count
        if response_message:
            assert response.json() == response_message
