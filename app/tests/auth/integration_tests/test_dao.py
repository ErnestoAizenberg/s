# async def test_add_and_get_new_user(user_dao):
#     user_data = {
#         "first_name": "first_name",
#         "last_name": "last_name",
#         "email": "user_factory@femail.com",
#         "password": "password",
#         }
#
#     # Добавление пользователя
#     new_user = await user_dao.add(values=SUserAddDB(**user_data))
#     assert new_user.id == 6
#     assert new_user is not None
