# tests/test_scoring.py
"""
Automated Test Suite for Adaptive Scoring Engine & Multi-Criteria Equation.
"""

import pytest
from core.curriculum import curriculum_graph
from core.scoring import ScoringEngine, ScoreBreakdown


def test_float_extraction_with_think_tags():
    raw_with_think = "<think>The student did a good job on temperature.</think>0.85"
    val = ScoringEngine.extract_float_from_llm(raw_with_think)
    assert val == 0.85


def test_float_extraction_from_json():
    raw_json = '{"score": 0.92, "strengths": "Great prompt structure."}'
    val = ScoringEngine.extract_float_from_llm(raw_json)
    assert val == 0.92


def test_float_extraction_fallback():
    empty = ""
    assert ScoringEngine.extract_float_from_llm(empty, default=0.5) == 0.0

    nonsense = "I cannot evaluate this."
    assert ScoringEngine.extract_float_from_llm(nonsense, default=0.5) == 0.5


def test_composite_score_perfect():
    node = curriculum_graph.get_node_by_id("node_01")
    breakdown = ScoringEngine.compute_composite_score(
        semantic_score=1.0,
        rule_score=1.0,
        hints_used=0,
        elapsed_seconds=30.0,
        node=node,
        fail_streak=0
    )
    # Raw = 0.50 * 1.0 + 0.50 * 1.0 = 1.00. Final = 1.00
    assert breakdown.final_score == 1.00
    assert breakdown.passed is True
    assert breakdown.hint_penalty == 0.0
    assert breakdown.time_penalty == 0.0


def test_composite_score_with_penalties():
    node = curriculum_graph.get_node_by_id("node_01")  # time budget 240s
    breakdown = ScoringEngine.compute_composite_score(
        semantic_score=0.80,  # 0.50 * 0.8 = 0.40
        rule_score=0.70,      # 0.50 * 0.7 = 0.35 -> raw = 0.75
        hints_used=2,         # 2 * 0.05 = 0.10
        elapsed_seconds=260.0,# over 240s -> 0.05
        node=node,
        fail_streak=1         # 1 * 0.01 = 0.01
    )
    # Final = 0.75 - 0.10 - 0.05 - 0.01 = 0.59
    assert breakdown.final_score == 0.59
    assert breakdown.passed is True  # 0.59 >= 0.50 requirement
    assert breakdown.hint_penalty == 0.10
    assert breakdown.time_penalty == 0.05
    assert breakdown.retry_penalty == 0.01
