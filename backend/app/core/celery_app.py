"""
Celery application setup for GolfCoach Pro.
"""

from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "golfcoach",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_track_started=True,
    worker_concurrency=settings.CELERY_WORKER_CONCURRENCY,
)

__all__ = ["celery_app"]
