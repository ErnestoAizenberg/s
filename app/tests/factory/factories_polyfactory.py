from faker import Faker
from models.user import User
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

faker = Faker()


# Базовая фабрика для SQLAlchemy
# Фабрика для создания ролей
# class RoleFactory(SQLAlchemyFactory):
#     __model__ = Role


# Фабрика для создания пользователей
class UserFactory(SQLAlchemyFactory):
    __model__ = User
    __set_relationships__ = True

    email = faker.email(domain="test.com")
