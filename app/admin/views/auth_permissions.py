from jose import jwt
from settings import settings
from sqladmin import ModelView
from starlette.requests import Request
from v1.auth.schemas import TokenPayloadSchema
from v1.dependencies.auth_dep import get_access_token_from_session_for_admin_panel


class SuperAdminPerm(ModelView):
    def is_accessible(self, request: Request) -> bool:
        token = get_access_token_from_session_for_admin_panel(request)
        payload_raw = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        payload = TokenPayloadSchema(**payload_raw)

        if payload.user_role in ["superuser"]:
            return True
        else:
            return False


class FundAdminAccess(ModelView):
    def is_accessible(self, request: Request) -> bool:
        token = get_access_token_from_session_for_admin_panel(request)
        payload_raw = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        payload = TokenPayloadSchema(**payload_raw)

        if payload.user_role in ["superuser", "fund_admin"]:
            return True
        else:
            return False
