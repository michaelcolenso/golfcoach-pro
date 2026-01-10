"""
FastAPI dependencies for GolfCoach Pro.

Includes database session, authentication, and other common dependencies.
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import redis

from app.core.database import get_db
from app.core.security import get_user_id_from_token
from app.core.config import settings
from app.models.user import User


# HTTP Bearer security scheme
security = HTTPBearer()


# ============================================
# Redis Connection
# ============================================


def get_redis() -> redis.Redis:
    """
    Get Redis connection.

    Returns:
        Redis client instance
    """
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


# ============================================
# Authentication Dependencies
# ============================================


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Get current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Extract user ID from token
    user_id = get_user_id_from_token(token)

    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user (can be extended with active status check).

    Args:
        current_user: Current authenticated user

    Returns:
        Current active user

    Raises:
        HTTPException: If user is inactive
    """
    # Future: Add is_active field check
    # if not current_user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Inactive user"
    #     )
    return current_user


# ============================================
# Optional Authentication
# ============================================


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise None.

    Useful for endpoints that work both authenticated and unauthenticated.

    Args:
        credentials: Optional HTTP Bearer token credentials
        db: Database session

    Returns:
        Current user if authenticated, None otherwise
    """
    if credentials is None:
        return None

    try:
        token = credentials.credentials
        user_id = get_user_id_from_token(token)
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except HTTPException:
        return None
