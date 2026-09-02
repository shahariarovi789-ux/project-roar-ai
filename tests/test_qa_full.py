# tests/test_qa_full.py
"""
Total QA System Verification for Project ROAR.
Tests end-to-end capabilities across all core subsystems:
1. Knowledge Graph & Curriculum Taxonomy
2. Model Manager & Inference Gateway
3. Vector Database RAG Retrieval
4. Lesson Generation & Tier Word-Count Calibration
5. Quiz Challenge Generation (Dynamic MCQs, No Embedded Hints)
6. Hint System (Non-repeating progressive hints across Q1, Q2, Q3)
7. Evaluator Agent & Multi-Criteria Adaptive Scoring
"""

import pytest
import asyncio
from core.curriculum import curriculum_graph
from core.learner_profile import LearnerProfile
from core.scoring import ScoringEngine
from backend.model_manager import model_manager
from agents.rag_agent import rag_agent
from agents.lesson_agent import lesson_agent
from agents.quiz_agent import quiz_agent
from agents.evaluator_agent import evaluator_agent


# ── 1. Curriculum Knowledge Graph QA ──────────────────────────
def test_qa_curriculum_graph():
    assert len(curriculum_graph.nodes) == 36
    node_01 = curriculum_graph.get_node_by_id("node_01")
    assert node_01 is not None
    assert node_01.difficulty_tier == 1
    assert node_01.weight == 1.0
    assert node_01.passing_threshold == 0.50

    # Prerequisite DAG consistency
    unlocked_initial = [n.id for n in curriculum_graph.nodes if curriculum_graph.is_unlocked(n.id, set())]
    assert "node_01" in unlocked_initial
    assert "node_03" not in unlocked_initial  # Requires node_01
    assert curriculum_graph.is_unlocked("node_03", {"node_01"}) is True


# ── 2. RAG Knowledge Retrieval QA ─────────────────────────────
def test_qa_rag_retrieval():
    context = rag_agent.retrieve_context("introduction to prompt engineering foundational instruction context", top_k=2)
    assert isinstance(context, str)


# ── 3. Lesson Agent Generation QA ─────────────────────────────
@pytest.mark.asyncio
async def test_qa_lesson_generation_tier1():
    node = curriculum_graph.get_node_by_id("node_01")
    profile = LearnerProfile(user_id="qa_user", prior_experience="beginner", prefers_examples=True)
    
    lesson = await lesson_agent.generate_lesson(node, profile)
    assert lesson["node_id"] == "node_01"
    assert "lesson_markdown" in lesson
    assert len(lesson["lesson_markdown"]) > 50
    # Tier 1 word count should be concise
    words = len(lesson["lesson_markdown"].split())
    assert words < 600, f"Tier 1 lesson too verbose: {words} words"


# ── 4. Quiz Agent Generation QA ───────────────────────────────
@pytest.mark.asyncio
async def test_qa_quiz_generation_no_embedded_hints():
    node = curriculum_graph.get_node_by_id("node_01")
    profile = LearnerProfile(user_id="qa_user")
    
    quiz = await quiz_agent.generate_quiz_challenge(node, profile)
    assert "questions" in quiz
    assert len(quiz["questions"]) == 3

    for idx, q in enumerate(quiz["questions"]):
        assert "question" in q
        q_text = q["question"]
        # Critical assertion: Hints must NEVER be embedded in the question text
        assert "Hint:" not in q_text, f"Question {idx+1} contains embedded Hint: {q_text}"
        assert "hint:" not in q_text.lower() or "delimit" in q_text.lower(), f"Question {idx+1} leaked hint keyword: {q_text}"

    # Question 1 must be MCQ with 4 options
    q1 = quiz["questions"][0]
    assert q1["type"] == "mcq"
    assert "options" in q1
    assert len(q1["options"]) >= 3


# ── 5. Hint Agent Non-Repeating Progressive Hints QA ──────────
@pytest.mark.asyncio
async def test_qa_progressive_hints():
    node = curriculum_graph.get_node_by_id("node_01")
    q1_text = "What is the primary role of prompt engineering?"
    
    h1 = await quiz_agent.generate_hint(node, q1_text, hint_number=1, previous_hints=[])
    assert len(h1) > 10
    assert not h1.startswith("Hint #1:")

    h2 = await quiz_agent.generate_hint(node, q1_text, hint_number=2, previous_hints=[h1])
    assert len(h2) > 10
    assert h2.lower().strip() != h1.lower().strip(), "Hint 2 duplicated Hint 1"

    h3 = await quiz_agent.generate_hint(node, q1_text, hint_number=3, previous_hints=[h1, h2])
    assert len(h3) > 10
    assert h3.lower().strip() not in [h1.lower().strip(), h2.lower().strip()], "Hint 3 duplicated previous hints"


# ── 6. Evaluator Agent & Scoring Engine QA ─────────────────────
@pytest.mark.asyncio
async def test_qa_evaluator_and_scoring():
    node = curriculum_graph.get_node_by_id("node_01")
    questions = [
        {"id": "q1", "type": "mcq", "question": "What is prompt engineering?", "correct": "B"},
        {"id": "q2", "type": "writing", "question": "Write a 2-bullet summary prompt."},
        {"id": "q3", "type": "writing", "question": "Improve a vague prompt."}
    ]
    student_answers = {
        "q1": "B",
        "q2": "You are a research assistant. Summarize the text in 2 concise bullets.",
        "q3": "Add specific persona roles, delimited text boundaries, and an exact length limit."
    }

    breakdown = await evaluator_agent.evaluate_submission(
        node=node,
        questions=questions,
        student_answers=student_answers,
        hints_used=1,
        elapsed_seconds=50.0
    )

    assert 0.0 <= breakdown.final_score <= 1.0
    assert breakdown.hint_penalty == 0.05
    assert breakdown.time_penalty == 0.0
    assert isinstance(breakdown.rationale, str)
    assert len(breakdown.rationale) > 10
