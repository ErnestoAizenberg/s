class TestProjectList:
    async def test_400_authorization(self, ac) -> None:
        response = await ac.get("/app/v1/projects/all/active")
        assert response.status_code == 400
        assert response.json() == {"detail": "Токен отсутствует в заголовке"}

    async def test_list_active(self, auth_ac) -> None:
        response = await auth_ac.client.get("/app/v1/projects/all/active", cookies=auth_ac.cookies.dict())
        assert response.status_code == 200

        assert response.json() == {
            "items": [
                {
                    "active_stage_number": 2,
                    "collected_percentage": 20,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 10000,
                    "id": 1,
                    "name": "project1",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 2000,
                    "unique_sponsors": 1,
                },
                {
                    "active_stage_number": 2,
                    "collected_percentage": 10,
                    "fund": {"id": 2, "name": "fund2", "picture_url": None},
                    "goal": 20000,
                    "id": 2,
                    "name": "project2",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 2000,
                    "unique_sponsors": 1,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 6,
                    "fund": {"id": 3, "name": "fund3", "picture_url": None},
                    "goal": 30000,
                    "id": 3,
                    "name": "project3",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 2000,
                    "unique_sponsors": 1,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 40000,
                    "id": 4,
                    "name": "project4",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 2, "name": "fund2", "picture_url": None},
                    "goal": 50000,
                    "id": 5,
                    "name": "project5",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
            ],
            "state": {"page": 1, "size": 5, "total_items": 20, "total_pages": 4},
        }

    async def test_list_finished(self, auth_ac) -> None:
        response = await auth_ac.client.get("/app/v1/projects/all/finished", cookies=auth_ac.cookies.dict())

        assert response.status_code == 200
        assert response.json() == {
            "items": [
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 3, "name": "fund3", "picture_url": None},
                    "goal": 210000,
                    "id": 21,
                    "name": "project21",
                    "pictures_list": [],
                    "status": "finished",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 220000,
                    "id": 22,
                    "name": "project22",
                    "pictures_list": [],
                    "status": "finished",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 2, "name": "fund2", "picture_url": None},
                    "goal": 230000,
                    "id": 23,
                    "name": "project23",
                    "pictures_list": [],
                    "status": "finished",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 3, "name": "fund3", "picture_url": None},
                    "goal": 240000,
                    "id": 24,
                    "name": "project24",
                    "pictures_list": [],
                    "status": "finished",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 250000,
                    "id": 25,
                    "name": "project25",
                    "pictures_list": [],
                    "status": "finished",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
            ],
            "state": {"page": 1, "size": 5, "total_items": 10, "total_pages": 2},
        }

    async def test_list_all(self, auth_ac) -> None:
        response = await auth_ac.client.get("/app/v1/projects/all/all", cookies=auth_ac.cookies.dict())

        assert response.status_code == 200
        assert response.json() == {
            "items": [
                {
                    "active_stage_number": 2,
                    "collected_percentage": 20,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 10000,
                    "id": 1,
                    "name": "project1",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 2000,
                    "unique_sponsors": 1,
                },
                {
                    "active_stage_number": 2,
                    "collected_percentage": 10,
                    "fund": {"id": 2, "name": "fund2", "picture_url": None},
                    "goal": 20000,
                    "id": 2,
                    "name": "project2",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 2000,
                    "unique_sponsors": 1,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 6,
                    "fund": {"id": 3, "name": "fund3", "picture_url": None},
                    "goal": 30000,
                    "id": 3,
                    "name": "project3",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 2000,
                    "unique_sponsors": 1,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 40000,
                    "id": 4,
                    "name": "project4",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 2, "name": "fund2", "picture_url": None},
                    "goal": 50000,
                    "id": 5,
                    "name": "project5",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
            ],
            "state": {"page": 1, "size": 5, "total_items": 30, "total_pages": 6},
        }

    async def test_list_by_fund_id(self, auth_ac) -> None:
        response = await auth_ac.client.get(
            "/app/v1/projects/all/all", cookies=auth_ac.cookies.dict(), params={"fund_id": 1}
        )

        assert response.status_code == 200
        assert response.json() == {
            "items": [
                {
                    "active_stage_number": 2,
                    "collected_percentage": 20,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 10000,
                    "id": 1,
                    "name": "project1",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 2000,
                    "unique_sponsors": 1,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 40000,
                    "id": 4,
                    "name": "project4",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 70000,
                    "id": 7,
                    "name": "project7",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 100000,
                    "id": 10,
                    "name": "project10",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 130000,
                    "id": 13,
                    "name": "project13",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
            ],
            "state": {"page": 1, "size": 5, "total_items": 10, "total_pages": 2},
        }

    async def test_list_active_and_fund_id(self, auth_ac) -> None:
        response = await auth_ac.client.get(
            "/app/v1/projects/all/active", cookies=auth_ac.cookies.dict(), params={"fund_id": 1}
        )

        assert response.status_code == 200
        assert response.json() == {
            "items": [
                {
                    "active_stage_number": 2,
                    "collected_percentage": 20,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 10000,
                    "id": 1,
                    "name": "project1",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 2000,
                    "unique_sponsors": 1,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 40000,
                    "id": 4,
                    "name": "project4",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 70000,
                    "id": 7,
                    "name": "project7",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 100000,
                    "id": 10,
                    "name": "project10",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
                {
                    "active_stage_number": None,
                    "collected_percentage": 0,
                    "fund": {"id": 1, "name": "fund1", "picture_url": None},
                    "goal": 130000,
                    "id": 13,
                    "name": "project13",
                    "pictures_list": [],
                    "status": "active",
                    "total_collected": 0,
                    "unique_sponsors": 0,
                },
            ],
            "state": {"page": 1, "size": 5, "total_items": 7, "total_pages": 2},
        }


"""
Тест кейсы
-создать проект и чтобы у него были все Зконченные стадии проверять сколько в респонсе
-есть и законченные и активные
-есть только активные ???
2 - осздать различные платежи и првоерять ответы
кейс - отсутствуют этапы вообще
"""
