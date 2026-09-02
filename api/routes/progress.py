# api/routes/progress.py
"""
Progress & Curriculum Mastery Map Endpoints.
"""

from fastapi import APIRouter, Depends
from api.middleware import get_current_user_id
from core.curriculum import curriculum_graph
from db.storage import get_learner_profile, get_all_mastery_scores

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/tree")
async def get_curriculum_tree(user_id: str = Depends(get_current_user_id)):
    """Returns the full 37-node learning tree with student's unlock status and mastery scores."""
    profile = await get_learner_profile(user_id)
    mastery_scores = await get_all_mastery_scores(user_id)
    completed_set = set(profile.completed_nodes) if profile else set()

    nodes_state = []
    for node in curriculum_graph.nodes:
        unlocked = curriculum_graph.is_unlocked(node.id, completed_set)
        passed = node.id in completed_set
        node_mastery = mastery_scores.get(node.id, {}).get("mastery_score", 0.0)

        nodes_state.append({
            "id": node.id,
            "title": node.title,
            "path": node.path,
            "category": node.category,
            "depth": node.depth,
            "difficulty_tier": node.difficulty_tier,
            "weight": node.weight,
            "bloom_level": node.bloom_level,
            "quiz_type": node.quiz_type,
            "prerequisites": node.prerequisites,
            "description": node.description,
            "is_unlocked": unlocked,
            "is_passed": passed,
            "is_current": (node.id == profile.current_node_id) if profile else False,
            "mastery_score": node_mastery
        })

    return {
        "curriculum_version": curriculum_graph.version,
        "total_nodes": len(curriculum_graph.nodes),
        "completed_nodes_count": len(completed_set),
        "overall_progress_percentage": round((len(completed_set) / len(curriculum_graph.nodes)) * 100, 1),
        "nodes": nodes_state
    }
