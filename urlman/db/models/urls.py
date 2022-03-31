from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from urlman.db.base import Base
from urlman.db.mixins import SoftDeleteMixin, TimeStampMixin, UUIDMixin


class UrlModel(UUIDMixin, TimeStampMixin, SoftDeleteMixin, Base):
    """Url db model."""

    __tablename__ = "urls"

    url = Column(
        String(length=255),
        nullable=False,
    )
    short_code = Column(
        String(length=255),
        unique=True,
        nullable=False,
    )
    is_protected = Column(
        Boolean(),
        default=False,
    )
    key = Column(
        String(255),
        nullable=True,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
    )
    user = relationship(
        "UserModel",
        back_populates="urls",
    )
    transitions = relationship(
        "TransitionModel",
        back_populates="url",
    )
