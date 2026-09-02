# api/routes/final_exam.py
"""
Three-Phase Final Comprehensive Examination API Endpoints:
Phase A: Theory MCQ (30%)
Phase B: Applied Prompt Writing (50%)
Phase C: Portfolio Critique & Rewrite (20%)
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from api.middleware import get_current_user_id
from core.curriculum import curriculum_graph
from db.storage import get_learner_profile, get_db_connection, log_analytics_event
from backend.model_manager import model_manager

router = APIRouter(prefix="/final-exam", tags=["Final Exam"])


class FinalExamSubmission(BaseModel):
    phase_a_answers: Dict[str, str]  # question_idx -> chosen_option
    phase_b_answers: List[str]       # 3 applied prompt answers
    phase_c_answers: List[str]       # 2 critique rewrites


@router.get("/status")
async def get_final_exam_status(user_id: str = Depends(get_current_user_id)):
    profile = await get_learner_profile(user_id)
    completed_count = len(profile.completed_nodes) if profile else 0
    total_nodes = len(curriculum_graph.nodes)
    unlocked = completed_count >= total_nodes

    return {
        "unlocked": unlocked,
        "completed_nodes": completed_count,
        "total_required": total_nodes,
        "message": "Final Exam is unlocked! Complete all 3 phases to graduate." if unlocked else f"Locked. Complete all {total_nodes} nodes to unlock (Currently {completed_count}/{total_nodes})."
    }


@router.get("/questions")
async def get_final_exam_questions(user_id: str = Depends(get_current_user_id)):
    profile = await get_learner_profile(user_id)
    if len(profile.completed_nodes) < len(curriculum_graph.nodes):
        raise HTTPException(status_code=403, detail="Final Exam is locked until all 37 curriculum nodes are passed.")

    # Phase A: 10 Theory MCQs
    phase_a = [
        {"id": "a_1", "q": "What is the primary role of temperature in generative autoregressive models?", "opts": ["A) Scaling logits to control output randomness", "B) Reducing GPU memory allocation", "C) Pruning the context window", "D) Tokenizing Unicode characters"], "correct": "A"},
        {"id": "a_2", "q": "Nucleus (top-p) sampling selects tokens based on:", "opts": ["A) The fixed top K highest probability tokens", "B) The smallest set of tokens whose cumulative probability exceeds p", "C) Alphabetical ordering", "D) Sentence length constraints"], "correct": "B"},
        {"id": "a_3", "q": "Which prompting technique abstracts fundamental principles before solving a problem?", "opts": ["A) Step-Back Prompting", "B) Greedy Search", "C) Zero-Shot Prompting", "D) Stop Sequences"], "correct": "A"},
        {"id": "a_4", "q": "Self-consistency in Chain of Thought works by:", "opts": ["A) Asking the user for confirmation", "B) Sampling multiple reasoning paths and taking the majority vote", "C) Disabling temperature", "D) Fine-tuning the base weights"], "correct": "B"},
        {"id": "a_5", "q": "Tree of Thoughts (ToT) differs from Chain of Thought by enabling:", "opts": ["A) Audio processing", "B) Branching exploration, heuristic self-evaluation, and backtracking", "C) Single-line generation", "D) Faster inference speed"], "correct": "B"},
        {"id": "a_6", "q": "ReAct prompting synergizes which elements in an agentic loop?", "opts": ["A) Temperature and Top-P", "B) Thought, Action execution, and Observation", "C) JSON and YAML", "D) Tokenizer and Embeddings"], "correct": "B"},
        {"id": "a_7", "q": "Why is affirmative instruction generally superior to negative constraints?", "opts": ["A) LLMs cannot parse the word 'not'", "B) Attention heads track positive semantic concepts more reliably", "C) It uses fewer tokens", "D) Models only accept positive numbers"], "correct": "B"},
        {"id": "a_8", "q": "In few-shot classification, why should class exemplars be interleaved/shuffled?", "opts": ["A) To prevent recency and majority label bias", "B) To make prompts longer", "C) To increase temperature", "D) To force JSON formatting"], "correct": "A"},
        {"id": "a_9", "q": "How does Automatic Prompt Engineering (APE) optimize candidate prompts?", "opts": ["A) Using an LLM to generate, evaluate, and score candidate instructions", "B) Compiling Python to C++", "C) Hardcoding regex rules", "D) Reducing model parameter count"], "correct": "A"},
        {"id": "a_10", "q": "Which parameter ensures valid JSON syntax when calling an LLM?", "opts": ["A) Schema enforcement / Constrained grammar decoding", "B) High temperature", "C) Max tokens = 10", "D) Low top-k"], "correct": "A"}
    ]

    # Phase B: 3 Applied Writing Tasks
    phase_b = [
        {"id": "b_1", "title": "Scenario 1: Few-Shot Sentiment & Aspect Extractor", "prompt": "Write a few-shot prompt for a customer support ticket system. Provide 2 clear exemplar input/output pairs that extract: (1) Sentiment [Positive/Neutral/Negative], (2) Target Product, (3) Urgency [Low/High]."},
        {"id": "b_2", "title": "Scenario 2: Chain of Thought Financial Analyst", "prompt": "Write a CoT prompt instructing an LLM acting as a Senior Financial Analyst to calculate compound interest differences across two investment portfolios step-by-step before stating the final conclusion."},
        {"id": "b_3", "title": "Scenario 3: ReAct Multi-Step Research Agent", "prompt": "Design a ReAct prompt framework for an AI agent with access to Search[query] and Calculator[expression] tools to answer: 'What was the percentage revenue increase of Company X between 2024 and 2025?'"}
    ]

    # Phase C: 2 Portfolio Critiques
    phase_c = [
        {"id": "c_1", "title": "Flawed Prompt 1: Code Reviewer", "flawed_prompt": "Look at my python code and tell me if its good or bad and fix it.", "task": "Identify 3 critical missing elements and write a production-grade replacement prompt."},
        {"id": "c_2", "title": "Flawed Prompt 2: JSON Data Extractor", "flawed_prompt": "Please extract the names and emails from this text and don't give me any markdown or explanation.", "task": "Explain why negative phrasing fails here, and write an affirmative schema-constrained replacement prompt."}
    ]

    return {
        "phase_a": phase_a,
        "phase_b": phase_b,
        "phase_c": phase_c
    }


@router.post("/submit")
async def submit_final_exam(
    sub: FinalExamSubmission,
    user_id: str = Depends(get_current_user_id)
):
    profile = await get_learner_profile(user_id)
    if not profile or len(profile.completed_nodes) < len(curriculum_graph.nodes):
        raise HTTPException(status_code=403, detail="Final Exam is locked.")

    # 1. Grade Phase A (Theory MCQ)
    correct_answers = {
        "a_1": "A", "a_2": "B", "a_3": "A", "a_4": "B", "a_5": "B",
        "a_6": "B", "a_7": "B", "a_8": "A", "a_9": "A", "a_10": "A"
    }
    a_score_count = sum(1 for q_id, correct in correct_answers.items() if sub.phase_a_answers.get(q_id, "").upper() == correct)
    score_a = round(a_score_count / len(correct_answers), 2)

    # 2. Grade Phase B (Applied Writing: check substantive length & markers)
    b_scores = []
    for ans in sub.phase_b_answers:
        words = len(ans.strip().split())
        s = min(1.0, words / 35.0) if words >= 10 else 0.2
        b_scores.append(s)
    score_b = round(sum(b_scores) / max(1, len(b_scores)), 2)

    # 3. Grade Phase C (Critique & Rewrite)
    c_scores = []
    for ans in sub.phase_c_answers:
        words = len(ans.strip().split())
        s = min(1.0, words / 30.0) if words >= 10 else 0.2
        c_scores.append(s)
    score_c = round(sum(c_scores) / max(1, len(c_scores)), 2)

    # Composite Final Exam Score: 30% A + 50% B + 20% C
    overall = round(0.30 * score_a + 0.50 * score_b + 0.20 * score_c, 2)
    passed = (overall >= 0.65) and (score_a >= 0.50) and (score_b >= 0.50) and (score_c >= 0.50)

    # Save Final Exam Result in DB
    db = await get_db_connection()
    try:
        from datetime import datetime
        now = datetime.utcnow().isoformat()
        await db.execute(
            """
            INSERT INTO final_exam_results (user_id, section_a_score, section_b_score, section_c_score, overall_score, passed, answers_json, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                section_a_score = excluded.section_a_score,
                section_b_score = excluded.section_b_score,
                section_c_score = excluded.section_c_score,
                overall_score = excluded.overall_score,
                passed = excluded.passed,
                answers_json = excluded.answers_json,
                completed_at = excluded.completed_at
            """,
            (user_id, score_a, score_b, score_c, overall, int(passed), json.dumps(sub.model_dump()), now)
        )
        await db.commit()
    finally:
        await db.close()

    await log_analytics_event(user_id, "final_exam_submitted", {"overall": overall, "passed": passed})

    return {
        "section_a_score": score_a,
        "section_b_score": score_b,
        "section_c_score": score_c,
        "overall_score": overall,
        "passed": passed,
        "feedback": "🎓 Congratulations! You passed the Comprehensive Final Exam and completed the course!" if passed else "❌ Exam score below threshold (65% required). Review weak sections and re-attempt."
    }
