from dataclasses import dataclass

from models.region import Region
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from v1.dao.database import Base, str_uniq
from v1.users.enums import LanguageEnum


@dataclass
class Country(Base):
    name: Mapped[str_uniq]
    language: Mapped[LanguageEnum] = mapped_column(
        SqlEnum(LanguageEnum, name="language_enum"),
        server_default=LanguageEnum.RU.value,
        default=LanguageEnum.RU.value,
        nullable=False,
    )

    # Связь с регионами
    regions: Mapped[list["Region"]] = relationship("Region", back_populates="country")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
