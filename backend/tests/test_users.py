"""
Tests for user management endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


def test_get_current_user(
    client: TestClient, test_user: User, auth_headers: dict
) -> None:
    """Test getting current user profile."""
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == test_user.id
    assert data["email"] == test_user.email
    assert data["full_name"] == test_user.full_name
    assert "profile" in data


def test_get_current_user_unauthorized(client: TestClient) -> None:
    """Test getting current user without authentication fails."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 403  # No Bearer token


def test_get_current_user_invalid_token(client: TestClient) -> None:
    """Test getting current user with invalid token fails."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401


def test_update_user_profile(
    client: TestClient, test_user: User, auth_headers: dict
) -> None:
    """Test updating user profile."""
    update_data = {
        "full_name": "Updated Name",
        "handicap": 12.5,
        "profile": {
            "primary_miss": "hook",
            "goals": ["Break 80", "Improve short game"],
        },
    }

    response = client.patch("/api/v1/users/me", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["full_name"] == "Updated Name"
    assert float(data["handicap"]) == 12.5
    assert data["profile"]["primary_miss"] == "hook"
    assert "Break 80" in data["profile"]["goals"]


def test_update_user_profile_partial(
    client: TestClient, test_user: User, auth_headers: dict
) -> None:
    """Test partial update of user profile."""
    update_data = {"handicap": 10.0}

    response = client.patch("/api/v1/users/me", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert float(data["handicap"]) == 10.0
    # Full name should remain unchanged
    assert data["full_name"] == test_user.full_name


def test_update_user_profile_unauthorized(client: TestClient) -> None:
    """Test updating user profile without authentication fails."""
    update_data = {"full_name": "Hacker"}

    response = client.patch("/api/v1/users/me", json=update_data)
    assert response.status_code == 403


def test_get_user_stats(
    client: TestClient, test_user: User, auth_headers: dict
) -> None:
    """Test getting user statistics."""
    response = client.get(
        f"/api/v1/users/{test_user.id}/stats?period=month", headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == test_user.id
    assert data["period"] == "month"
    assert "swings_analyzed" in data
    assert "average_score" in data
    assert "improvement_trend" in data
    assert "most_common_issues" in data
    assert "biomechanics_avg" in data


def test_get_user_stats_forbidden(
    client: TestClient, test_user: User, auth_headers: dict
) -> None:
    """Test getting other user's statistics fails."""
    other_user_id = test_user.id + 1
    response = client.get(
        f"/api/v1/users/{other_user_id}/stats", headers=auth_headers
    )
    assert response.status_code == 403


def test_get_user_stats_invalid_period(
    client: TestClient, test_user: User, auth_headers: dict
) -> None:
    """Test getting user statistics with invalid period fails."""
    response = client.get(
        f"/api/v1/users/{test_user.id}/stats?period=invalid", headers=auth_headers
    )
    assert response.status_code == 400
