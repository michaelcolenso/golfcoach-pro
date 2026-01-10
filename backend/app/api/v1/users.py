"""
User management endpoints for GolfCoach Pro API.

Handles user profile retrieval and updates.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserStats
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """
    Retrieve authenticated user's profile.

    Args:
        current_user: Current authenticated user

    Returns:
        User profile information
    """
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Update authenticated user's profile.

    Args:
        user_update: User update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user profile
    """
    updated_user = UserService.update_user(db, current_user, user_update)
    return updated_user


@router.get("/{user_id}/stats", response_model=UserStats)
async def get_user_statistics(
    user_id: int,
    period: str = "month",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> UserStats:
    """
    Retrieve user's golf statistics.

    Args:
        user_id: User ID
        period: Statistics period (week, month, year, all)
        current_user: Current authenticated user
        db: Database session

    Returns:
        User statistics

    Raises:
        HTTPException 403: User can only access their own stats
        HTTPException 404: User not found
    """
    # Verify user can only access their own stats
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own statistics",
        )

    # Verify period is valid
    if period not in ["week", "month", "year", "all"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid period. Must be one of: week, month, year, all",
        )

    # TODO: Implement actual statistics calculation
    # For now, return mock data
    return UserStats(
        user_id=user_id,
        period=period,
        swings_analyzed=0,
        average_score=0.0,
        improvement_trend="stable",
        most_common_issues=[],
        biomechanics_avg={
            "spine_angle": 0.0,
            "hip_rotation": 0.0,
            "shoulder_turn": 0.0,
            "x_factor": 0.0,
        },
        drills_completed=0,
        practice_sessions=0,
    )
