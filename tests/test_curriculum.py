# tests/test_curriculum.py
"""
Automated Test Suite for Curriculum Knowledge Graph & Prerequisite Engine.
"""

import pytest
from core.curriculum import curriculum_graph, CurriculumNode


def test_curriculum_total_nodes():
    assert len(curriculum_graph.nodes) == 36, "Expected exactly 36 curriculum nodes"


def test_curriculum_tiers_distribution():
    tier_1 = curriculum_graph.get_nodes_by_tier(1)
    tier_2 = curriculum_graph.get_nodes_by_tier(2)
    tier_3 = curriculum_graph.get_nodes_by_tier(3)

    assert len(tier_1) == 10, f"Expected 10 Tier 1 nodes, got {len(tier_1)}"
    assert len(tier_2) == 18, f"Expected 18 Tier 2 nodes, got {len(tier_2)}"
    assert len(tier_3) == 8, f"Expected 8 Tier 3 nodes, got {len(tier_3)}"


def test_prerequisite_unlock_logic():
    # node_01 (Introduction to prompt engineering) has no prerequisites -> unlocked initially
    assert curriculum_graph.is_unlocked("node_01", set()) is True

    # node_03 (Output length) requires node_01
    assert curriculum_graph.is_unlocked("node_03", set()) is False
    assert curriculum_graph.is_unlocked("node_03", {"node_01"}) is True

    # node_14 (Self-consistency) requires node_13 (CoT)
    assert curriculum_graph.is_unlocked("node_14", set()) is False
    assert curriculum_graph.is_unlocked("node_14", {"node_13"}) is True


def test_topological_sequence():
    ordered = curriculum_graph.get_ordered_sequence()
    assert len(ordered) == 36
    # Ensure node_01 appears before node_03
    idx_01 = next(i for i, n in enumerate(ordered) if n.id == "node_01")
    idx_03 = next(i for i, n in enumerate(ordered) if n.id == "node_03")
    assert idx_01 < idx_03


def test_time_budgets():
    node_01 = curriculum_graph.get_node_by_id("node_01")
    assert node_01.title == "Introduction to prompt engineering"
    assert node_01.time_budget_seconds == 240.0  # 180 + 60 * 1.0

    node_react = curriculum_graph.get_node_by_id("node_16")
    assert node_react.time_budget_seconds == 420.0  # 180 + 60 * 4.0

