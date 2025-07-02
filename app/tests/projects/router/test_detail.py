class TestProjectDetail:
    async def test_400_authorization(self, ac) -> None:
        response = await ac.get("/app/v1/projects/detail/1")
        assert response.status_code == 400
        assert response.json() == {"detail": "Токен отсутствует в заголовке"}

    async def test_id_validate(self, auth_ac) -> None:
        response = await auth_ac.client.get("/app/v1/projects/detail/hob", cookies=auth_ac.cookies.dict())
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "input": "hob",
                    "loc": ["path", "project_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "type": "int_parsing",
                }
            ]
        }

    async def test_id_not_exist(self, auth_ac) -> None:
        response = await auth_ac.client.get("/app/v1/projects/detail/99", cookies=auth_ac.cookies.dict())
        assert response.status_code == 404

    async def test_list_active(self, auth_ac) -> None:
        response = await auth_ac.client.get("/app/v1/projects/detail/1", cookies=auth_ac.cookies.dict())
        assert response.status_code == 200

        assert response.json() == {
            "active_stage_number": 2,
            "collected_percentage": 20,
            "description": "desc1",
            "documents": [
                {
                    "id": 1,
                    "mime": "PDF",
                    "name": "Док1 для Проекта 1",
                    "size": 123,
                    "type": "DOCUMENT",
                    "url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/tests%2Fdigits%2F1.png",
                },
                {
                    "id": 2,
                    "mime": "PDF",
                    "name": "Док2 для Проекта 1",
                    "size": 123,
                    "type": "DOCUMENT",
                    "url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/tests%2Fdigits%2F2.png",
                },
            ],
            "fund": {"id": 1, "name": "fund1", "picture_url": None},
            "goal": 10000,
            "id": 1,
            "name": "project1",
            "pictures_list": [],
            "region": {
                "name": "Tatarstan",
                "picture_url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/tests%2Fdigits%2F4.png",
            },
            "stages": [
                {
                    "collected": 2000,
                    "goal": 1000,
                    "name": "proj1 stage1",
                    "number": 1,
                    "reports": [
                        {
                            "id": 5,
                            "mime": "PDF",
                            "name": "Реп1 для Стадии 1",
                            "size": 123,
                            "type": "REPORT",
                            "url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/tests%2Fdigits%2F5.png",
                        },
                        {
                            "id": 6,
                            "mime": "PDF",
                            "name": "Реп2 для Стадии 1",
                            "size": 123,
                            "type": "REPORT",
                            "url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/tests%2Fdigits%2F6.png",
                        },
                    ],
                    "status": "finished",
                },
                {
                    "collected": 2000,
                    "goal": 2000,
                    "name": "proj1 stage2",
                    "number": 2,
                    "reports": [
                        {
                            "id": 7,
                            "mime": "PDF",
                            "name": "Реп1 для Стадии 2",
                            "size": 123,
                            "type": "REPORT",
                            "url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/tests%2Fdigits%2F7.png",
                        },
                        {
                            "id": 8,
                            "mime": "PDF",
                            "name": "Реп2 для Стадии 2",
                            "size": 123,
                            "type": "REPORT",
                            "url": "https://b35fabb0-4ffa-4a15-9f0b-c3e80016c729.selstorage.ru/tests%2Fdigits%2F8.png",
                        },
                    ],
                    "status": "active",
                },
            ],
            "status": "active",
            "total_collected": 2000,
            "unique_sponsors": 1,
        }
