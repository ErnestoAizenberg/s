import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    SECRET_KEY: str
    ALGORITHM: str
    MODE: Literal["PROD", "DEV", "TEST"]

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""
    GOOGLE_TOKEN_URI: str = "https://accounts.google.com/o/oauth2/token"

    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str
    S3_ENDPOINT_URL: str
    S3_FILE_BASE_URL: str

    YOOKASSA_TEST_SECRET_KEY: str
    YOOKASSA_TEST_SHOP_ID: int

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")

    @property
    def google_redirect_url(self) -> str:
        return (
            f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
        )


# Получаем параметры для загрузки переменных среды
settings = Settings()
