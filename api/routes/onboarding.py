# api/routes/onboarding.py
"""
Onboarding Questionnaire API Endpoints.
"""

from fastapi import APIRouter, Depends
from db.models import OnboardingAnswerRequest
from api.middleware import get_current_user_id
from agents.onboarding_agent import OnboardingAgent
from agents.orchestrator import TutorOrchestrator
from core.state_machine import StateTransitionController
from db.storage import get_tutor_state, save_tutor_state

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.get("/questions")
async def get_onboarding_questions():
    """Returns the 7-question onboarding intake spec."""
    return {"questions": OnboardingAgent.get_questions_spec()}


@router.post("/submit")
async def submit_onboarding_answers(
    req: OnboardingAnswerRequest,
    user_id: str = Depends(get_current_user_id)
):
    """Saves learner profile preferences and transitions tutor to LESSON phase."""
    profile = await OnboardingAgent.process_answers(user_id, req.model_dump())
    state = await get_tutor_state(user_id)
    if state:
        StateTransitionController.on_onboarding_completed(state, profile)
        await save_tutor_state(user_id, state, profile.completed_nodes)

    return await TutorOrchestrator.get_or_create_session(user_id)
