from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from v1.dao.database import Base, str_uniq


@dataclass
class City(Base):
    name: Mapped[str_uniq]

    # Связь с пользователями
    users: Mapped[list["User"]] = relationship("User", back_populates="city")  # noqa F821

    # Внешний ключ для региона
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=False)
    region: Mapped["Region"] = relationship("Region", back_populates="citys", lazy="joined")  # noqa F821

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
