from dataclasses import dataclass

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from v1.api_utils.validators import validate_link_url
from v1.dao.database import Base
from v1.file.enums import FileTypeEnum, MimeEnum


@dataclass
class File(Base):
    name: Mapped[str]
    size: Mapped[int]
    url: Mapped[str]
    type: Mapped[FileTypeEnum] = mapped_column(SqlEnum(FileTypeEnum, name="file_type_enum"), nullable=False)
    mime: Mapped[MimeEnum] = mapped_column(SqlEnum(MimeEnum, name="file_mime_enum"), nullable=False)

    # OneToOne
    user_picture: Mapped["User"] = relationship(  # noqa F821
        "User", back_populates="picture", uselist=False, passive_deletes=True
    )

    region: Mapped["Region"] = relationship(  # noqa F821
        "Region", back_populates="picture", uselist=False, passive_deletes=True
    )

    fund_picture: Mapped["Fund"] = relationship(  # noqa F821
        "Fund", back_populates="picture", foreign_keys="[Fund.picture_id]", uselist=False, passive_deletes=True
    )

    # OneToMany
    fund_document_id: Mapped[int | None] = mapped_column(ForeignKey("funds.id"), nullable=True)
    fund_document: Mapped["Fund"] = relationship(  # noqa F821
        "Fund",
        back_populates="documents",
        foreign_keys=[fund_document_id],
    )

    project_document_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    project_document: Mapped["Project"] = relationship(  # noqa F821
        "Project", back_populates="documents", foreign_keys="[File.project_document_id]"
    )

    project_picture_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    project_picture: Mapped["Project"] = relationship(  # noqa F821
        "Project", back_populates="pictures", foreign_keys="[File.project_picture_id]"
    )

    stage_id: Mapped[int | None] = mapped_column(ForeignKey("stages.id"), nullable=True)
    stage: Mapped["Stage"] = relationship("Stage", back_populates="reports")  # noqa F821

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    # @validates(
    #     "fund_document_id", "project_id", "stage_id", "user_picture", "project_document_id", "project_picture_id"
    # )
    # def validate_single_target(self, key, value):
    #     user_picture = 1 if key == "user_picture" else self.user_picture
    #     fund_picture = 1 if key == "fund_picture" else self.fund_picture
    #     project_document = 1 if key == "project_document" else self.project_document
    #     region = 1 if key == "region" else self.region
    #     fund_document_id = value if key == "fund_document_id" else self.fund_document_id
    #     project_document_id = value if key == "project_document_id" else self.project_document_id
    #     project_picture_id = value if key == "project_picture_id" else self.project_picture_id
    #     stage_id = value if key == "stage_id" else self.stage_id
    #
    #     ids = [fund_picture, fund_document_id, project_document_id, project_document, project_picture_id,
    #     stage_id, user_picture, region]
    #     num_set = sum(bool(i) for i in ids)
    #
    #     if num_set == 0:
    #         raise ValueError("File must be related to at least one model (project or fund).")
    #     if num_set > 1:
    #         raise ValueError(
    #             "File must be related to only one model (project or fund or stage or user_picture) not multiple."
    #         )
    #
    #     return value

    @validates("url")
    def validate_link(self, key: str, value: str) -> str:
        return validate_link_url(value)

    @property
    def get_fullname(self):
        return self.name + "." + self.mime.value.lower()

    @property
    def picture_url(self) -> str | None:
        return self.url

    @property
    def upload(self):  # this method for sqladmin update method without uploaded picture
        return None
