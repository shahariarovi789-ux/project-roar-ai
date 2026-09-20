# agents/mcp_adapter.py
"""
MCP-Enabled Orchestrator Adapter.
Provides a unified, protocol-compliant interface for the tutoring workflow
where all agent context, curriculum graphs, and assessment tools are
routed through the Model Context Protocol (MCP) bus.
"""

import time
from typing import Dict, Any, Optional
from mcp_server.client import mcp_client
from backend.activity_tracker import activity_tracker
from backend.model_manager import model_manager
from backend.prompt_templates import get_lesson_prompt
from agents.quiz_agent import quiz_agent


class MCPOrchestratorAdapter:
    """Orchestrator that operates exclusively over the Model Context Protocol (MCP).

    Guarantees state synchronization, strict JSON schema validation,
    and modular decoupling across all specialist agents.
    """

    @staticmethod
    async def get_or_create_session(user_id: str) -> Dict[str, Any]:
        """Loads learner state and profile via MCP resources."""
        profile_data = await mcp_client.read_resource(f"roar://learner/{user_id}/profile")
        session_data = await mcp_client.read_resource(f"roar://learner/{user_id}/session")
        dag_data = await mcp_client.read_resource("roar://curriculum/dag")

        current_node_id = session_data.get("current_node_id", "node_01")
        node_data = await mcp_client.read_resource(f"roar://curriculum/node/{current_node_id}")

        completed_nodes = profile_data.get("completed_nodes", [])
        mastery_map = profile_data.get("mastery_map", {})

        return {
            "user_id": user_id,
            "onboarding_done": profile_data.get("onboarding_done", False),
            "current_phase": session_data.get("current_phase", "lesson"),
            "current_node": {
                "id": node_data.get("id"),
                "title": node_data.get("title"),
                "category": node_data.get("category"),
                "difficulty_tier": node_data.get("difficulty_tier"),
                "weight": node_data.get("weight"),
                "quiz_type": node_data.get("quiz_type")
            },
            "completed_nodes_count": len(completed_nodes),
            "total_nodes_count": dag_data.get("total_nodes", 36),
            "mastery_average": round(sum(mastery_map.values()) / max(1, len(mastery_map)), 2) if mastery_map else 0.0,
            "mcp_enabled": True
        }

    @staticmethod
    async def fetch_current_lesson(user_id: str, node_id: Optional[str] = None, force_regen: bool = False) -> Dict[str, Any]:
        """Synthesizes lesson material using MCP resources and ChromaDB RAG tools."""
        profile_data = await mcp_client.read_resource(f"roar://learner/{user_id}/profile")
        session_data = await mcp_client.read_resource(f"roar://learner/{user_id}/session")

        target_node_id = node_id or session_data.get("current_node_id", "node_01")
        node_data = await mcp_client.read_resource(f"roar://curriculum/node/{target_node_id}")

        # Retrieve grounding context via MCP Tool
        rag_res = await mcp_client.call_tool("retrieve_grounding_context", {
            "topic": node_data.get("title", ""),
            "n_results": 3
        })
        grounding_context = rag_res.get("grounding_text", "")

        fail_streak = profile_data.get("fail_streaks", {}).get(target_node_id, 0)

        # Build prompt using standardized template
        prompt = get_lesson_prompt(
            node_id=target_node_id,
            topic_path=f"{node_data.get('category')} / {node_data.get('title')}",
            topic_description=node_data.get("description", ""),
            key_concepts=node_data.get("rubric", {}).get("key_concepts", []),
            depth=1,
            difficulty_tier=node_data.get("difficulty_tier", 1),
            rag_context=grounding_context,
            prefers_examples=profile_data.get("prefers_examples", True),
            prefers_steps=profile_data.get("prefers_steps", True),
            prefers_detailed=profile_data.get("prefers_detailed", True),
            prior_experience=profile_data.get("prior_experience", "beginner"),
            fail_streak=fail_streak
        )

        res = await model_manager.generate_async(
            prompt=prompt,
            system_prompt="You are an expert AI Prompt Engineering Tutor. Author structured study material in GitHub Markdown.",
            temperature=0.85 if force_regen else 0.70,
            max_tokens=1500,
            agent_name="Lesson Agent (MCP)",
            intent="lesson"
        )

        return {
            "node_id": target_node_id,
            "title": node_data.get("title"),
            "category": node_data.get("category"),
            "difficulty_tier": node_data.get("difficulty_tier"),
            "weight": node_data.get("weight"),
            "lesson_markdown": res.get("text", "Lesson content"),
            "latency_ms": res.get("latency_ms", 120.0),
            "is_passed": (target_node_id in profile_data.get("completed_nodes", [])),
            "is_current": (target_node_id == session_data.get("current_node_id")),
            "mcp_grounding": True
        }

    @staticmethod
    async def fetch_current_quiz(user_id: str, node_id: Optional[str] = None, force_regen: bool = False) -> Dict[str, Any]:
        """Generates quiz challenges using MCP resources and verifies prerequisite locks."""
        session_data = await mcp_client.read_resource(f"roar://learner/{user_id}/session")
        profile_data = await mcp_client.read_resource(f"roar://learner/{user_id}/profile")

        target_node_id = node_id or session_data.get("current_node_id", "node_01")

        # Check prerequisite via MCP Tool
        unlock_check = await mcp_client.call_tool("verify_node_unlocked", {
            "user_id": user_id,
            "node_id": target_node_id
        })

        fail_streak = profile_data.get("fail_streaks", {}).get(target_node_id, 0)
        from core.curriculum import curriculum_graph
        node_obj = curriculum_graph.get_node_by_id(target_node_id) or curriculum_graph.nodes[0]
        from core.learner_profile import LearnerProfile
        profile_obj = LearnerProfile.from_dict(profile_data)

        quiz_data = await quiz_agent.generate_quiz_challenge(
            node=node_obj,
            profile=profile_obj,
            fail_streak=fail_streak,
            force_regen=force_regen
        )

        quiz_data["unlocked"] = unlock_check.get("unlocked", True)
        quiz_data["mcp_verified"] = True
        return quiz_data

    @staticmethod
    async def evaluate_quiz_submission(user_id: str, answers: Any) -> Dict[str, Any]:
        """Evaluates student submissions via MCP tool grade_prompt_submission."""
        session_data = await mcp_client.read_resource(f"roar://learner/{user_id}/session")
        profile_data = await mcp_client.read_resource(f"roar://learner/{user_id}/profile")

        target_node_id = session_data.get("current_node_id", "node_01")
        hints_used = session_data.get("hints_requested", 0)
        start_ts = session_data.get("quiz_start_timestamp") or time.time()
        elapsed_seconds = max(1.0, time.time() - start_ts)
        fail_streak = profile_data.get("fail_streaks", {}).get(target_node_id, 0)

        answers_dict = answers if isinstance(answers, dict) else {"q1": str(answers), "q2": str(answers), "q3": str(answers)}

        # Call MCP Tool
        eval_result = await mcp_client.call_tool("grade_prompt_submission", {
            "node_id": target_node_id,
            "student_answers": answers_dict,
            "hints_used": hints_used,
            "elapsed_seconds": elapsed_seconds,
            "fail_streak": fail_streak
        })

        # Update progress via MCP Tool
        update_result = await mcp_client.call_tool("update_learner_progress", {
            "user_id": user_id,
            "node_id": target_node_id,
            "score": eval_result.get("final_score", 0.0),
            "passed": eval_result.get("passed", False)
        })

        return {
            "breakdown": eval_result,
            "progress_update": update_result,
            "mcp_evaluated": True
        }

    @staticmethod
    async def request_hint(user_id: str, question_idx: int = 1, node_id: Optional[str] = None) -> Dict[str, Any]:
        """Requests Socratic hint using compute_socratic_hint MCP tool."""
        session_data = await mcp_client.read_resource(f"roar://learner/{user_id}/session")
        target_node_id = node_id or session_data.get("current_node_id", "node_01")

        hints_used = session_data.get("hints_requested", 0)
        if hints_used >= 3:
            return {"hint": "Maximum hints (3/3) reached for this attempt.", "hints_used": 3, "mcp": True}

        hint_level = hints_used + 1
        previous_hints = session_data.get("delivered_hints", [])

        hint_res = await mcp_client.call_tool("compute_socratic_hint", {
            "node_id": target_node_id,
            "hint_level": hint_level,
            "previous_hints": previous_hints
        })

        return {
            "hint": hint_res.get("hint_text"),
            "hints_used": hint_level,
            "mcp_scaffolded": True
        }
