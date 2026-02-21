
from sqlalchemy import Column, ColumnElement, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship


from app.models.mixins.status_mixin import StatusMixin
from app.models.mixins.timestamp_mixin import TimeStampMixin
from app.models.mixins.soft_delete_mixin import SoftDeleteMixin
from app.core.databse import Base


class Post(TimeStampMixin, SoftDeleteMixin, StatusMixin, Base):

    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )

    title = Column(
        String,
        nullable=False,
    )

    content = Column(
        String,
        nullable=False,
    )

    published = Column(
        Boolean,
        nullable=False,
        server_default=text("TRUE"),
    )

    # foreign key
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # relations:
    owner = relationship("User", back_populates="posts")



