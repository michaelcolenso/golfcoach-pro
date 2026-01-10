"""
API v1 routes for GolfCoach Pro.
"""

from fastapi import APIRouter
from app.api.v1 import health, auth, users


api_router = APIRouter()

# Register all v1 routes
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)

__all__ = ["api_router"]
