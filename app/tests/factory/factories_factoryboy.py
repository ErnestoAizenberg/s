import factory
from factory.alchemy import SQLAlchemyModelFactory
from models.user import User
from sqlalchemy.orm import Session


class BaseFactory(SQLAlchemyModelFactory):
    # Базовый класс для всех фабрик, которые работают с SQLAlchemy.
    # Прокидываем сессию в Meta и создаем общую логику для всех фабрик.
    class Meta:
        sqlalchemy_session_persistence = "commit"  # Настройка для сохранения объектов в БД

    @classmethod
    def set_session(cls, session: Session):
        # Устанавливаем сессию для всех фабрик.
        cls._meta.sqlalchemy_session = session


# class RoleFactory(BaseFactory):
#     class Meta:
#         model = Role
#
#     id = factory.LazyFunction(int)
#     name = factory.Faker("word")


class UserFactory(BaseFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
