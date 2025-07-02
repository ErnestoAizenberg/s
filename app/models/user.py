from dataclasses import dataclass

from email_validator import EmailNotValidError, validate_email
from models.city import City
from models.payment import Payment
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, event, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from v1.auth.service_jwt import hash_password_in_signal
from v1.dao.database import Base
from v1.users.enums import LanguageEnum, RoleEnum


@dataclass
class User(Base):
    name: Mapped[str]
    password: Mapped[str | None]

    google_access_token: Mapped[str | None]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    language: Mapped[LanguageEnum] = mapped_column(
        SqlEnum(LanguageEnum, name="language_enum"),
        server_default=LanguageEnum.RU.value,
        default=LanguageEnum.RU.value,
        nullable=False,
    )

    role: Mapped[RoleEnum] = mapped_column(
        SqlEnum(RoleEnum, name="role_enum"),
        server_default=RoleEnum.USER.value,
        default=RoleEnum.USER,
        nullable=False,
    )

    is_anonymous: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    picture_id: Mapped[int | None] = mapped_column(ForeignKey("files.id"), nullable=True, unique=True, default=None)
    picture: Mapped["File | None"] = relationship(  # noqa F821
        "File",  # noqa F821
        back_populates="user_picture",
        lazy="joined",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    # Связь с городом
    city_id: Mapped[int] = mapped_column(ForeignKey("citys.id"), default=1, server_default=text("1"))
    city: Mapped["City"] = relationship("City", back_populates="users", lazy="joined")

    # RELATIONS
    payments: Mapped[list["Payment"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    @validates("email")
    def validate_email_field(self, key, value):
        try:
            valid = validate_email(value)
            return valid.normalized
        except EmailNotValidError as e:
            raise ValueError(f"Невалидный email: {e}")

    @property
    def picture_url(self) -> str | None:
        return self.picture.url if self.picture else None


# всегда хешируем пароль, привязываем событие перед вставкой или обновлением
event.listen(User.password, "set", hash_password_in_signal, retval=True)
