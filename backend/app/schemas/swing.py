"""
Pydantic schemas for swing-related API requests and responses.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SwingUploadRequest(BaseModel):
    """Schema for swing upload metadata (multipart fields)."""

    club: Optional[str] = Field(None, max_length=50)
    intended_shape: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)


class SwingUploadResponse(BaseModel):
    """Schema for swing upload response."""

    swing_id: int
    status: str
    message: str
    estimated_time_seconds: int


class SwingSummaryResponse(BaseModel):
    """Schema for a swing summary item in list responses."""

    id: int
    recorded_at: datetime
    club_type: Optional[str] = None
    intended_shape: Optional[str] = None
    duration_ms: Optional[int] = None
    thumbnail_url: Optional[str] = None
    status: str
    has_analysis: bool
    overall_score: Optional[float] = None

    class Config:
        from_attributes = True


class SwingDetailResponse(BaseModel):
    """Schema for detailed swing response."""

    id: int
    user_id: int
    recorded_at: datetime
    club_type: Optional[str] = None
    intended_shape: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_ms: Optional[int] = None
    status: str
    metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata_json")

    class Config:
        from_attributes = True
        populate_by_name = True
