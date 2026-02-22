from enum import Enum as pyEnum
from sqlalchemy import (
    Column,
    Enum as sqlEnum
)


class StatusEnum(pyEnum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    REPORTED = "REPORTED"



class StatusMixin():

    status = Column(
        sqlEnum(StatusEnum, name="status_enum"),
        nullable=False,
        server_default="ACTIVE",
        default=StatusEnum.ACTIVE,
    )