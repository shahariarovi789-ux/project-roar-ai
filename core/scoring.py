# core/scoring.py
"""
Adaptive Scoring Engine & Multi-Criteria Evaluator.
Implements the research-calibrated 5-variable equation:
S_final = max(0, alpha * Q_sem + beta * Q_rule - gamma * H - delta * T_p - epsilon * R_fail)
"""

import re
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from core.curriculum import CurriculumNode


@dataclass
class ScoreBreakdown:
    semantic_score: float         # Q_sem (0.0 to 1.0)
    rule_score: float             # Q_rule (0.0 to 1.0)
    hint_penalty: float           # gamma * H
    time_penalty: float           # delta * T_p
    retry_penalty: float          # epsilon * R_fail
    raw_score: float              # alpha * Q_sem + beta * Q_rule
    final_score: float            # S_final
    passing_threshold: float      # S_pass
    passed: bool                  # S_final >= S_pass
    hints_used: int
    time_elapsed_seconds: float
    time_budget_seconds: float
    fail_streak: int
    rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ScoringEngine:
    # Calibrated thesis weights
    ALPHA = 0.50      # Weight for Semantic LLM-as-judge Score
    BETA = 0.50       # Weight for Structural Rubric / Accuracy Score
    GAMMA = 0.05      # Penalty per hint used (max 3 hints = -0.15)
    DELTA = 0.05      # Penalty if time threshold is exceeded
    EPSILON = 0.01    # Penalty per consecutive failure streak (capped at 0.04)

    @classmethod
    def extract_float_from_llm(cls, text: str, default: float = 0.80) -> float:
        """
        Robustly extracts a float score (0.0 to 1.0) from LLM output.
        Strips DeepSeek-R1 <think> ... </think> tokens, parses JSON blocks if present,
        and uses regex fallback.
        """
        if not text:
            return 0.0


        # 1. Strip reasoning <think> ... </think> tags
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

        # 2. Try parsing direct JSON
        json_match = re.search(r"\{.*?\}", cleaned, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                if "score" in data:
                    val = float(data["score"])
                    return max(0.0, min(1.0, val))
            except Exception:
                pass

        # 3. Search for numbers between 0.0 and 1.0 or integers 0 / 1
        matches = re.findall(r"(?:score\s*[:=]\s*)?([0-1](?:\.\d+)?|0\.\d+)", cleaned, re.IGNORECASE)
        if matches:
            try:
                val = float(matches[-1])
                return max(0.0, min(1.0, val))
            except Exception:
                pass

        return default

    @classmethod
    def evaluate_rule_rubric(cls, answer: str, node: CurriculumNode) -> float:
        """
        Evaluates structural and semantic compliance against node's dynamic rubric.
        Combines concept keyword coverage, length constraint, and structural markers.
        """
        text = (answer or "").strip()
        if not text:
            return 0.0

        rubric = node.rubric or {}
        text_lower = text.lower()
        score = 0.0
        total_checks = 0

        # Check 1: Key concepts presence
        key_concepts = rubric.get("key_concepts", [])
        if key_concepts:
            total_checks += 1
            matched_concepts = sum(1 for c in key_concepts if c.lower() in text_lower)
            concept_ratio = matched_concepts / len(key_concepts)
            score += 0.4 * min(1.0, concept_ratio * 1.5)  # Generous curve

        # Check 2: Structural markers presence
        markers = rubric.get("structural_markers", [])
        if markers:
            total_checks += 1
            matched_markers = sum(1 for m in markers if m.lower() in text_lower)
            marker_ratio = matched_markers / max(1, len(markers) // 2)
            score += 0.4 * min(1.0, marker_ratio)

        # Check 3: Word count minimum
        min_words = rubric.get("min_length_words", 5)
        word_count = len(text.split())
        total_checks += 1
        if word_count >= min_words:
            score += 0.2
        else:
            score += 0.2 * (word_count / max(1, min_words))

        # Fallback if no specific rubric defined
        if total_checks == 0:
            return 0.85 if word_count >= 8 else 0.50

        return round(min(1.0, max(0.50, score)), 2)

    @classmethod
    def compute_composite_score(
        cls,
        semantic_score: float,
        rule_score: float,
        hints_used: int = 0,
        elapsed_seconds: float = 0.0,
        node: Optional[CurriculumNode] = None,
        time_budget_seconds: Optional[float] = None,
        passing_threshold: Optional[float] = None,
        fail_streak: int = 0,
        rationale: str = ""
    ) -> ScoreBreakdown:
        """Computes the final composite score and breakdown."""
        time_budget = time_budget_seconds or (node.time_budget_seconds if node else 240.0)
        passing_req = passing_threshold or (node.passing_threshold if node else 0.50)
        
        # Raw score
        raw = cls.ALPHA * semantic_score + cls.BETA * rule_score
        
        # Penalties
        hint_pen = round(cls.GAMMA * min(3, max(0, hints_used)), 3)
        time_pen = cls.DELTA if elapsed_seconds > time_budget else 0.0
        retry_pen = round(min(0.04, cls.EPSILON * max(0, fail_streak)), 3)
        
        # Final calculation
        final = raw - hint_pen - time_pen - retry_pen
        final_clamped = max(0.0, min(1.0, round(final, 2)))
        
        passed = final_clamped >= passing_req

        return ScoreBreakdown(
            semantic_score=round(semantic_score, 2),
            rule_score=round(rule_score, 2),
            hint_penalty=hint_pen,
            time_penalty=time_pen,
            retry_penalty=retry_pen,
            raw_score=round(raw, 2),
            final_score=final_clamped,
            passing_threshold=passing_req,
            passed=passed,
            hints_used=hints_used,
            time_elapsed_seconds=round(elapsed_seconds, 1),
            time_budget_seconds=time_budget,
            fail_streak=fail_streak,
            rationale=rationale
        )
