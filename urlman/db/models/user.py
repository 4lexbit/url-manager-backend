from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from urlman.db.base import Base
from urlman.db.mixins import SoftDeleteMixin, TimeStampMixin, UUIDMixin


class UserModel(UUIDMixin, TimeStampMixin, SoftDeleteMixin, Base):
    """User db model."""

    __tablename__ = "users"

    email = Column(
        String(255),
        unique=True,
        nullable=False,
    )
    username = Column(
        String(32),
        unique=True,
        nullable=False,
    )
    password = Column(
        String(255),
        nullable=False,
    )
    first_name = Column(
        String(128),
        nullable=True,
    )
    last_name = Column(
        String(255),
        nullable=True,
    )
    last_entrance = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    urls = relationship("UrlModel", back_populates="user")
