from enum import Enum


class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    CANCELED = "canceled"
    WAITING_FOR_CAPTURE = "waiting_for_capture"
    SUCCEEDED = "succeeded"
