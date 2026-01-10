"""
Authentication endpoints for GolfCoach Pro API.

Handles user registration, login, token refresh, and logout.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token, generate_tokens
from app.core.dependencies import get_redis
from app.core.config import settings
from app.schemas.user import (
    UserCreate,
    UserLogin,
    AuthResponse,
    TokenRefresh,
    TokenResponse,
    LogoutRequest,
)
from app.services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)) -> AuthResponse:
    """
    Register a new user account.

    Args:
        user_data: User registration data (email, password, full_name)
        db: Database session

    Returns:
        User information and authentication tokens

    Raises:
        HTTPException 400: Invalid input
        HTTPException 409: Email already registered
    """
    result = UserService.register_user(db, user_data)

    return AuthResponse(
        user=result["user"],
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        token_type=result["token_type"],
        expires_in=result["expires_in"],
    )


@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)) -> AuthResponse:
    """
    Authenticate user and receive access token.

    Args:
        credentials: Login credentials (email, password)
        db: Database session

    Returns:
        User information and authentication tokens

    Raises:
        HTTPException 401: Invalid credentials
    """
    result = UserService.login_user(db, credentials.email, credentials.password)

    return AuthResponse(
        user=result["user"],
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        token_type=result["token_type"],
        expires_in=result["expires_in"],
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Get a new access token using refresh token.

    Args:
        token_data: Refresh token data
        db: Database session

    Returns:
        New access token

    Raises:
        HTTPException 401: Invalid or expired refresh token
    """
    try:
        # Verify refresh token
        payload = verify_token(token_data.refresh_token, token_type="refresh")
        user_id = int(payload.get("sub"))

        redis_client = get_redis()
        blacklist_key = f"blacklist:{token_data.refresh_token}"
        if redis_client.get(blacklist_key):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked",
            )

        # Verify user exists
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        # Generate new access token
        tokens = generate_tokens(user_id)

        return TokenResponse(
            access_token=tokens["access_token"],
            token_type=tokens["token_type"],
            expires_in=tokens["expires_in"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from e


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(logout_data: LogoutRequest) -> None:
    """
    Invalidate refresh token (logout user).

    In a production system, you would:
    1. Add refresh token to a blacklist in Redis
    2. Optionally revoke all sessions for the user

    For now, this is a placeholder that accepts the request.

    Args:
        logout_data: Logout request with refresh token

    Returns:
        No content (204)
    """
    redis_client = get_redis()
    ttl_seconds = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    redis_client.setex(
        f"blacklist:{logout_data.refresh_token}",
        ttl_seconds,
        "1",
    )
