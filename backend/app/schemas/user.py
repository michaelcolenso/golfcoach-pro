"""
Pydantic schemas for User-related API requests and responses.

Follows the API specifications from API_SPEC.md.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator


# ============================================
# User Profile Schemas
# ============================================


class UserProfileBase(BaseModel):
    """Base user profile schema."""

    date_of_birth: Optional[datetime] = None
    height_cm: Optional[int] = Field(None, ge=50, le=300)
    weight_kg: Optional[int] = Field(None, ge=20, le=300)
    dominant_hand: Optional[str] = Field(None, pattern="^(left|right)$")
    primary_miss: Optional[str] = None
    goals: Optional[List[str]] = Field(default_factory=list)
    physical_limitations: Optional[List[str]] = Field(default_factory=list)


class UserProfileCreate(UserProfileBase):
    """Schema for creating user profile."""

    pass


class UserProfileUpdate(UserProfileBase):
    """Schema for updating user profile (all fields optional)."""

    pass


class UserProfileResponse(UserProfileBase):
    """Schema for user profile responses."""

    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================
# User Schemas
# ============================================


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    handicap: Optional[float] = Field(None, ge=0.0, le=54.0)


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    handicap: Optional[float] = Field(None, ge=0.0, le=54.0)
    profile: Optional[UserProfileUpdate] = None


class UserResponse(UserBase):
    """Schema for user responses."""

    id: int
    profile: Optional[UserProfileResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Authentication Schemas
# ============================================


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    """Schema for token refresh request."""

    refresh_token: str


class TokenResponse(BaseModel):
    """Schema for token refresh response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponse(BaseModel):
    """Schema for authentication response (login/register)."""

    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# ============================================
# User Statistics Schemas
# ============================================


class IssueFrequency(BaseModel):
    """Schema for common issue frequency."""

    issue: str
    count: int
    percentage: float


class BiometricsAverage(BaseModel):
    """Schema for average biomechanics data."""

    spine_angle: float
    hip_rotation: float
    shoulder_turn: float
    x_factor: float


class UserStats(BaseModel):
    """Schema for user statistics."""

    user_id: int
    period: str = Field(..., pattern="^(week|month|year|all)$")
    swings_analyzed: int
    average_score: float
    improvement_trend: str = Field(..., pattern="^(improving|stable|regressing)$")
    most_common_issues: List[IssueFrequency]
    biomechanics_avg: BiometricsAverage
    drills_completed: int
    practice_sessions: int


# ============================================
# Logout Schemas
# ============================================


class LogoutRequest(BaseModel):
    """Schema for logout request."""

    refresh_token: str
