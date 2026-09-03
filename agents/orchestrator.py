# agents/orchestrator.py
"""
Orchestrator Supervisor Agent.
Coordinates state transitions, agent invocation, multi-question challenge workflows,
telemetry logging, and live activity tracking.
"""

from typing import Dict, Any, List, Optional
from core.curriculum import curriculum_graph, CurriculumNode
from core.learner_profile import LearnerProfile
from core.state_machine import TutorState, TutorPhase, StateTransitionController
from agents.onboarding_agent import OnboardingAgent
from agents.lesson_agent import lesson_agent
from agents.quiz_agent import quiz_agent
from agents.evaluator_agent import evaluator_agent
from backend.model_manager import model_manager
from backend.activity_tracker import activity_tracker
from db.storage import (
    get_learner_profile, save_learner_profile,
    get_tutor_state, save_tutor_state,
    record_quiz_attempt, log_research_metric, log_analytics_event
)


class TutorOrchestrator:
    @staticmethod
    async def get_or_create_session(user_id: str) -> Dict[str, Any]:
        """Loads or initializes learner state and profile."""
        profile = await get_learner_profile(user_id)
        if not profile:
            profile = LearnerProfile(user_id=user_id)
            await save_learner_profile(profile)

        state = await get_tutor_state(user_id)
        if not state:
            state = TutorState(user_id=user_id)
            await save_tutor_state(user_id, state, profile.completed_nodes)

        current_node = curriculum_graph.get_node_by_id(state.current_node_id) or curriculum_graph.nodes[0]

        return {
            "user_id": user_id,
            "phase": state.phase.value,
            "profile": profile.to_dict(),
            "state": state.to_dict(),
            "current_node": {
                "id": current_node.id,
                "title": current_node.title,
                "path": current_node.path,
                "category": current_node.category,
                "difficulty_tier": current_node.difficulty_tier,
                "weight": current_node.weight,
                "quiz_type": current_node.quiz_type
            },
            "completed_nodes_count": len(profile.completed_nodes),
            "total_nodes_count": len(curriculum_graph.nodes),
            "mastery_average": round(sum(profile.mastery_map.values()) / max(1, len(profile.mastery_map)), 2) if profile.mastery_map else 0.0,
            "recent_activity": activity_tracker.get_recent(15)
        }

    @staticmethod
    async def fetch_current_lesson(user_id: str, node_id: Optional[str] = None, force_regen: bool = False) -> Dict[str, Any]:
        profile = await get_learner_profile(user_id) or LearnerProfile(user_id=user_id)
        state = await get_tutor_state(user_id) or TutorState(user_id=user_id)
        
        target_node_id = node_id or state.current_node_id
        node = curriculum_graph.get_node_by_id(target_node_id) or curriculum_graph.nodes[0]
        
        fail_streak = profile.get_fail_streak(node.id)
        lesson_data = await lesson_agent.generate_lesson(node, profile, fail_streak=fail_streak, force_regen=force_regen)
        
        # Log research metric
        await log_research_metric(
            user_id=user_id,
            llm_backend=model_manager.backend,
            llm_model=model_manager.current_model,
            node_id=node.id,
            latency_ms=lesson_data["latency_ms"],
            tokens_used=len(lesson_data["lesson_markdown"].split()),
            quality_score=1.0
        )
        lesson_data["recent_activity"] = activity_tracker.get_recent(10)
        lesson_data["is_passed"] = (node.id in profile.completed_nodes)
        lesson_data["is_current"] = (node.id == state.current_node_id)
        return lesson_data

    @staticmethod
    async def fetch_current_quiz(user_id: str, node_id: Optional[str] = None, force_regen: bool = False) -> Dict[str, Any]:
        profile = await get_learner_profile(user_id) or LearnerProfile(user_id=user_id)
        state = await get_tutor_state(user_id) or TutorState(user_id=user_id)
        
        target_node_id = node_id or state.current_node_id
        node = curriculum_graph.get_node_by_id(target_node_id) or curriculum_graph.nodes[0]
        
        fail_streak = profile.get_fail_streak(node.id)
        quiz_data = await quiz_agent.generate_quiz_challenge(node, profile, fail_streak=fail_streak, force_regen=force_regen)
        
        # Update state with quiz questions and start timer
        StateTransitionController.start_quiz(state, node, reset_timer=True)
        state.current_quiz_questions = quiz_data.get("questions", [])
        state.current_quiz_text = f"Assessment for {node.title} with {len(state.current_quiz_questions)} questions"
        await save_tutor_state(user_id, state, profile.completed_nodes)

        quiz_data["recent_activity"] = activity_tracker.get_recent(10)
        quiz_data["is_passed"] = (node.id in profile.completed_nodes)
        return quiz_data


    @staticmethod
    async def evaluate_quiz_submission(user_id: str, answers: Any) -> Dict[str, Any]:
        """
        Evaluates student submission for the 3 questions.
        Supports both dict: {"q1": ans1, "q2": ans2, "q3": ans3} or single string.
        """
        import time
        profile = await get_learner_profile(user_id) or LearnerProfile(user_id=user_id)
        state = await get_tutor_state(user_id) or TutorState(user_id=user_id)
        node = curriculum_graph.get_node_by_id(state.current_node_id) or curriculum_graph.nodes[0]

        start_ts = state.quiz_start_timestamp or time.time()
        elapsed_seconds = max(1.0, time.time() - start_ts)
        hints_used = state.hints_requested
        fail_streak = profile.get_fail_streak(node.id)

        questions = state.current_quiz_questions
        if not questions:
            # Fallback if questions weren't stored in state
            questions = [
                {"id": "q1", "title": "Core Mechanics", "type": "writing", "question": f"Explain {node.title}"},
                {"id": "q2", "title": "Applied Prompt", "type": "writing", "question": f"Write a prompt for {node.title}"},
                {"id": "q3", "title": "Refinement", "type": "writing", "question": f"Edge case for {node.title}"}
            ]

        # Normalize answers to dict
        answers_dict = {}
        if isinstance(answers, dict):
            answers_dict = answers
        else:
            # If string submitted, map to all questions
            for q in questions:
                answers_dict[q.get("id", "q1")] = str(answers)

        # Run multi-question evaluator agent
        breakdown = await evaluator_agent.evaluate_submission(
            node=node,
            questions=questions,
            student_answers=answers_dict,
            hints_used=hints_used,
            elapsed_seconds=elapsed_seconds,
            fail_streak=fail_streak
        )

        breakdown_dict = breakdown.to_dict()

        # Update State & Learner Profile
        StateTransitionController.on_quiz_evaluated(state, profile, breakdown_dict)
        await save_learner_profile(profile)
        await save_tutor_state(user_id, state, profile.completed_nodes)

        # Record attempt in database
        attempt_id = await record_quiz_attempt(
            user_id=user_id,
            node_id=node.id,
            quiz_type=node.quiz_type,
            answer_text=str(answers_dict),
            semantic_score=breakdown.semantic_score,
            rule_score=breakdown.rule_score,
            final_score=breakdown.final_score,
            required_score=breakdown.passing_threshold,
            passed=breakdown.passed,
            hints_used=hints_used,
            time_elapsed_s=elapsed_seconds,
            fail_streak_before=fail_streak,
            llm_rationale=breakdown.rationale
        )

        return {
            "attempt_id": attempt_id,
            "breakdown": breakdown_dict,
            "current_phase": state.phase.value,
            "completed_nodes": profile.completed_nodes,
            "recent_activity": activity_tracker.get_recent(15)
        }

    @staticmethod
    async def request_hint(user_id: str, question_idx: int = 1, node_id: Optional[str] = None) -> Dict[str, Any]:
        state = await get_tutor_state(user_id) or TutorState(user_id=user_id)
        target_node_id = node_id or state.current_node_id
        node = curriculum_graph.get_node_by_id(target_node_id) or curriculum_graph.nodes[0]

        if state.hints_requested >= 3:
            return {"hint": "Maximum hints (3/3) reached for this attempt.", "hints_used": 3}

        state.hints_requested += 1
        q_text = node.title
        if state.current_quiz_questions and len(state.current_quiz_questions) >= question_idx:
            q_text = state.current_quiz_questions[question_idx - 1].get("question", node.title)

        delivered = getattr(state, "delivered_hints", None)
        if delivered is None:
            delivered = []
            state.delivered_hints = delivered

        hint_text = await quiz_agent.generate_hint(
            node=node,
            quiz_question=q_text,
            hint_number=state.hints_requested,
            previous_hints=delivered
        )
        delivered.append(hint_text)
        state.delivered_hints = delivered

        profile = await get_learner_profile(user_id) or LearnerProfile(user_id=user_id)
        await save_tutor_state(user_id, state, profile.completed_nodes)

        await log_analytics_event(user_id, "hint_requested", {"node_id": node.id, "hint_num": state.hints_requested})
        return {
            "hint": hint_text,
            "hints_used": state.hints_requested,
            "recent_activity": activity_tracker.get_recent(5)
        }


    @staticmethod
    async def advance_node(user_id: str) -> Dict[str, Any]:
        profile = await get_learner_profile(user_id) or LearnerProfile(user_id=user_id)
        state = await get_tutor_state(user_id) or TutorState(user_id=user_id)

        activity_tracker.log("Orchestrator", f"Passed node {state.current_node_id}. Resolving next unlocked node...", "", "info")
        StateTransitionController.advance_to_next_node(state, profile)
        await save_learner_profile(profile)
        await save_tutor_state(user_id, state, profile.completed_nodes)

        activity_tracker.log("Orchestrator", f"Current active node is now: {state.current_node_id}", "", "success")
        return await TutorOrchestrator.get_or_create_session(user_id)
