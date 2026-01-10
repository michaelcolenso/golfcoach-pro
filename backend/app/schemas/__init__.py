"""
Pydantic schemas for GolfCoach Pro API.
"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenRefresh,
    TokenResponse,
    AuthResponse,
    UserProfileBase,
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserStats,
    IssueFrequency,
    BiometricsAverage,
    LogoutRequest,
)
from app.schemas.swing import (
    SwingUploadRequest,
    SwingUploadResponse,
    SwingSummaryResponse,
    SwingDetailResponse,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenRefresh",
    "TokenResponse",
    "AuthResponse",
    "UserProfileBase",
    "UserProfileCreate",
    "UserProfileUpdate",
    "UserProfileResponse",
    "UserStats",
    "IssueFrequency",
    "BiometricsAverage",
    "LogoutRequest",
    "SwingUploadRequest",
    "SwingUploadResponse",
    "SwingSummaryResponse",
    "SwingDetailResponse",
]
