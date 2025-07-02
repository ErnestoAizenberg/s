from datetime import datetime, timedelta, timezone

from fastapi.responses import Response
from jose import jwt
from models.user import User
from settings import settings
from v1.auth.service_jwt import verify_password


def create_tokens(data: dict) -> dict:
    # Текущее время в UTC
    now = datetime.now(timezone.utc)

    # AccessToken - 30 минут
    access_expire = now + timedelta(days=1)
    access_payload = data.copy()
    access_payload.update({"exp": int(access_expire.timestamp()), "type": "access"})
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # RefreshToken - 7 дней
    refresh_expire = now + timedelta(days=7)
    refresh_payload = data.copy()
    refresh_payload.update({"exp": int(refresh_expire.timestamp()), "type": "refresh"})
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": access_token, "refresh_token": refresh_token}


async def authenticate_user(user, password):
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def set_tokens_to_response(response: Response, user: User):
    new_tokens = create_tokens(
        data={
            "user_id": str(user.id),
            "role": user.role,
        }
    )
    access_token = new_tokens.get("access_token")
    refresh_token = new_tokens.get("refresh_token")
    secure = settings.MODE in ["PROD", "TEST"]

    response.set_cookie(
        key="user_access_token",
        value=access_token,
        httponly=True,
        secure=secure,
        samesite="lax",
    )

    response.set_cookie(
        key="user_refresh_token",
        value=refresh_token,
        httponly=True,
        secure=secure,
        samesite="lax",
    )
