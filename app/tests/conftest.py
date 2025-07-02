import httpx
import pytest
from httpx import ASGITransport, AsyncClient
from main import app as fastapi_app
from models.user import User
from settings import settings
from tests.schemas import AuthorizedClientModel, CookiesModel
from utils.scripts.local_db_fill import prepare_database_core
from v1.dao.database import async_session_maker
from v1.users.dao import UserDAO
from yookassa import Configuration


@pytest.fixture(autouse=True)
def setup_yookassa_config():
    Configuration.account_id = settings.YOOKASSA_TEST_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_TEST_SECRET_KEY


@pytest.fixture(scope="class", autouse=True)
async def prepare_database(session):
    assert settings.MODE == "TEST"
    await prepare_database_core(session)


@pytest.fixture(scope="class")
async def prepare_database_manually(session):
    await prepare_database_core(session)


@pytest.fixture(scope="class")
async def session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture(scope="function")
async def user_dao(session) -> UserDAO:
    user_dao = UserDAO(session)
    return user_dao


@pytest.fixture(scope="class")
async def ac():
    async with AsyncClient(transport=ASGITransport(fastapi_app), base_url="http://test/") as async_client:
        yield async_client


@pytest.fixture(scope="class")
async def auth_ac():
    async with AsyncClient(transport=ASGITransport(fastapi_app), base_url="http://test") as ac:
        await ac.post("/app/v1/auth/login/", json={"email": "user1@test.com", "password": "password"})
        assert ac.cookies["user_access_token"]

        yield AuthorizedClientModel(
            client=ac,
            cookies=CookiesModel(
                user_access_token=ac.cookies.get("user_access_token"),
                user_refresh_token=ac.cookies.get("user_refresh_token"),
            ),
        )


@pytest.fixture(scope="class")
async def authenticated_super():
    async with AsyncClient(transport=ASGITransport(fastapi_app), base_url="http://test") as ac:
        response = await ac.post(
            "/app/v1/auth/login/",
            json={"email": "superadmin@test.com", "password": "password"},
        )
        assert response.status_code == 200
        assert ac.cookies["user_access_token"]

        yield AuthorizedClientModel(
            client=ac,
            cookies=CookiesModel(
                user_access_token=ac.cookies.get("user_access_token"),
                user_refresh_token=ac.cookies.get("user_refresh_token"),
            ),
        )


async def auth_by(ac: AsyncClient, user: User):
    logout_response = await ac.post("/app/v1/auth/logout/")
    assert logout_response.status_code == 307

    login_response = await ac.post("/app/v1/auth/login/", json={"email": user.email, "password": "password"})
    assert login_response.status_code == 200
    assert isinstance(ac.cookies, httpx.Cookies)
    return AuthorizedClientModel(
        client=ac,
        cookies=CookiesModel(
            user_access_token=ac.cookies.get("user_access_token"),
            user_refresh_token=ac.cookies.get("user_refresh_token"),
        ),
    )
