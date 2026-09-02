# api/routes/quiz.py
"""
Quiz API Endpoints: Fetch challenge, submit answer, request hint, advance node.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from db.models import QuizSubmitRequest, QuizHintRequest
from api.middleware import get_current_user_id
from agents.orchestrator import TutorOrchestrator

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.get("/current")
async def get_current_quiz(
    node_id: Optional[str] = Query(None),
    regen: bool = Query(False),
    user_id: str = Depends(get_current_user_id)
):
    """Fetches 3 dynamic, topic-specific challenge questions for the active node or specified node."""
    return await TutorOrchestrator.fetch_current_quiz(user_id, node_id=node_id, force_regen=regen)


@router.post("/submit")
async def submit_quiz_answer(
    req: QuizSubmitRequest,
    user_id: str = Depends(get_current_user_id)
):
    """Evaluates student's multi-question answer using the 5-variable adaptive scoring formula."""
    payload = req.answers if req.answers else req.answer
    return await TutorOrchestrator.evaluate_quiz_submission(user_id, payload)


@router.post("/hint")
async def request_quiz_hint(
    req: Optional[QuizHintRequest] = None,
    user_id: str = Depends(get_current_user_id)
):
    """Requests a hint (max 3) with progressive scaffolding."""
    q_idx = req.question_idx if req and req.question_idx else 1
    node_id = req.node_id if req else None
    return await TutorOrchestrator.request_hint(user_id, question_idx=q_idx, node_id=node_id)



@router.post("/advance")
async def advance_node(user_id: str = Depends(get_current_user_id)):
    """Advances to the next unlocked node in the curriculum after passing."""
    return await TutorOrchestrator.advance_node(user_id)
