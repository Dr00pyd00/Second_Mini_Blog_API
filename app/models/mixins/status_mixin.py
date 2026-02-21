import enum as pyEnum

from sqlalchemy import (
    Column,
    Enum as sqlEnum
)


class StatusEnum(pyEnum):
    ACTIVE = 'active'
    ARCIVED = 'archived'
    REPORTED = 'reported'



class StatusMixin():

    status = Column(
        sqlEnum(StatusEnum, name="status_enum", create_type=False),
        nullable=False,
        server_default="ACTIVE",
        default=StatusEnum.ACTIVE,
    )