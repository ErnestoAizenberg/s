import uuid
from datetime import datetime

from pydantic import BaseModel
from pydantic_core import Url
from v1.payment.enums import PaymentStatusEnum


class PaymentCreateSchema(BaseModel):
    id: uuid.UUID
    amount: float
    income_amount: float
    test: bool = True
    status: PaymentStatusEnum = PaymentStatusEnum.PENDING
    user_id: int
    project_id: int
    stage_id: int
    created_at: datetime
    captured_at: datetime

    class Config:
        use_enum_values = True


class YooPaymentUrlSchema(BaseModel):
    redirect_url: Url


class YooAmount(BaseModel):
    currency: str
    value: float


class YooThreeDSecure(BaseModel):
    applied: bool
    challenge_completed: bool
    method_completed: bool


class YooAuthorizationDetails(BaseModel):
    auth_code: str
    rrn: str
    three_d_secure: YooThreeDSecure


class YooMetadataInputSchema(BaseModel):
    project_id: str
    user_id: str


class YooMetadataCallbackSchema(BaseModel):
    project_id: int
    user_id: int


class YooWebhookDataSchema(BaseModel):
    amount: YooAmount
    authorization_details: YooAuthorizationDetails
    captured_at: datetime
    created_at: datetime
    description: str
    id: uuid.UUID
    income_amount: YooAmount
    metadata: YooMetadataCallbackSchema
    paid: bool
    status: PaymentStatusEnum = PaymentStatusEnum.PENDING
    test: bool
