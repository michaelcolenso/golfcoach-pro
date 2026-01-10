"""
Main FastAPI application for GolfCoach Pro backend.

Initializes the FastAPI app, middleware, and routes.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.core.config import settings
from app.core.database import engine
from app.models.user import Base
from app.api.v1 import api_router


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Create database tables
# Note: In production, use Alembic migrations instead
if settings.APP_ENV == "development":
    Base.metadata.create_all(bind=engine)


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered golf swing analysis and coaching API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ============================================
# CORS Middleware
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS.split(","),
    allow_headers=settings.CORS_ALLOW_HEADERS.split(","),
)


# ============================================
# Exception Handlers
# ============================================


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle validation errors from Pydantic.

    Args:
        request: FastAPI request
        exc: Validation exception

    Returns:
        JSON response with error details
    """
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "validation_error",
            "message": "Invalid request data",
            "details": exc.errors(),
        },
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """
    Handle database errors.

    Args:
        request: FastAPI request
        exc: SQLAlchemy exception

    Returns:
        JSON response with error message
    """
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "A database error occurred",
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all other exceptions.

    Args:
        request: FastAPI request
        exc: Exception

    Returns:
        JSON response with error message
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
        },
    )


# ============================================
# Routes
# ============================================

# Root endpoint
@app.get("/")
async def root() -> dict:
    """
    Root endpoint with API information.

    Returns:
        API information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


# Include API v1 routes
app.include_router(api_router, prefix="/api/v1")


# ============================================
# Startup and Shutdown Events
# ============================================


@app.on_event("startup")
async def startup_event() -> None:
    """
    Run on application startup.

    Initializes connections and services.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"API documentation: {settings.API_BASE_URL}/docs")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Run on application shutdown.

    Cleans up connections and resources.
    """
    logger.info(f"Shutting down {settings.APP_NAME}")


# ============================================
# Health Check
# ============================================

# Note: Detailed health checks are in /api/v1/health
@app.get("/health")
async def simple_health_check() -> dict:
    """
    Simple health check endpoint.

    Returns:
        Status information
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
