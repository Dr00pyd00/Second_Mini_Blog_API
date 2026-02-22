from sqlalchemy import  (
    Column,
    Integer,
    String,
    Enum as sqlEnum
)
from sqlalchemy.orm import relationship
from enum import Enum as pyEnum


from app.models.mixins.status_mixin import StatusMixin
from app.models.mixins.timestamp_mixin import TimeStampMixin
from app.models.mixins.soft_delete_mixin import SoftDeleteMixin
from app.core.databse import Base


# enum for roles:
class RoleEnum(pyEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(TimeStampMixin, SoftDeleteMixin, StatusMixin, Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )

    username = Column(
        String,
        nullable=False,
        unique=True,
    )

    password = Column(
        String,
        nullable=False,
    )

    email = Column(
        String,
        nullable=True,
        unique=True,
    )

    role = Column(
        sqlEnum(RoleEnum, name="roles_enum"),
        nullable=False,
        server_default="USER",
        default=RoleEnum.USER,
    )

    # Relations:
    posts = relationship(
        "Post",
        back_populates="owner",
        cascade="all, delete-orphan"
    )