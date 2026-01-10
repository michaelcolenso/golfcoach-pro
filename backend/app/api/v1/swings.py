"""Swing analysis endpoints."""

from fastapi import APIRouter

from app.tasks.analysis import analyze_swing

router = APIRouter(prefix="/swings", tags=["swings"])


@router.post("/{swing_id}/analyze")
async def analyze_swing_endpoint(swing_id: str) -> dict:
    """
    Queue a swing analysis task.

    Args:
        swing_id: Identifier for the swing to analyze.

    Returns:
        Task metadata for the queued analysis.
    """
    task = analyze_swing.delay(swing_id)
    return {
        "swing_id": swing_id,
        "task_id": task.id,
        "status": "queued",
    }
