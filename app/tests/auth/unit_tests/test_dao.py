from tests.factory.factories_polyfactory import faker
from v1.users.schemas import EmailModel, SUserAddDB, UserBase


class TestDAO:
    async def test_bulk_update(self, user_dao):  # DONT MOVE FROM HERE !!!
        users = await user_dao.find_all()
        for user in users:
            assert not user.name.startswith("updated_")

        for user in users:
            user.name = f"updated_{user.name}"

        res = []

        for user in users:
            user_base_instance = UserBase.model_validate(vars(user))
            res.append(user_base_instance)

        await user_dao.bulk_update(res)

        updated_users = await user_dao.find_all()
        for user in updated_users:
            assert user.name.startswith("updated_")

    async def test_add_user_and_find_by_id(self, user_dao):
        user_data_dict = {
            "email": "1test@test.com",
            "name": "test",
            "password": "8654567",
        }

        new_user = await user_dao.add(values=SUserAddDB(**user_data_dict))
        assert new_user.id == 6

        user = await user_dao.find_one_or_none_by_id(new_user.id)
        assert user.email == "1test@test.com"

    async def test_find_one_or_none(self, user_dao):
        user_data_dict = {
            "email": "2test@test.com",
            "name": "test4",
            "password": "876trfghy6t5r",
        }

        await user_dao.add(values=SUserAddDB(**user_data_dict))
        user = await user_dao.find_one_or_none(filters=EmailModel(email="2test@test.com"))
        assert user.name == "test4"

        user = await user_dao.find_one_or_none(filters=EmailModel(email="nonexistent@test.com"))
        assert user is None

    async def test_find_all(self, user_dao):
        users = await user_dao.find_all()
        assert len(users) == 7

    async def test_add_many(self, user_dao):
        users = [
            {
                "email": faker.email(domain="test.com"),
                "name": "name",
                "password": "8654567",
            }
            for i in range(10)
        ]

        new_users = await user_dao.add_many([SUserAddDB(**user_data) for user_data in users])
        assert len(new_users) == 10

    async def test_update(self, user_dao):
        user_data_dict = {
            "email": "3test@test.com",
            "name": "test3",
            "password": "8654567",
        }
        new_user = await user_dao.add(values=SUserAddDB(**user_data_dict))
        assert new_user.name == "test3"

        user_data_dict["name"] = "updated_name"
        updated_user = await user_dao.update(
            filters=EmailModel(email=new_user.email), values=UserBase(**user_data_dict)
        )
        assert updated_user == 1

        updated_user = await user_dao.find_one_or_none_by_id(new_user.id)
        assert updated_user.name == "updated_name"

    async def test_delete(self, user_dao):
        user_data_dict = {
            "email": "4test@test.com",
            "name": "test4",
            "password": "8654567",
        }
        new_user = await user_dao.add(values=SUserAddDB(**user_data_dict))
        assert new_user.name == "test4"

        deleted_user = await user_dao.delete(filters=EmailModel(email=new_user.email))
        assert deleted_user == 1

        deleted_user = await user_dao.find_one_or_none_by_id(new_user.id)
        assert deleted_user is None

    async def test_count(self, user_dao):
        count = await user_dao.count()
        assert count == 18
