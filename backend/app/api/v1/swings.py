"""
Swing management endpoints for GolfCoach Pro API.

Handles swing uploads, retrieval, and analysis enqueueing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import itertools
import os
import shutil

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User


router = APIRouter(prefix="/swings", tags=["Swings"])


@dataclass
class SwingRecord:
    """In-memory representation of a swing record."""

    id: int
    user_id: int
    recorded_at: datetime
    club_type: Optional[str]
    intended_shape: Optional[str]
    notes: Optional[str]
    video_key: str
    thumbnail_key: Optional[str]
    duration_ms: Optional[int]
    status: str
    metadata: Dict[str, Optional[str]]


class SwingUploadResponse(BaseModel):
    """Response payload for swing upload."""

    swing_id: int
    status: str
    message: str
    estimated_time_seconds: int


class SwingMetadataResponse(BaseModel):
    """Metadata for uploaded swing video."""

    resolution: Optional[str] = None
    fps: Optional[int] = None
    file_size_bytes: Optional[int] = None


class SwingDetailResponse(BaseModel):
    """Detailed swing response payload."""

    id: int
    user_id: int
    recorded_at: datetime
    club_type: Optional[str] = None
    intended_shape: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    duration_ms: Optional[int] = None
    status: str
    metadata: SwingMetadataResponse


class SwingAnalyzeResponse(BaseModel):
    """Response payload for analysis enqueueing."""

    swing_id: int
    status: str
    message: str


class SwingRepository:
    """Simple in-memory swing repository for API scaffolding."""

    _id_counter = itertools.count(1)
    _records: Dict[int, SwingRecord] = {}

    @classmethod
    def create(
        cls,
        *,
        user_id: int,
        club_type: Optional[str],
        intended_shape: Optional[str],
        notes: Optional[str],
        video_key: str,
        metadata: Dict[str, Optional[str]],
    ) -> SwingRecord:
        swing_id = next(cls._id_counter)
        record = SwingRecord(
            id=swing_id,
            user_id=user_id,
            recorded_at=datetime.utcnow(),
            club_type=club_type,
            intended_shape=intended_shape,
            notes=notes,
            video_key=video_key,
            thumbnail_key=None,
            duration_ms=None,
            status="PROCESSING",
            metadata=metadata,
        )
        cls._records[swing_id] = record
        return record

    @classmethod
    def get(cls, swing_id: int) -> Optional[SwingRecord]:
        return cls._records.get(swing_id)


class StorageService:
    """Minimal storage adapter for swing video uploads."""

    @staticmethod
    def upload_video(file: UploadFile, swing_id: int) -> str:
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        extension = Path(file.filename or "").suffix.lower().lstrip(".")
        filename = f"swing-{swing_id}.{extension or 'mp4'}"
        destination = upload_dir / filename

        with destination.open("wb") as output_file:
            shutil.copyfileobj(file.file, output_file)

        return filename

    @staticmethod
    def get_signed_url(storage_key: str) -> str:
        return f"{settings.API_BASE_URL}/media/{storage_key}?signature=mock"


def _validate_upload(file: UploadFile) -> int:
    extension = Path(file.filename or "").suffix.lower().lstrip(".")
    if extension not in settings.VIDEO_ALLOWED_FORMATS_LIST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format",
        )

    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    max_size_bytes = settings.VIDEO_MAX_SIZE_MB * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large",
        )

    return file_size


@router.post(
    "/upload",
    response_model=SwingUploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_swing_video(
    video: UploadFile = File(...),
    club: Optional[str] = Form(None),
    intended_shape: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> SwingUploadResponse:
    """
    Upload a golf swing video for analysis.

    Args:
        video: Uploaded video file
        club: Optional club type
        intended_shape: Optional intended shot shape
        notes: Optional user notes
        current_user: Current authenticated user
        db: Database session

    Returns:
        Swing upload status
    """
    file_size = _validate_upload(video)

    # Placeholder for storage upload and persistence
    metadata = {
        "resolution": None,
        "fps": None,
        "file_size_bytes": file_size,
    }

    swing_record = SwingRepository.create(
        user_id=current_user.id,
        club_type=club,
        intended_shape=intended_shape,
        notes=notes,
        video_key="pending",
        metadata=metadata,
    )

    storage_key = StorageService.upload_video(video, swing_record.id)
    swing_record.video_key = storage_key

    return SwingUploadResponse(
        swing_id=swing_record.id,
        status=swing_record.status,
        message="Video uploaded successfully. Analysis in progress.",
        estimated_time_seconds=30,
    )


@router.get("/{swing_id}", response_model=SwingDetailResponse)
async def get_swing_details(
    swing_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> SwingDetailResponse:
    """
    Retrieve detailed information about a specific swing.

    Args:
        swing_id: Swing identifier
        current_user: Current authenticated user
        db: Database session

    Returns:
        Swing details with signed URLs

    Raises:
        HTTPException 404: Swing not found or unauthorized
    """
    swing_record = SwingRepository.get(swing_id)
    if swing_record is None or swing_record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Swing not found",
        )

    return SwingDetailResponse(
        id=swing_record.id,
        user_id=swing_record.user_id,
        recorded_at=swing_record.recorded_at,
        club_type=swing_record.club_type,
        intended_shape=swing_record.intended_shape,
        video_url=StorageService.get_signed_url(swing_record.video_key),
        thumbnail_url=(
            StorageService.get_signed_url(swing_record.thumbnail_key)
            if swing_record.thumbnail_key
            else None
        ),
        duration_ms=swing_record.duration_ms,
        status=swing_record.status,
        metadata=SwingMetadataResponse(**swing_record.metadata),
    )


@router.post(
    "/{swing_id}/analyze",
    response_model=SwingAnalyzeResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def analyze_swing(
    swing_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> SwingAnalyzeResponse:
    """
    Enqueue swing analysis via Celery.

    Args:
        swing_id: Swing identifier
        current_user: Current authenticated user
        db: Database session

    Returns:
        Analysis enqueue status

    Raises:
        HTTPException 404: Swing not found or unauthorized
    """
    swing_record = SwingRepository.get(swing_id)
    if swing_record is None or swing_record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Swing not found",
        )

    # TODO: Dispatch Celery task for analysis
    swing_record.status = "PROCESSING"

    return SwingAnalyzeResponse(
        swing_id=swing_record.id,
        status=swing_record.status,
        message="Swing analysis queued.",
    )
