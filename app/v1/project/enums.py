import enum


class AbstractStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    FINISHED = "finished"
    ALL = "all"
