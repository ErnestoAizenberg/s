import httpx
import pytest
from tests.conftest import auth_by
from v1.users.schemas import EmailModel


class TestUsers:
    @pytest.mark.parametrize(
        "is_authorized, status_code, response_message",
        [
            (
                True,
                200,
                {
                    "city": {"id": 1, "name": "Kazan"},
                    "email": "user1@test.com",
                    "id": 4,
                    "is_active": True,
                    "is_anonymous": False,
                    "language": "RU",
                    "name": "user1",
                    "picture_url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/tests%2Fdigits%2F2.png",
                },
            ),
            (False, 400, {"detail": "Токен отсутствует в заголовке"}),
        ],
    )
    async def test_me_200(self, ac, auth_ac, is_authorized, status_code, response_message) -> None:
        if is_authorized:
            response = await auth_ac.client.get("/app/v1/users/me", cookies=auth_ac.cookies.dict())

        else:
            response = await ac.get("/app/v1/users/me")

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
    async def test_all_users(self, ac, user_dao, email, status_code, users_count, response_message) -> None:
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

    @pytest.mark.parametrize(
        "is_authorized, file_name, content, status_code, response_expected",
        [
            (
                True,
                "file1.png",
                b"Test file content1",
                200,
                {
                    "id": 29,
                    "mime": "PNG",
                    "name": "file1",
                    "size": 18,
                    "type": "PICTURE",
                    "url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/file1.png",
                },
            ),
            (
                True,
                "file2.png",
                b"Test file content2",
                200,
                {
                    "id": 30,
                    "mime": "PNG",
                    "name": "file2",
                    "size": 18,
                    "type": "PICTURE",
                    "url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/file2.png",
                },
            ),
            (
                False,
                "file1.png",
                b"Test file content3",
                400,
                {"detail": "Токен отсутствует в заголовке"},
            ),
        ],
    )
    # TODO add test for checking the old picture deleted from S3 if it possible
    async def test_update_user_picture(
        self,
        ac,
        auth_ac,
        user_dao,
        is_authorized,
        file_name,
        content,
        status_code,
        response_expected,
    ) -> None:
        if is_authorized:
            response = await auth_ac.client.put(
                "/app/v1/users/update_logo",
                files={"picture": (file_name, content, "image/png")},
                cookies=auth_ac.cookies.dict(),
            )

            assert response.status_code == status_code
            assert response.json() == response_expected

            # Проверяем, что по ссылке действительно лежит тот же файл (байтовое сравнение)
            file_url = response_expected.get("url")
            async with httpx.AsyncClient() as client:
                file_response = await client.get(file_url)

            assert file_response.status_code == 200
            assert file_response.content == content
        else:
            response = await ac.put(
                "/app/v1/users/update_logo",
                files={"picture": (file_name, content, "image/png")},
            )

            assert response.status_code == status_code
            assert response.json() == response_expected

    @pytest.mark.parametrize(
        "authorized, status_code, response_message",
        [  # AUTHORIZED USERS
            (
                True,
                200,
                {
                    "city_id": 1,
                    "email": "updated@example.com",
                    "name": "updated",
                    "language": "RU",
                },
            ),
            (False, 400, {"detail": "Токен отсутствует в заголовке"}),
        ],
    )
    async def test_update_user(self, ac, auth_ac, user_dao, authorized, status_code, response_message) -> None:
        new_data = {
            "email": "updated@example.com",
            "name": "updated",
            "picture": "updated",
            "city_id": 1,
        }

        if authorized:
            response = await auth_ac.client.put(
                "/app/v1/users/update_data", cookies=auth_ac.cookies.dict(), json=new_data
            )

        else:
            response = await ac.put("/app/v1/users/update_data", json=new_data)

        assert response.status_code == status_code
        assert response.json() == response_message

    @pytest.mark.parametrize(
        "status_code, response_message",
        [
            (422, {"detail": "Нет города с данным city_id."}),
        ],
    )
    async def test_update_user_city_id_validation(self, ac, auth_ac, user_dao, status_code, response_message) -> None:
        data = {"email": "updated@example.com", "name": "updated", "city_id": 99}
        response = await auth_ac.client.put("/app/v1/users/update_data", cookies=auth_ac.cookies.dict(), json=data)

        assert response.status_code == status_code
        assert response.json() == response_message

    @pytest.mark.parametrize(
        "status_code, response_message",
        [
            (
                422,
                {
                    "detail": [
                        {
                            "ctx": {"expected": "'RU' or 'EN'"},
                            "input": "UZ",
                            "loc": ["body", "language"],
                            "msg": "Input should be 'RU' or 'EN'",
                            "type": "enum",
                        }
                    ]
                },
            ),
        ],
    )
    async def test_update_user_language_validation(self, ac, auth_ac, user_dao, status_code, response_message) -> None:
        data = {"language": "UZ"}
        response = await auth_ac.client.put("/app/v1/users/update_data", cookies=auth_ac.cookies.dict(), json=data)

        assert response.status_code == status_code
        assert response.json() == response_message

    @pytest.mark.parametrize(
        "status_code, input_data, response_message",
        [  # AUTHORIZED USERS
            (
                200,
                {
                    "email": "updated@example.com",
                    "name": "updated",
                    "city_id": 1,
                    "language": "EN",
                },
                {
                    "email": "updated@example.com",
                    "name": "updated",
                    "city_id": 1,
                    "language": "EN",
                },
            ),
            (
                200,
                {"city_id": 2},
                {
                    "email": "updated@example.com",
                    "name": "updated",
                    "city_id": 2,
                    "language": "EN",
                },
            ),
            (
                200,
                {"name": "updated1"},
                {
                    "email": "updated@example.com",
                    "name": "updated1",
                    "city_id": 2,
                    "language": "EN",
                },
            ),
            (
                200,
                {"email": "1updated@example.com"},
                {
                    "email": "1updated@example.com",
                    "name": "updated1",
                    "city_id": 2,
                    "language": "EN",
                },
            ),
        ],
    )
    async def test_update_user_only_single_field(
        self, ac, auth_ac, user_dao, status_code, input_data, response_message
    ) -> None:
        response = await auth_ac.client.put(
            "/app/v1/users/update_data", cookies=auth_ac.cookies.dict(), json=input_data
        )

        assert response.status_code == status_code
        assert response.json() == response_message

    async def test_delete_authorized_user(self, ac, auth_ac) -> None:
        me_response_before_deleting = await auth_ac.client.get("/app/v1/users/me", cookies=auth_ac.cookies.dict())
        assert me_response_before_deleting.status_code == 200
        assert me_response_before_deleting.json()["is_active"]

        response = await auth_ac.client.delete(
            "/app/v1/users/me",
            cookies=auth_ac.cookies.dict(),
        )
        me_response = await auth_ac.client.get("/app/v1/users/me", cookies=auth_ac.cookies.dict())

        assert response.status_code == 200
        assert response.json() == {"message": "Вы успешно удалили аккаунт!"}

        assert me_response.status_code == 200
        assert not me_response.json()["is_active"]

    async def test_delete_not_authorized_user(self, ac, auth_ac) -> None:
        response = await ac.delete("/app/v1/users/me")

        assert response.status_code == 400
        assert response.json() == {"detail": "Токен отсутствует в заголовке"}
