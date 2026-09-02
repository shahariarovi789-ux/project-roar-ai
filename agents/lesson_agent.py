# agents/lesson_agent.py
"""
Lesson Agent.
Generates genuine, personalized, and non-static study materials for curriculum nodes
using ChromaDB RAG retrieval and real LLM inference.
"""

import random
from typing import Dict, Any, Optional
from core.curriculum import CurriculumNode
from core.learner_profile import LearnerProfile
from backend.model_manager import model_manager
from backend.prompt_templates import get_lesson_prompt
from backend.activity_tracker import activity_tracker
from agents.rag_agent import rag_agent


class LessonAgent:
    @staticmethod
    async def generate_lesson(
        node: CurriculumNode,
        profile: LearnerProfile,
        fail_streak: int = 0,
        force_regen: bool = False
    ) -> Dict[str, Any]:
        """
        Dynamically generates personalized, non-static lesson material for the targeted node.
        Supports force_regen for on-demand synthesis of fresh variations with diverse analogies.
        """
        regen_tag = " (Fresh Regeneration)" if force_regen else ""
        activity_tracker.log("Lesson Agent", f"Initiating lesson generation for: {node.title}{regen_tag}", f"Tier {node.difficulty_tier} (Weight: {node.weight})", "running")

        # 1. Retrieve RAG context from vector database
        activity_tracker.log("Lesson Agent", "Querying ChromaDB vector store...", f"Query: '{node.path}'", "running")
        rag_context = rag_agent.retrieve_context(f"{node.path} {node.description}", top_k=3)
        if rag_context:
            activity_tracker.log("Lesson Agent", "Retrieved 3 domain knowledge chunks from ChromaDB", "RAG Active", "success")

        # 2. Build focused system prompt
        custom_system_prompt = (
            "You are an elite, highly engaging AI Prompt Engineering Professor. "
            f"Your objective is to teach '{node.title}' clearly and practically. "
            "Focus purely on prompt engineering techniques, prompt anatomy, and concrete before/after prompt demonstrations."
        )

        prompt = get_lesson_prompt(
            node_id=node.id,
            topic_path=node.path,
            topic_description=node.description,
            key_concepts=node.rubric.get("key_concepts", []),
            depth=node.depth,
            difficulty_tier=node.difficulty_tier,
            rag_context=rag_context,
            prefers_examples=profile.prefers_examples,
            prefers_steps=profile.prefers_steps,
            prefers_detailed=profile.prefers_detailed,
            prior_experience=profile.prior_experience,
            fail_streak=fail_streak
        )

        if force_regen:
            variation_domains = ["Software Engineering & API Automation", "Data Science & Structured Analytics", "Creative Writing & Content Synthesis", "Technical Documentation & System Prompts", "Financial Analysis & Compliance Extraction"]
            chosen_domain = random.choice(variation_domains)
            prompt += f"\n\n### VARIATION REGENERATION DIRECTIVE:\nThe student requested a fresh alternative explanation. Use a unique scenario and practical before/after prompt grounded in the domain of: '{chosen_domain}'. Keep it crisp, highly practical, and distinct from standard templates."

        # 3. Genuine LLM inference call with active temperature
        res = await model_manager.generate_async(
            prompt=prompt,
            system_prompt=custom_system_prompt,
            temperature=0.85 if force_regen else 0.7,
            max_tokens=1500,
            agent_name="Lesson Agent",
            intent="lesson"
        )

        activity_tracker.log("Lesson Agent", f"Lesson generation completed in {res['latency_ms']}ms", f"Model: {res['model']}", "success")

        return {
            "node_id": node.id,
            "topic_title": node.title,
            "topic_path": node.path,
            "category": node.category,
            "difficulty_tier": node.difficulty_tier,
            "weight": node.weight,
            "bloom_level": node.bloom_level,
            "lesson_markdown": res["text"],
            "rag_sources_used": bool(rag_context),
            "latency_ms": res["latency_ms"],
            "model_used": res["model"]
        }


# Global singleton instance
lesson_agent = LessonAgent()
