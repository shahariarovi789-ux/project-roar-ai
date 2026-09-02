# api/routes/session.py
"""
Session State Endpoints: Start, Resume, Status, and Live Agent Activity Stream.
"""

from fastapi import APIRouter, Depends
from api.middleware import get_current_user_id
from agents.orchestrator import TutorOrchestrator
from backend.activity_tracker import activity_tracker

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/start")
async def start_session(user_id: str = Depends(get_current_user_id)):
    """Initializes or resumes the learner's tutoring state session."""
    return await TutorOrchestrator.get_or_create_session(user_id)


@router.get("/status")
async def get_session_status(user_id: str = Depends(get_current_user_id)):
    return await TutorOrchestrator.get_or_create_session(user_id)


@router.get("/activity")
async def get_live_agent_activity(user_id: str = Depends(get_current_user_id)):
    """Returns the live stream of recent agent actions, thoughts, and LLM telemetry."""
    return {"events": activity_tracker.get_recent(30)}
