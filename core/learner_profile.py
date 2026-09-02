# core/learner_profile.py
"""
Learner Profile representation capturing intake questionnaire metadata,
learning preferences, session time budgets, and runtime mastery state.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional
import json


@dataclass
class LearnerProfile:
    user_id: str
    name: str = ""
    
    # Onboarding preferences
    prior_experience: str = "beginner"       # "beginner", "intermediate", "expert"
    prefers_examples: bool = True            # Example-first vs Theory-first
    prefers_steps: bool = True               # Step-by-step vs High-level
    prefers_detailed: bool = True            # Detailed vs Brief
    preferred_quiz_style: str = "mixed"      # "mcq", "writing", "mixed"
    session_time_budget: int = 30            # Minutes per session (15, 30, 60)
    onboarding_done: bool = False

    # Runtime tracking
    current_node_id: str = "node_01"
    completed_nodes: List[str] = field(default_factory=list)
    mastery_map: Dict[str, float] = field(default_factory=dict)     # node_id -> score (0.0 - 1.0)
    fail_streaks: Dict[str, int] = field(default_factory=dict)      # node_id -> consecutive fail count
    
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LearnerProfile":
        allowed_fields = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in data.items() if k in allowed_fields}
        return cls(**filtered)

    def mark_node_passed(self, node_id: str, score: float):
        if node_id not in self.completed_nodes:
            self.completed_nodes.append(node_id)
        self.mastery_map[node_id] = round(max(self.mastery_map.get(node_id, 0.0), score), 2)
        self.fail_streaks[node_id] = 0
        self.updated_at = datetime.utcnow().isoformat()

    def record_node_failure(self, node_id: str, score: float):
        self.fail_streaks[node_id] = self.fail_streaks.get(node_id, 0) + 1
        self.mastery_map[node_id] = round(score, 2)
        self.updated_at = datetime.utcnow().isoformat()

    def get_fail_streak(self, node_id: str) -> int:
        return self.fail_streaks.get(node_id, 0)

    def get_mastery(self, node_id: str) -> float:
        return self.mastery_map.get(node_id, 0.0)

    def is_expert(self) -> bool:
        return self.prior_experience.lower() == "expert"
