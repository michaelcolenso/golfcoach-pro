"""
Storage service for handling MinIO object storage operations.
"""

from __future__ import annotations

from datetime import timedelta
from typing import BinaryIO

from minio import Minio

from app.core.config import settings


class StorageService:
    """Service for interacting with MinIO storage."""

    def __init__(self) -> None:
        self._client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self._bucket_name = settings.MINIO_BUCKET_NAME
        self._bucket_checked = False
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        if self._bucket_checked:
            return

        if not self._client.bucket_exists(self._bucket_name):
            self._client.make_bucket(self._bucket_name)

        self._bucket_checked = True

    def upload_file(
        self, file_obj: BinaryIO, object_key: str, content_type: str | None
    ) -> None:
        """
        Upload a file to MinIO.

        Args:
            file_obj: File-like object to upload
            object_key: Object key in the bucket
            content_type: MIME type of the object
        """
        self._ensure_bucket_exists()

        file_obj.seek(0, 2)
        size = file_obj.tell()
        file_obj.seek(0)

        self._client.put_object(
            self._bucket_name,
            object_key,
            file_obj,
            size,
            content_type=content_type or "application/octet-stream",
        )

    def generate_signed_url(self, object_key: str, expiry_seconds: int) -> str:
        """
        Generate a presigned URL for an object.

        Args:
            object_key: Object key in the bucket
            expiry_seconds: URL expiration time in seconds

        Returns:
            Presigned URL string
        """
        self._ensure_bucket_exists()
        return self._client.presigned_get_object(
            self._bucket_name,
            object_key,
            expires=timedelta(seconds=expiry_seconds),
        )


storage_service = StorageService()
