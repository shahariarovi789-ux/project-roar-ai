# core/curriculum.py
"""
Curriculum Ontology & Knowledge Graph Representation for Prompt Engineering Tutor.
Enhanced with dynamic rubrics, quiz_types, prerequisite graph validation, and topological sorting.
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "curriculum_tree.json"


@dataclass
class CurriculumNode:
    id: str
    title: str
    path: str
    category: str
    depth: int
    difficulty_tier: int          # 1 (Foundational), 2 (Intermediate), 3 (Advanced)
    weight: float                 # Continuous difficulty & cognitive weight (1.0 to 4.0)
    bloom_level: str              # Remember, Understand, Apply, Analyze, Evaluate, Create
    quiz_type: str                # mcq_definition, prompt_writing, construction_critique, code_prompt, scenario_analysis
    prerequisites: List[str] = field(default_factory=list)
    description: str = ""
    rubric: Dict[str, Any] = field(default_factory=dict)

    @property
    def passing_threshold(self) -> float:
        """Returns the required passing score for this node's difficulty tier."""
        thresholds = {1: 0.50, 2: 0.60, 3: 0.70}
        return thresholds.get(self.difficulty_tier, 0.60)

    @property
    def time_budget_seconds(self) -> float:
        """Dynamic time budget: T = 180 + 60 * Weight (4 to 7 minutes for 3-question quizzes)."""
        return round(180.0 + 60.0 * self.weight, 1)



class CurriculumGraph:
    def __init__(self, data_path: Optional[Path] = None):
        path = data_path or DATA_FILE
        if not path.exists():
            raise FileNotFoundError(f"Curriculum data file not found at: {path}")

        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        self.version = raw.get("curriculum_version", "2.0")
        self.difficulty_scale = raw.get("difficulty_scale", {})
        self.nodes: List[CurriculumNode] = [
            CurriculumNode(**item) for item in raw.get("nodes", [])
        ]
        self._id_map: Dict[str, CurriculumNode] = {n.id: n for n in self.nodes}

    def get_node_by_id(self, node_id: str) -> Optional[CurriculumNode]:
        return self._id_map.get(node_id)

    def get_nodes_by_tier(self, tier: int) -> List[CurriculumNode]:
        return [n for n in self.nodes if n.difficulty_tier == tier]

    def total_weight(self) -> float:
        return round(sum(n.weight for n in self.nodes), 2)

    def get_prerequisite_nodes(self, node_id: str) -> List[CurriculumNode]:
        node = self.get_node_by_id(node_id)
        if not node:
            return []
        return [self._id_map[pid] for pid in node.prerequisites if pid in self._id_map]

    def is_unlocked(self, node_id: str, completed_node_ids: Set[str]) -> bool:
        """A node is unlocked if all its prerequisites are in completed_node_ids."""
        node = self.get_node_by_id(node_id)
        if not node:
            return False
        return all(p in completed_node_ids for p in node.prerequisites)

    def get_ordered_sequence(self) -> List[CurriculumNode]:
        """
        Returns topological ordering of nodes respecting prerequisites,
        fallback to list order if cycles are absent.
        """
        visited = set()
        order = []

        def visit(node: CurriculumNode):
            if node.id in visited:
                return
            for pid in node.prerequisites:
                if pid in self._id_map and pid not in visited:
                    visit(self._id_map[pid])
            visited.add(node.id)
            order.append(node)

        for n in self.nodes:
            visit(n)
        return order

    def get_next_node(self, current_node_id: str, completed_node_ids: Set[str]) -> Optional[CurriculumNode]:
        """Finds the next logical unlocked, uncompleted node."""
        ordered = self.get_ordered_sequence()
        # First check right after current
        found_current = False
        for node in ordered:
            if found_current:
                if node.id not in completed_node_ids and self.is_unlocked(node.id, completed_node_ids):
                    return node
            if node.id == current_node_id:
                found_current = True

        # Fallback: scan from start for any unlocked uncompleted node
        for node in ordered:
            if node.id not in completed_node_ids and self.is_unlocked(node.id, completed_node_ids):
                return node
        return None

    def summary_stats(self) -> Dict[str, Any]:
        tier_counts = {1: 0, 2: 0, 3: 0}
        tier_weights = {1: 0.0, 2: 0.0, 3: 0.0}
        quiz_type_counts: Dict[str, int] = {}

        for n in self.nodes:
            tier_counts[n.difficulty_tier] += 1
            tier_weights[n.difficulty_tier] += n.weight
            quiz_type_counts[n.quiz_type] = quiz_type_counts.get(n.quiz_type, 0) + 1

        return {
            "total_nodes": len(self.nodes),
            "total_curriculum_weight": self.total_weight(),
            "tier_distribution": {
                "Tier 1 (Foundational)": {"count": tier_counts[1], "weight_sum": round(tier_weights[1], 2)},
                "Tier 2 (Intermediate)": {"count": tier_counts[2], "weight_sum": round(tier_weights[2], 2)},
                "Tier 3 (Advanced)": {"count": tier_counts[3], "weight_sum": round(tier_weights[3], 2)},
            },
            "quiz_type_distribution": quiz_type_counts
        }


# Global singleton instance for easy import
curriculum_graph = CurriculumGraph()

if __name__ == "__main__":
    stats = curriculum_graph.summary_stats()
    print("=== Enhanced Curriculum Graph Summary ===")
    print(json.dumps(stats, indent=2))
