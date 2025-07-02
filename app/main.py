import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from admin.register import create_admin_panel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from settings import settings
from v1.auth.router import v1_auth_router, v2_auth_router
from v1.auth_google.router import v1_google_router
from v1.city.router import v1_cities_router
from v1.fund.router import v1_funds_router
from v1.payment.router import v1_payments_router
from v1.project.router import v1_projects_router
from v1.s3_storage.router import v1_s3_router
from v1.users.router import v1_users_router
from yookassa import Configuration as YookassaConfiguration

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")

    YookassaConfiguration.configure(
        account_id=settings.YOOKASSA_TEST_SHOP_ID,
        secret_key=settings.YOOKASSA_TEST_SECRET_KEY,
    )

    create_admin_panel(app)

    yield
    logger.info("Завершение работы приложения...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Садака_app",
        lifespan=lifespan,
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Монтирование статических файлов
    # app.mount(
    #     '/static',
    #     StaticFiles(directory='app/static'),
    #     name='static'
    # )

    # Регистрация роутеров
    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    app.include_router(v1_auth_router, prefix="/app/v1/auth", tags=["Auth v1"])
    app.include_router(v2_auth_router, prefix="/app/v2/auth", tags=["Auth v2"])
    app.include_router(v1_google_router, prefix="/app/v1/google", tags=["Google OAuth v1"])
    app.include_router(v1_s3_router, prefix="/app/v1/s3_storage", tags=["S3 Storage v1"])
    app.include_router(v1_users_router, prefix="/app/v1/users", tags=["Users v1"])
    app.include_router(v1_projects_router, prefix="/app/v1/projects", tags=["Projects v1"])
    app.include_router(v1_funds_router, prefix="/app/v1/funds", tags=["Funds v1"])
    app.include_router(v1_payments_router, prefix="/app/v1/payments", tags=["Payments v1"])
    app.include_router(v1_cities_router, prefix="/app/v1/cities", tags=["Cities v1"])


# Создание экземпляра приложения
app = create_app()
