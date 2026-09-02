# agents/onboarding_agent.py
"""
Onboarding Agent.
Handles the 7-question conversational intake questionnaire, extracts learner
preferences, and initializes the LearnerProfile and TutorState.
"""

from typing import Dict, Any, List, Optional
from core.learner_profile import LearnerProfile
from db.storage import save_learner_profile


ONBOARDING_QUESTIONS = [
    {
        "step": 1,
        "key": "name",
        "question": "Welcome to the Prompt Engineering Tutor! What should I call you?",
        "type": "text",
        "placeholder": "Enter your name..."
    },
    {
        "step": 2,
        "key": "prior_experience",
        "question": "What is your prior experience level with prompt engineering and LLMs?",
        "type": "choice",
        "options": [
            {"value": "beginner", "label": "Beginner (New to prompt design)"},
            {"value": "intermediate", "label": "Intermediate (Regularly use ChatGPT/Claude)"},
            {"value": "expert", "label": "Expert (Build LLM apps / advanced prompting)"}
        ]
    },
    {
        "step": 3,
        "key": "prefers_examples",
        "question": "When learning a new prompting technique, what helps you more?",
        "type": "choice",
        "options": [
            {"value": True, "label": "Show me a concrete example first, then explain the theory"},
            {"value": False, "label": "Explain the core mental model first, then show examples"}
        ]
    },
    {
        "step": 4,
        "key": "prefers_detailed",
        "question": "How detailed do you like your lesson explanations?",
        "type": "choice",
        "options": [
            {"value": True, "label": "Detailed & thorough (in-depth nuances & edge cases)"},
            {"value": False, "label": "Concise & punchy (get straight to the actionable points)"}
        ]
    },
    {
        "step": 5,
        "key": "prefers_steps",
        "question": "How do you prefer instructions and breakdowns structured?",
        "type": "choice",
        "options": [
            {"value": True, "label": "Step-by-step numbered breakdown"},
            {"value": False, "label": "Fluid conceptual narrative"}
        ]
    },
    {
        "step": 6,
        "key": "preferred_quiz_style",
        "question": "What type of quiz challenges do you prefer?",
        "type": "choice",
        "options": [
            {"value": "writing", "label": "Hands-on prompt writing & coding"},
            {"value": "mcq", "label": "Conceptual multiple-choice"},
            {"value": "mixed", "label": "Mixed challenges based on topic difficulty"}
        ]
    },
    {
        "step": 7,
        "key": "session_time_budget",
        "question": "How much time do you typically have per learning session?",
        "type": "choice",
        "options": [
            {"value": 15, "label": "15 minutes (Quick micro-lessons)"},
            {"value": 30, "label": "30 minutes (Standard deep focus)"},
            {"value": 60, "label": "60 minutes (Intensive masterclass)"}
        ]
    }
]


class OnboardingAgent:
    @staticmethod
    def get_questions_spec() -> List[Dict[str, Any]]:
        return ONBOARDING_QUESTIONS

    @staticmethod
    async def process_answers(user_id: str, answers: Dict[str, Any]) -> LearnerProfile:
        profile = LearnerProfile(
            user_id=user_id,
            name=answers.get("name", "Student").strip() or "Student",
            prior_experience=answers.get("prior_experience", "beginner"),
            prefers_examples=bool(answers.get("prefers_examples", True)),
            prefers_steps=bool(answers.get("prefers_steps", True)),
            prefers_detailed=bool(answers.get("prefers_detailed", True)),
            preferred_quiz_style=answers.get("preferred_quiz_style", "mixed"),
            session_time_budget=int(answers.get("session_time_budget", 30)),
            onboarding_done=True,
            current_node_id="node_01"
        )
        await save_learner_profile(profile)
        return profile
