"""
Pytest configuration and fixtures for GolfCoach Pro backend tests.

Provides database, client, and user fixtures for testing.
"""

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db
from app.core.config import settings
from app.models.user import Base, User, UserProfile
from app.core.security import hash_password


# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test.

    Yields:
        Database session
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database dependency override.

    Args:
        db: Test database session

    Yields:
        FastAPI test client
    """

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db: Session) -> User:
    """
    Create a test user in the database.

    Args:
        db: Test database session

    Returns:
        Test user
    """
    user = User(
        email="test@example.com",
        password_hash=hash_password("TestPassword123!"),
        full_name="Test User",
        handicap=15.0,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create profile
    profile = UserProfile(
        user_id=user.id,
        dominant_hand="right",
        goals=["Improve swing", "Lower handicap"],
    )
    db.add(profile)
    db.commit()

    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user: User) -> dict:
    """
    Get authentication headers for test user.

    Args:
        client: Test client
        test_user: Test user

    Returns:
        Headers with Bearer token
    """
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123!"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def test_user_data() -> dict:
    """
    Get test user registration data.

    Returns:
        User registration data
    """
    return {
        "email": "newuser@example.com",
        "password": "NewPassword123!",
        "full_name": "New Test User",
    }
