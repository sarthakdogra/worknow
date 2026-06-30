from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.user import User


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    bio: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    experience_summary: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    location_city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    location_state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    rating_avg: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    rating_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationship to User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="worker_profile",
    )