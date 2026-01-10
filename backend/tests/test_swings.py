"""
Tests for swing upload and analysis endpoints.
"""

import io
from typing import Generator
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.dependencies import get_celery_app, get_storage_service


class StorageServiceMock:
    """Mock storage service for swing uploads."""

    def __init__(self, signed_url: str) -> None:
        self.signed_url = signed_url
        self.uploaded_files: list[str] = []

    def upload_video(
        self,
        file_obj: io.BytesIO,
        filename: str,
        content_type: str,
        **_: object,
    ) -> str:
        """Record upload and return a mock object key."""
        self.uploaded_files.append(filename)
        return "videos/mock-swing.mp4"

    def get_signed_url(self, object_key: str, **_: object) -> str:
        """Return a signed URL for the object key."""
        return self.signed_url


class CeleryAppMock:
    """Mock Celery app for enqueueing analysis tasks."""

    def __init__(self) -> None:
        self.send_task = Mock()
        self.delay = Mock()


@pytest.fixture(scope="function")
def storage_service_mock() -> Generator[StorageServiceMock, None, None]:
    """Provide a storage service mock with dependency override."""
    signed_url = "https://cdn.example.com/videos/mock.mp4?signature=test"
    storage_service = StorageServiceMock(signed_url=signed_url)
    app.dependency_overrides[get_storage_service] = lambda: storage_service

    try:
        yield storage_service
    finally:
        app.dependency_overrides.pop(get_storage_service, None)


@pytest.fixture(scope="function")
def celery_app_mock() -> Generator[CeleryAppMock, None, None]:
    """Provide a Celery app mock with dependency override."""
    celery_app = CeleryAppMock()
    app.dependency_overrides[get_celery_app] = lambda: celery_app

    try:
        yield celery_app
    finally:
        app.dependency_overrides.pop(get_celery_app, None)


def _upload_swing(
    client: TestClient, auth_headers: dict, club: str = "driver"
) -> dict:
    video_stream = io.BytesIO(b"test swing video")
    response = client.post(
        "/api/v1/swings/upload",
        headers=auth_headers,
        data={
            "club": club,
            "intended_shape": "straight",
            "notes": "Working on backswing",
        },
        files={"video": ("swing.mp4", video_stream, "video/mp4")},
    )
    assert response.status_code == 202
    data = response.json()
    assert "swing_id" in data
    return data


def test_upload_swing_accepts_video_and_fields(
    client: TestClient, auth_headers: dict, storage_service_mock: StorageServiceMock
) -> None:
    """Test uploading a swing video returns accepted response."""
    data = _upload_swing(client, auth_headers)

    assert data["swing_id"]
    assert storage_service_mock.uploaded_files == ["swing.mp4"]


def test_get_swing_returns_signed_video_url(
    client: TestClient, auth_headers: dict, storage_service_mock: StorageServiceMock
) -> None:
    """Test retrieving swing details returns a signed video URL."""
    upload_data = _upload_swing(client, auth_headers)

    response = client.get(
        f"/api/v1/swings/{upload_data['swing_id']}", headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == upload_data["swing_id"]
    assert "video_url" in data
    assert "signature=" in data["video_url"]


def test_analyze_swing_enqueues_celery_task(
    client: TestClient,
    auth_headers: dict,
    storage_service_mock: StorageServiceMock,
    celery_app_mock: CeleryAppMock,
) -> None:
    """Test analyzing a swing enqueues a Celery task."""
    upload_data = _upload_swing(client, auth_headers)

    response = client.post(
        f"/api/v1/swings/{upload_data['swing_id']}/analyze",
        headers=auth_headers,
    )
    assert response.status_code == 202
    data = response.json()

    assert data["swing_id"] == upload_data["swing_id"]
    assert celery_app_mock.send_task.called or celery_app_mock.delay.called
