from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from v1.dao.database import Base
from v1.payment.enums import PaymentStatusEnum


@dataclass
class Payment(Base):
    # Base info
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    captured_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    # Core data
    amount: Mapped[float | None] = mapped_column(default=None)
    income_amount: Mapped[float | None] = mapped_column(default=None)
    test: Mapped[bool] = mapped_column(default=False)

    # With default values
    status: Mapped[PaymentStatusEnum] = mapped_column(
        SqlEnum(PaymentStatusEnum, name="payment_status_enum"), default=PaymentStatusEnum.PENDING
    )

    # Project relations
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="payments", lazy="joined")  # noqa F821

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped["Project"] = relationship("Project", back_populates="payments", lazy="joined")  # noqa F821

    stage_id: Mapped[int] = mapped_column(ForeignKey("stages.id"), nullable=False)
    stage: Mapped["Stage"] = relationship("Stage", back_populates="payments", lazy="joined")  # noqa F821

    def __str__(self):
        return f"{self.project.name}, {self.income_amount}, {self.status}, test - {self.test}"
