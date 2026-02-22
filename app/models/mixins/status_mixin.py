from enum import Enum as pyEnum
from sqlalchemy import (
    Column,
    Enum as sqlEnum
)


class StatusEnum(pyEnum):
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    REPORTED = 'reported'



class StatusMixin():

    status = Column(
        sqlEnum(StatusEnum, name="status_enum"),
        nullable=False,
        server_default="ACTIVE",
        default=StatusEnum.ACTIVE,
    )