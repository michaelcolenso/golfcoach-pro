"""
Configuration module for GolfCoach Pro backend.

Uses Pydantic Settings for type-safe configuration from environment variables.
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_ENV: str = Field(default="development")
    APP_NAME: str = Field(default="GolfCoach Pro")
    APP_VERSION: str = Field(default="0.1.0")
    DEBUG: bool = Field(default=True)

    # API Configuration
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    API_BASE_URL: str = Field(default="http://localhost:8000")

    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for JWT signing",
    )

    # JWT Settings
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # Database (PostgreSQL + TimescaleDB)
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default="golfcoach")
    POSTGRES_USER: str = Field(default="golfcoach_user")
    POSTGRES_PASSWORD: str = Field(default="change-this-password")

    # Connection pool settings
    DB_POOL_SIZE: int = Field(default=20)
    DB_MAX_OVERFLOW: int = Field(default=40)

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Construct async database URL for async SQLAlchemy."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: str = Field(default="")
    REDIS_DB: int = Field(default=0)

    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL from components."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Cache TTL (seconds)
    CACHE_TTL_SHORT: int = Field(default=300)  # 5 minutes
    CACHE_TTL_MEDIUM: int = Field(default=3600)  # 1 hour
    CACHE_TTL_LONG: int = Field(default=86400)  # 24 hours

    # MinIO (Object Storage)
    MINIO_ENDPOINT: str = Field(default="localhost:9000")
    MINIO_ACCESS_KEY: str = Field(default="minioadmin")
    MINIO_SECRET_KEY: str = Field(default="minioadmin")
    MINIO_BUCKET_NAME: str = Field(default="golfcoach-videos")
    MINIO_SECURE: bool = Field(default=False)

    # Celery (Task Queue)
    @property
    def CELERY_BROKER_URL(self) -> str:
        """Construct Celery broker URL."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        """Construct Celery result backend URL."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/2"

    CELERY_WORKER_CONCURRENCY: int = Field(default=4)

    # AI Services - Anthropic (Claude)
    ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key")
    CLAUDE_MODEL: str = Field(default="claude-opus-4-5-20251101")
    CLAUDE_MAX_TOKENS: int = Field(default=4096)
    CLAUDE_TEMPERATURE: float = Field(default=0.3)

    # AI Cost limits
    AI_DAILY_BUDGET: float = Field(default=100.00)

    # MediaPipe Configuration
    MEDIAPIPE_MODEL_COMPLEXITY: int = Field(
        default=2, description="0=lite, 1=full, 2=heavy"
    )
    MEDIAPIPE_MIN_DETECTION_CONFIDENCE: float = Field(default=0.5)
    MEDIAPIPE_MIN_TRACKING_CONFIDENCE: float = Field(default=0.5)

    # Video Processing
    VIDEO_MAX_SIZE_MB: int = Field(default=100)
    VIDEO_MAX_DURATION_SECONDS: int = Field(default=30)
    VIDEO_ALLOWED_FORMATS: str = Field(default="mp4,mov,avi")
    VIDEO_PROCESSING_FPS: int = Field(default=60)
    FFMPEG_PATH: str = Field(default="/usr/bin/ffmpeg")

    @property
    def VIDEO_ALLOWED_FORMATS_LIST(self) -> List[str]:
        """Get list of allowed video formats."""
        return [fmt.strip() for fmt in self.VIDEO_ALLOWED_FORMATS.split(",")]

    # File Storage
    UPLOAD_DIR: str = Field(default="/tmp/golfcoach/uploads")
    TEMP_DIR: str = Field(default="/tmp/golfcoach/temp")
    MAX_UPLOAD_SIZE_MB: int = Field(default=100)

    # File retention (days)
    VIDEO_RETENTION_DAYS: int = Field(default=365)
    TEMP_FILE_RETENTION_HOURS: int = Field(default=24)

    # CORS
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:19006,exp://localhost:19000"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: str = Field(default="GET,POST,PUT,DELETE,PATCH,OPTIONS")
    CORS_ALLOW_HEADERS: str = Field(default="*")

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        """Get list of allowed CORS origins."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_DEFAULT: int = Field(default=100)  # requests per minute
    RATE_LIMIT_FREE: int = Field(default=60)
    RATE_LIMIT_PRO: int = Field(default=120)
    RATE_LIMIT_ELITE: int = Field(default=300)

    # Email (Optional - for notifications)
    SMTP_HOST: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    SMTP_FROM: str = Field(default="noreply@golfcoachpro.com")

    # Monitoring & Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")

    # Sentry (Error tracking)
    SENTRY_DSN: str = Field(default="")
    SENTRY_ENVIRONMENT: str = Field(default="development")

    # Prometheus metrics
    METRICS_ENABLED: bool = Field(default=True)
    METRICS_PORT: int = Field(default=9090)

    # Payment (Stripe)
    STRIPE_PUBLIC_KEY: str = Field(default="")
    STRIPE_SECRET_KEY: str = Field(default="")
    STRIPE_WEBHOOK_SECRET: str = Field(default="")
    STRIPE_PRICE_PRO_MONTHLY: str = Field(default="")
    STRIPE_PRICE_PRO_YEARLY: str = Field(default="")
    STRIPE_PRICE_ELITE_MONTHLY: str = Field(default="")

    # Feature Flags
    FEATURE_REAL_TIME_MODE: bool = Field(default=True)
    FEATURE_3D_VISUALIZATION: bool = Field(default=False)
    FEATURE_MULTI_ANGLE: bool = Field(default=False)
    FEATURE_COACH_PORTAL: bool = Field(default=False)
    FEATURE_INTEGRATIONS: bool = Field(default=False)

    # Development
    RELOAD: bool = Field(default=True)
    SQL_ECHO: bool = Field(default=False)
    SEED_DATABASE: bool = Field(default=True)
    MOCK_AI_IN_TESTS: bool = Field(default=True)

    # Security
    HTTPS_ONLY: bool = Field(default=False)
    ALLOWED_HOSTS: str = Field(default="localhost,127.0.0.1")
    SESSION_COOKIE_SECURE: bool = Field(default=False)
    SESSION_COOKIE_HTTPONLY: bool = Field(default=True)
    SESSION_COOKIE_SAMESITE: str = Field(default="lax")

    # Testing
    TEST_DATABASE_URL: str = Field(
        default="postgresql://test_user:test_pass@localhost:5432/test_golfcoach"
    )

    # Backup
    BACKUP_ENABLED: bool = Field(default=False)
    BACKUP_S3_BUCKET: str = Field(default="")
    BACKUP_AWS_ACCESS_KEY: str = Field(default="")
    BACKUP_AWS_SECRET_KEY: str = Field(default="")
    BACKUP_RETENTION_DAYS: int = Field(default=30)

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v_upper

    @field_validator("JWT_ALGORITHM")
    @classmethod
    def validate_jwt_algorithm(cls, v: str) -> str:
        """Validate JWT algorithm."""
        allowed = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
        if v not in allowed:
            raise ValueError(f"JWT_ALGORITHM must be one of {allowed}")
        return v


# Global settings instance
settings = Settings()
