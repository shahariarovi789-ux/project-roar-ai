# tests/test_agents.py
"""
Automated Test Suite for Multi-Agent Logic: Lesson, Quiz, Evaluator, and Hardware Scout.
"""

import pytest
from core.curriculum import curriculum_graph
from core.learner_profile import LearnerProfile
from agents.hardware_scout import HardwareScout
from agents.lesson_agent import lesson_agent
from agents.quiz_agent import quiz_agent
from agents.evaluator_agent import evaluator_agent


def test_hardware_scout():
    profile = HardwareScout.scan_device()
    assert profile.os_name in ["Darwin", "Linux", "Windows"]
    assert profile.cpu_cores > 0
    assert profile.total_ram_gb > 0
    assert profile.recommended_model in ["qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b", "phi3:mini"]


@pytest.mark.asyncio
async def test_lesson_generation_mock():
    node = curriculum_graph.get_node_by_id("node_01")
    profile = LearnerProfile(user_id="test_user", prefers_examples=True)

    lesson_data = await lesson_agent.generate_lesson(node, profile)
    assert lesson_data["node_id"] == "node_01"
    assert len(lesson_data["lesson_markdown"]) > 20


@pytest.mark.asyncio
async def test_quiz_generation_and_evaluation_mock():
    node = curriculum_graph.get_node_by_id("node_01")
    profile = LearnerProfile(user_id="test_user")

    quiz_data = await quiz_agent.generate_quiz_challenge(node, profile)
    assert "questions" in quiz_data
    assert len(quiz_data["questions"]) == 3
    assert quiz_data["node_id"] == "node_01"

    eval_breakdown = await evaluator_agent.evaluate_submission(
        node=node,
        questions=quiz_data["questions"],
        student_answers={
            "q1": "B",
            "q2": "Act as a Senior Engineer. Generate clean Python functions.",
            "q3": "Naive prompts hallucinate when context is missing. Add explicit schema."
        },
        hints_used=0,
        elapsed_seconds=45.0
    )
    assert 0.0 <= eval_breakdown.final_score <= 1.0
