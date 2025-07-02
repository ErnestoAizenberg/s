import enum

from pydantic import BaseModel
from v1.users.enums import RoleEnum


class TokenTypeEnum(str, enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayloadSchema(BaseModel):
    user_id: int
    user_role: RoleEnum
    exp: int
    type: TokenTypeEnum
