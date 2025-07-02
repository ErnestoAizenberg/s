from exceptions import FailedGoogleOauthException
from fastapi import APIRouter, Depends, HTTPException, Response
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from v1.auth.service_auth import set_tokens_to_response
from v1.auth_google.schemas import GoogleRedirectUrl
from v1.auth_google.service import google_auth_service
from v1.client.google_client import google_client
from v1.dependencies.dao_dep import get_session_with_commit

v1_google_router = APIRouter()


@v1_google_router.get("/login/", response_model=GoogleRedirectUrl)
async def google_login():
    try:
        redirect_url = google_client.google_redirect_url
        logger.error(f"Гугл авторизация \n {redirect_url}")
        return GoogleRedirectUrl(redirect_url=redirect_url)

    except Exception as e:
        logger.error(f"Error during Google authorization: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during authorization")


@v1_google_router.get("/callback/")
async def google_auth(
    code: str,
    response: Response,
    session: AsyncSession = Depends(get_session_with_commit),
):
    google_permitted_user = await google_auth_service(code, session)
    if google_permitted_user:
        set_tokens_to_response(response, google_permitted_user)
        return Response(status_code=200, content="Thanks to logging in sadaka app via Google")
    else:
        raise FailedGoogleOauthException
