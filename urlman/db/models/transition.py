from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from urlman.db.base import Base


class TransitionModel(Base):
    """Transition db model."""

    __tablename__ = "transitions"

    id = Column(
        Integer,
        primary_key=True,
    )
    ip = Column(
        String(255),
        nullable=True,
    )
    check_time = Column(
        DateTime(timezone=True),
        default=func.now(),
    )

    url_id = Column(
        UUID(as_uuid=True),
        ForeignKey("urls.id"),
    )
    url = relationship(
        "UrlModel",
        back_populates="transition",
    )
