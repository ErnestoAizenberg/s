from dataclasses import dataclass

from models.city import City
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from v1.dao.database import Base, str_uniq


@dataclass
class Region(Base):
    name: Mapped[str_uniq]

    picture_id: Mapped[int | None] = mapped_column(
        ForeignKey("files.id", ondelete="SET NULL", use_alter=True, name="fk_region_picture_id"),  # noqa F821
        nullable=True,
        unique=True,
    )

    picture: Mapped["File | None"] = relationship(  # noqa F821
        "File",
        back_populates="region",
        lazy="joined",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    # Внешний ключ для страны
    country_id: Mapped[int] = mapped_column(ForeignKey("countrys.id"), nullable=False)
    country: Mapped["Country"] = relationship("Country", back_populates="regions", lazy="joined")  # noqa F821

    # Связь с городами
    citys: Mapped[list["City"]] = relationship("City", back_populates="region")
    funds: Mapped[list["Fund"]] = relationship("Fund", back_populates="region")  # imported in __init__.py # noqa F821

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    @property
    def picture_url(self) -> str | None:
        return self.picture.url if self.picture else None
