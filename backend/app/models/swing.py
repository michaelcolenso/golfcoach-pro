"""
SQLAlchemy model for golf swings.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Swing(Base):
    """Swing video and analysis metadata."""

    __tablename__ = "swings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    club_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    intended_shape: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    video_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    thumbnail_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="PROCESSING", nullable=False
    )
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(
        "metadata", JSON, default=dict, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User", backref="swings")


__all__ = ["Swing"]
