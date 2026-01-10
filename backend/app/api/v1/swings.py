"""
Swing upload and retrieval endpoints.
"""

from __future__ import annotations

from itertools import count
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.services.storage_service import storage_service


router = APIRouter(prefix="/swings", tags=["Swings"])

_swing_id_counter = count(1)
_swing_store: dict[int, dict[str, str]] = {}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_swing_video(file: UploadFile = File(...)) -> dict:
    """
    Upload a swing video to object storage.

    Args:
        file: Uploaded video file

    Returns:
        Swing metadata including ID and object key
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    extension = Path(file.filename).suffix
    object_key = f"swings/{uuid4()}{extension}"

    try:
        storage_service.upload_file(file.file, object_key, file.content_type)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload swing video: {exc}",
        ) from exc

    swing_id = next(_swing_id_counter)
    _swing_store[swing_id] = {"object_key": object_key, "filename": file.filename}

    return {
        "swing_id": swing_id,
        "object_key": object_key,
        "filename": file.filename,
    }


@router.get("/{swing_id}/video")
async def get_swing_video(swing_id: int, expiry_seconds: int = 3600) -> dict:
    """
    Get a presigned URL for a swing video.

    Args:
        swing_id: ID of the swing
        expiry_seconds: Signed URL expiration in seconds

    Returns:
        Presigned URL for the swing video
    """
    swing = _swing_store.get(swing_id)
    if not swing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Swing not found",
        )

    try:
        video_url = storage_service.generate_signed_url(
            swing["object_key"], expiry_seconds
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate signed URL: {exc}",
        ) from exc

    return {
        "swing_id": swing_id,
        "video_url": video_url,
        "object_key": swing["object_key"],
    }
