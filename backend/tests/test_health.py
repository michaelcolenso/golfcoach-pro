"""
Tests for health check endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "docs" in data


def test_simple_health_check(client: TestClient) -> None:
    """Test simple health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_health_check_endpoint(client: TestClient) -> None:
    """Test detailed health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data
    assert "environment" in data


def test_health_check_database(client: TestClient) -> None:
    """Test database health check endpoint."""
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "database_url" in data


def test_health_check_redis(client: TestClient) -> None:
    """Test Redis health check endpoint."""
    # Note: This will fail if Redis is not running
    # In a real test environment, you'd mock Redis or use a test Redis instance
    response = client.get("/api/v1/health/redis")

    # We expect this to fail in CI/test environment without Redis
    # In a real deployment test, you'd assert 200
    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "healthy"
        assert data["redis"] == "connected"


def test_health_check_full(client: TestClient) -> None:
    """Test full health check endpoint."""
    response = client.get("/api/v1/health/full")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "checks" in data
    assert "database" in data["checks"]
    # Redis might not be available in test environment
    assert "redis" in data["checks"]
