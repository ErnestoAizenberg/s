import enum


class FileTypeEnum(str, enum.Enum):
    DOCUMENT = "DOCUMENT"
    REPORT = "REPORT"
    PICTURE = "PICTURE"


class MimeEnum(str, enum.Enum):
    PDF = "PDF"
    PNG = "PNG"
    JPEG = "JPEG"
