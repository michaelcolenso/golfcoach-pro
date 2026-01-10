"""
SQLAlchemy models for GolfCoach Pro.
"""

from app.models.base import Base
from app.models.swing import Swing
from app.models.user import User, UserProfile

__all__ = ["Base", "User", "UserProfile", "Swing"]
