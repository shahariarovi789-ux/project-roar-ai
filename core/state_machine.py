# core/state_machine.py
"""
Finite State Machine & Workflow Transitions for the Tutoring Orchestrator.
Defines valid state transitions across ONBOARDING, LESSON, QUIZ, EVALUATING, FINAL_EXAM.
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Set
from core.learner_profile import LearnerProfile
from core.curriculum import curriculum_graph, CurriculumNode


class TutorPhase(str, Enum):
    ONBOARDING = "ONBOARDING"
    LESSON = "LESSON"
    QUIZ = "QUIZ"
    EVALUATING = "EVALUATING"
    NODE_PASSED = "NODE_PASSED"
    NODE_FAILED = "NODE_FAILED"
    FINAL_EXAM_PHASE_A = "FINAL_EXAM_PHASE_A"   # MCQ Theory
    FINAL_EXAM_PHASE_B = "FINAL_EXAM_PHASE_B"   # Applied Writing
    FINAL_EXAM_PHASE_C = "FINAL_EXAM_PHASE_C"   # Portfolio Critique
    FINAL_EXAM_COMPLETE = "FINAL_EXAM_COMPLETE"
    COURSE_COMPLETE = "COURSE_COMPLETE"


@dataclass
class TutorState:
    user_id: str
    phase: TutorPhase = TutorPhase.ONBOARDING
    current_node_id: str = "node_01"
    
    # Quiz runtime tracking
    current_quiz_text: str = ""
    current_quiz_questions: List[Dict[str, Any]] = field(default_factory=list)
    current_quiz_type: str = "mcq_definition"
    hints_requested: int = 0
    delivered_hints: List[str] = field(default_factory=list)
    quiz_start_timestamp: Optional[float] = None
    last_score_breakdown: Optional[Dict[str, Any]] = None
    
    # Final exam tracking
    final_exam_scores: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["phase"] = self.phase.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TutorState":
        data_copy = dict(data)
        if "phase" in data_copy and isinstance(data_copy["phase"], str):
            data_copy["phase"] = TutorPhase(data_copy["phase"])
        allowed = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in data_copy.items() if k in allowed}
        return cls(**filtered)


class StateTransitionController:
    """Manages legal state transitions and next-action decisions."""

    @staticmethod
    def on_onboarding_completed(state: TutorState, profile: LearnerProfile) -> TutorPhase:
        profile.onboarding_done = True
        state.phase = TutorPhase.LESSON
        return state.phase

    @staticmethod
    def start_quiz(state: TutorState, node: CurriculumNode, reset_timer: bool = True) -> TutorPhase:
        import time
        state.phase = TutorPhase.QUIZ
        state.current_quiz_type = node.quiz_type
        if reset_timer:
            state.quiz_start_timestamp = time.time()
            state.hints_requested = 0
            state.delivered_hints = []
        return state.phase


    @staticmethod
    def on_quiz_evaluated(
        state: TutorState,
        profile: LearnerProfile,
        score_breakdown: Dict[str, Any]
    ) -> TutorPhase:
        state.last_score_breakdown = score_breakdown
        passed = score_breakdown.get("passed", False)
        final_score = score_breakdown.get("final_score", 0.0)

        if passed:
            profile.mark_node_passed(state.current_node_id, final_score)
            state.phase = TutorPhase.NODE_PASSED
        else:
            profile.record_node_failure(state.current_node_id, final_score)
            state.phase = TutorPhase.NODE_FAILED
            
        return state.phase

    @staticmethod
    def advance_to_next_node(state: TutorState, profile: LearnerProfile) -> TutorPhase:
        completed_set = set(profile.completed_nodes)
        
        # Check if all 37 nodes are passed
        if len(completed_set) >= len(curriculum_graph.nodes):
            state.phase = TutorPhase.FINAL_EXAM_PHASE_A
            return state.phase

        next_node = curriculum_graph.get_next_node(state.current_node_id, completed_set)
        if next_node:
            state.current_node_id = next_node.id
            profile.current_node_id = next_node.id
            state.phase = TutorPhase.LESSON
            state.hints_requested = 0
            state.last_score_breakdown = None
            state.current_quiz_questions = []
        else:
            state.phase = TutorPhase.FINAL_EXAM_PHASE_A
            
        return state.phase

    @staticmethod
    def retry_current_node(state: TutorState) -> TutorPhase:
        """After failure, return to lesson with easier scaffolding."""
        state.phase = TutorPhase.LESSON
        state.hints_requested = 0
        state.current_quiz_questions = []
        return state.phase
