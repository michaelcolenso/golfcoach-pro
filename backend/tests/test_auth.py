"""
Tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


def test_register_user(client: TestClient, test_user_data: dict) -> None:
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    data = response.json()

    # Check user data
    assert "user" in data
    assert data["user"]["email"] == test_user_data["email"]
    assert data["user"]["full_name"] == test_user_data["full_name"]
    assert "id" in data["user"]

    # Check tokens
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


def test_register_duplicate_email(
    client: TestClient, test_user: User, test_user_data: dict
) -> None:
    """Test registration with duplicate email fails."""
    # Try to register with existing email
    test_user_data["email"] = test_user.email

    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 409
    data = response.json()
    assert "already registered" in data["detail"].lower()


def test_register_invalid_password(client: TestClient) -> None:
    """Test registration with weak password fails."""
    data = {
        "email": "test@example.com",
        "password": "weak",  # Too short, no uppercase, no number
        "full_name": "Test User",
    }

    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 400


def test_register_invalid_email(client: TestClient) -> None:
    """Test registration with invalid email fails."""
    data = {
        "email": "not-an-email",
        "password": "StrongPass123!",
        "full_name": "Test User",
    }

    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 400


def test_login_success(client: TestClient, test_user: User) -> None:
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123!"},
    )
    assert response.status_code == 200
    data = response.json()

    # Check user data
    assert "user" in data
    assert data["user"]["email"] == test_user.email
    assert data["user"]["id"] == test_user.id

    # Check tokens
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user: User) -> None:
    """Test login with wrong password fails."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "WrongPassword123!"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient) -> None:
    """Test login with non-existent user fails."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "SomePassword123!"},
    )
    assert response.status_code == 401


def test_refresh_token(client: TestClient, test_user: User) -> None:
    """Test token refresh."""
    # First, login to get tokens
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123!"},
    )
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]

    # Now refresh the token
    response = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


def test_refresh_token_invalid(client: TestClient) -> None:
    """Test token refresh with invalid token fails."""
    response = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401


def test_logout(client: TestClient, test_user: User) -> None:
    """Test logout."""
    # First, login to get tokens
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123!"},
    )
    refresh_token = login_response.json()["refresh_token"]

    # Now logout
    response = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert response.status_code == 204
