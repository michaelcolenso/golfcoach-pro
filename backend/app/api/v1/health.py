"""
Health check endpoints for GolfCoach Pro API.

Provides basic health check and database/redis connectivity checks.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis

from app.core.database import get_db
from app.core.dependencies import get_redis
from app.core.config import settings


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check() -> dict:
    """
    Basic health check endpoint.

    Returns:
        Status information
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }


@router.get("/db")
async def health_check_database(db: Session = Depends(get_db)) -> dict:
    """
    Database connectivity health check.

    Args:
        db: Database session

    Returns:
        Database status

    Raises:
        HTTPException: If database is not accessible
    """
    try:
        # Execute a simple query
        result = db.execute(text("SELECT 1"))
        result.fetchone()

        return {
            "status": "healthy",
            "database": "connected",
            "database_url": f"postgresql://{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}",
        ) from e


@router.get("/redis")
async def health_check_redis() -> dict:
    """
    Redis connectivity health check.

    Returns:
        Redis status

    Raises:
        HTTPException: If Redis is not accessible
    """
    try:
        redis_client = get_redis()
        # Ping Redis
        redis_client.ping()

        return {
            "status": "healthy",
            "redis": "connected",
            "redis_url": f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Redis connection failed: {str(e)}",
        ) from e


@router.get("/full")
async def health_check_full(db: Session = Depends(get_db)) -> dict:
    """
    Full health check including all dependencies.

    Args:
        db: Database session

    Returns:
        Complete status information
    """
    checks = {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "checks": {},
    }

    # Check database
    try:
        db.execute(text("SELECT 1"))
        checks["checks"]["database"] = "connected"
    except Exception as e:
        checks["status"] = "unhealthy"
        checks["checks"]["database"] = f"failed: {str(e)}"

    # Check Redis
    try:
        redis_client = get_redis()
        redis_client.ping()
        checks["checks"]["redis"] = "connected"
    except Exception as e:
        checks["status"] = "unhealthy"
        checks["checks"]["redis"] = f"failed: {str(e)}"

    return checks
