from httpx import AsyncClient
from pydantic import BaseModel


class CookiesModel(BaseModel):
    user_access_token: str = None
    user_refresh_token: str = None


class AuthorizedClientModel(BaseModel):
    client: AsyncClient
    cookies: CookiesModel

    class Config:
        arbitrary_types_allowed = True  # чтобы AsyncClient был принят в pydantic модели
