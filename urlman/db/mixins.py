import uuid

from sqlalchemy import Boolean, Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class UUIDMixin:
    """A mixin that adds an uuid primary key."""

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


@declarative_mixin
class TimeStampMixin:
    """A mixin that adds a timestamps fields."""

    created_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
    )
    last_check = Column(
        DateTime(timezone=True),
        nullable=True,
    )


@declarative_mixin
class SoftDeleteMixin:
    """A mixin that adds a soft-delete fields."""

    is_deleted = Column(
        Boolean(),
        default=False,
    )
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )
