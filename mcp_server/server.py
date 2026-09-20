# mcp_server/server.py
"""
ROAR Model Context Protocol (MCP) Server.
Exposes Project ROAR's pedagogical knowledge graph, ChromaDB vector stores,
learner profile states, and assessment tools via the official MCP specification.
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from mcp.server.mcpserver import MCPServer

from core.curriculum import curriculum_graph
from core.learner_profile import LearnerProfile
from core.state_machine import TutorState, TutorPhase, StateTransitionController
from agents.rag_agent import rag_agent
from agents.quiz_agent import quiz_agent
from agents.evaluator_agent import evaluator_agent
from agents.hardware_scout import HardwareScout
from db.storage import (
    get_learner_profile,
    save_learner_profile,
    get_tutor_state,
    save_tutor_state,
    record_quiz_attempt,
)


def create_roar_mcp_server() -> MCPServer:
    """Creates and configures the ROAR MCP Server with all resources, tools, and prompts."""
    server = MCPServer(
        name="ROAR-Tutor-MCP",
        version="2.0.0",
        instructions=(
            "ROAR Model Context Protocol Server provides standardized access to prompt engineering "
            "curriculum DAG resources, ChromaDB vector grounding, learner profile state, and "
            "adaptive educational tools (lesson generation, assessment, dual-stage grading, scaffolding)."
        )
    )

    # =========================================================================
    # MCP RESOURCES: Standardized URI Context Providers
    # =========================================================================

    @server.resource("roar://curriculum/dag")
    def get_curriculum_dag() -> str:
        """Returns the full 36-node topological curriculum DAG, node weights, and Bloom taxonomy tiers."""
        nodes_data = [
            {
                "id": n.id,
                "title": n.title,
                "category": n.category,
                "difficulty_tier": n.difficulty_tier,
                "weight": n.weight,
                "prerequisites": n.prerequisites,
                "quiz_type": n.quiz_type,
                "passing_score": n.rubric.get("passing_score", 0.5) if n.rubric else 0.5
            }
            for n in curriculum_graph.nodes
        ]
        return json.dumps({
            "total_nodes": len(nodes_data),
            "summary_stats": curriculum_graph.summary_stats(),
            "nodes": nodes_data
        }, indent=2)

    @server.resource("roar://curriculum/node/{node_id}")
    def get_curriculum_node(node_id: str) -> str:
        """Returns detailed pedagogical specifications, rubrics, and prerequisites for a specific node."""
        node = curriculum_graph.get_node_by_id(node_id)
        if not node:
            return json.dumps({"error": f"Node '{node_id}' not found in curriculum DAG."})
        return json.dumps({
            "id": node.id,
            "title": node.title,
            "category": node.category,
            "difficulty_tier": node.difficulty_tier,
            "weight": node.weight,
            "description": node.description,
            "prerequisites": node.prerequisites,
            "quiz_type": node.quiz_type,
            "rubric": node.rubric
        }, indent=2)

    @server.resource("roar://learner/{user_id}/profile")
    async def get_learner_profile_resource(user_id: str) -> str:
        """Returns the live learner profile, preferences, mastery map, and fail streaks for a user."""
        profile = await get_learner_profile(user_id)
        if not profile:
            profile = LearnerProfile(user_id=user_id)
        return json.dumps(profile.to_dict(), indent=2)

    @server.resource("roar://learner/{user_id}/session")
    async def get_learner_session_resource(user_id: str) -> str:
        """Returns active session state, current node, phase, and hints quota for a user."""
        state = await get_tutor_state(user_id)
        if not state:
            state = TutorState(user_id=user_id)
        return json.dumps(state.to_dict(), indent=2)

    @server.resource("roar://hardware/profile")
    def get_hardware_profile_resource() -> str:
        """Returns host hardware profile, GPU/VRAM telemetry, and recommended local LLM model tier."""
        profile = HardwareScout.scan_device()
        return json.dumps(profile.to_dict(), indent=2)

    # =========================================================================
    # MCP TOOLS: Standardized Educational & Assessment Capabilities
    # =========================================================================

    @server.tool()
    def retrieve_grounding_context(topic: str, n_results: int = 3) -> Dict[str, Any]:
        """Retrieves semantic grounding documentation from ChromaDB vector store for a prompt engineering topic.

        Args:
            topic: The technical topic or query to search (e.g. 'chain-of-thought', 'delimiters').
            n_results: Number of relevant knowledge chunks to retrieve (default: 3).
        """
        context_str = rag_agent.retrieve_context(topic, top_k=n_results)
        chunks = [c for c in context_str.split("\n\n") if c.strip()]
        return {
            "topic": topic,
            "chunks_retrieved": len(chunks),
            "grounding_text": context_str or "No specific grounding documents found."
        }

    @server.tool()
    async def verify_node_unlocked(user_id: str, node_id: str) -> Dict[str, Any]:
        """Verifies whether a student meets all prerequisite requirements in the DAG to study a node.

        Args:
            user_id: Unique student identifier.
            node_id: Target curriculum node ID to check (e.g. 'node_05').
        """
        node = curriculum_graph.get_node_by_id(node_id)
        if not node:
            return {"unlocked": False, "error": f"Node '{node_id}' not found."}

        profile = await get_learner_profile(user_id)
        completed = set(profile.completed_nodes) if profile else set()
        is_unlocked = curriculum_graph.is_unlocked(node_id, completed)
        missing_prereqs = [p for p in node.prerequisites if p not in completed]

        return {
            "node_id": node_id,
            "title": node.title,
            "unlocked": is_unlocked,
            "prerequisites": node.prerequisites,
            "completed_prerequisites": [p for p in node.prerequisites if p in completed],
            "missing_prerequisites": missing_prereqs
        }

    @server.tool()
    async def compute_socratic_hint(
        node_id: str,
        hint_level: int,
        quiz_question: Optional[str] = None,
        previous_hints: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generates a calibrated 3-tier Socratic scaffolding hint without leaking the answer.

        Args:
            node_id: Active curriculum node ID.
            hint_level: Hint tier level (1: Socratic concept, 2: Structural rubric, 3: Constrained template).
            quiz_question: The active question text (optional).
            previous_hints: List of hints previously delivered in this attempt.
        """
        node = curriculum_graph.get_node_by_id(node_id) or curriculum_graph.nodes[0]
        q_text = quiz_question or f"Explain and apply {node.title}"
        prev = previous_hints or []

        hint_level = max(1, min(3, hint_level))
        hint_text = await quiz_agent.generate_hint(
            node=node,
            quiz_question=q_text,
            hint_number=hint_level,
            previous_hints=prev
        )

        return {
            "node_id": node.id,
            "hint_level": hint_level,
            "hint_text": hint_text,
            "is_last_hint": (hint_level >= 3)
        }

    @server.tool()
    async def grade_prompt_submission(
        node_id: str,
        student_answers: Dict[str, str],
        hints_used: int = 0,
        elapsed_seconds: float = 30.0,
        fail_streak: int = 0
    ) -> Dict[str, Any]:
        """Evaluates student submission using dual-stage semantic LLM-as-a-judge and 5-variable adaptive scoring.

        Args:
            node_id: Target curriculum node ID.
            student_answers: Dict of question ID to student's answer text (e.g. {'q1': '...', 'q2': '...'}).
            hints_used: Number of hints requested during this attempt (0 - 3).
            elapsed_seconds: Time taken to submit in seconds.
            fail_streak: Prior consecutive fail count on this node.
        """
        node = curriculum_graph.get_node_by_id(node_id) or curriculum_graph.nodes[0]
        questions = [
            {"id": "q1", "title": "Core Mechanics", "type": "writing", "question": f"Explain {node.title}"},
            {"id": "q2", "title": "Applied Prompt", "type": "writing", "question": f"Write a prompt for {node.title}"},
            {"id": "q3", "title": "Refinement", "type": "writing", "question": f"Edge case for {node.title}"}
        ]

        breakdown = await evaluator_agent.evaluate_submission(
            node=node,
            questions=questions,
            student_answers=student_answers,
            hints_used=hints_used,
            elapsed_seconds=elapsed_seconds,
            fail_streak=fail_streak
        )

        return breakdown.to_dict()

    @server.tool()
    async def update_learner_progress(
        user_id: str,
        node_id: str,
        score: float,
        passed: bool
    ) -> Dict[str, Any]:
        """Atomically updates learner profile, unlocks subsequent DAG nodes, and transitions tutor state.

        Args:
            user_id: Student unique identifier.
            node_id: Node ID that was attempted.
            score: Final score achieved (0.0 to 1.0).
            passed: Whether the score satisfied the node's passing threshold.
        """
        profile = await get_learner_profile(user_id) or LearnerProfile(user_id=user_id)
        state = await get_tutor_state(user_id) or TutorState(user_id=user_id)

        if passed:
            profile.mark_node_passed(node_id, score)
            StateTransitionController.advance_to_next_node(state, profile)
        else:
            profile.record_node_failure(node_id, score)
            state.phase = TutorPhase.NODE_FAILED

        await save_learner_profile(profile)
        await save_tutor_state(user_id, state, profile.completed_nodes)

        return {
            "user_id": user_id,
            "node_id": node_id,
            "passed": passed,
            "mastery_score": profile.get_mastery(node_id),
            "fail_streak": profile.get_fail_streak(node_id),
            "completed_nodes_count": len(profile.completed_nodes),
            "active_node_id": state.current_node_id,
            "current_phase": state.phase.value
        }

    return server


# Global singleton MCP server instance
mcp_server = create_roar_mcp_server()

if __name__ == "__main__":
    # Allows running as a standalone stdio MCP server for Claude Desktop / Cursor
    asyncio.run(mcp_server.run_stdio_async())
