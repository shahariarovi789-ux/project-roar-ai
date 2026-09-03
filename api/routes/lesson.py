# api/routes/lesson.py
"""
Lesson API Endpoints: Fetch current or specific node lesson, jump directly to quiz.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from api.middleware import get_current_user_id
from agents.orchestrator import TutorOrchestrator
from core.curriculum import curriculum_graph
from core.learner_profile import LearnerProfile
from core.state_machine import TutorPhase, TutorState
from db.storage import get_learner_profile, get_tutor_state, save_tutor_state

router = APIRouter(prefix="/lesson", tags=["Lesson"])


@router.get("/current")
async def get_current_lesson(
    node_id: Optional[str] = Query(None),
    regen: bool = Query(False),
    user_id: str = Depends(get_current_user_id)
):
    """Generates personalized study material for the active node or specified node."""
    return await TutorOrchestrator.fetch_current_lesson(user_id, node_id=node_id, force_regen=regen)


@router.get("/{node_id}")
async def get_specific_node_lesson(
    node_id: str,
    regen: bool = Query(False),
    user_id: str = Depends(get_current_user_id)
):
    """Fetches study materials for any unlocked or previously passed curriculum node."""
    node = curriculum_graph.get_node_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Curriculum node not found")
    return await TutorOrchestrator.fetch_current_lesson(user_id, node_id=node_id, force_regen=regen)


@router.post("/skip-to-quiz")
async def skip_to_quiz(user_id: str = Depends(get_current_user_id)):
    """Allows expert students to jump directly to the quiz section."""
    profile = await get_learner_profile(user_id) or LearnerProfile(user_id=user_id)
    state = await get_tutor_state(user_id) or TutorState(user_id=user_id)
    
    state.phase = TutorPhase.QUIZ
    await save_tutor_state(user_id, state, profile.completed_nodes)
    return await TutorOrchestrator.fetch_current_quiz(user_id)
