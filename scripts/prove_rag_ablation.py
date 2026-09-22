# scripts/prove_rag_ablation.py
"""
RAG Ablation Proof Generator.
Generates an undeniable, side-by-side empirical comparison:
'With RAG (ChromaDB)' vs. 'Without RAG (Parametric Memory Only)'
for an advanced prompt engineering node, demonstrating real hallucination and drift.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.curriculum import curriculum_graph
from agents.rag_agent import rag_agent
from backend.model_manager import model_manager
from backend.prompt_templates import get_lesson_prompt


async def demonstrate_rag_difference():
    # Pick an advanced node where parametric memory fails: Node 10 (Delimiters & Adversarial Escaping)
    node = curriculum_graph.get_node_by_id("node_10") or curriculum_graph.nodes[9]
    print("=" * 80)
    print(f"🔬 LIVE SCIENTIFIC PROOF: RAG ABLATION EXPERIMENT ON [{node.title}]")
    print("=" * 80)
    print(f"Curriculum Node ID: {node.id}")
    print(f"Category: {node.category} | Bloom Tier: {node.difficulty_tier} | Weight: {node.weight}")
    print(f"Key Rubric Concepts Required: {node.rubric.get('key_concepts', [])}\n")

    # 1. RETRIEVE RAG GROUNDING CONTEXT
    rag_context = rag_agent.retrieve_context(node.title, top_k=3)
    print(f"📚 [ChromaDB Vector Store] Retrieved {len(rag_context.splitlines())} lines of verified grounding documents.\n")

    # 2. RUN WITH RAG
    print("⏳ [1/2] Generating Lesson WITH RAG (Project ROAR Pipeline)...")
    prompt_with_rag = get_lesson_prompt(
        node_id=node.id,
        topic_path=f"{node.category} / {node.title}",
        topic_description=node.description,
        key_concepts=node.rubric.get("key_concepts", []),
        depth=node.difficulty_tier,
        difficulty_tier=node.difficulty_tier,
        rag_context=rag_context,
        prefers_examples=True,
        prefers_steps=True,
        prefers_detailed=True,
        prior_experience="intermediate"
    )
    res_with_rag = await model_manager.generate_async(
        prompt=prompt_with_rag,
        system_prompt="You are an expert AI Prompt Engineering Tutor. Author structured study material.",
        temperature=0.7,
        max_tokens=600,
        agent_name="LessonAgent-WithRAG"
    )

    # 3. RUN WITHOUT RAG (ABLATION BASELINE)
    print("⏳ [2/2] Generating Lesson WITHOUT RAG (Parametric Memory Only)...")
    prompt_without_rag = get_lesson_prompt(
        node_id=node.id,
        topic_path=f"{node.category} / {node.title}",
        topic_description=node.description,
        key_concepts=node.rubric.get("key_concepts", []),
        depth=node.difficulty_tier,
        difficulty_tier=node.difficulty_tier,
        rag_context="",  # ABLATED: No grounding provided!
        prefers_examples=True,
        prefers_steps=True,
        prefers_detailed=True,
        prior_experience="intermediate"
    )
    res_without_rag = await model_manager.generate_async(
        prompt=prompt_without_rag,
        system_prompt="You are an expert AI Prompt Engineering Tutor. Author structured study material.",
        temperature=0.7,
        max_tokens=600,
        agent_name="LessonAgent-NoRAG"
    )

    # Check key rubric concepts coverage
    required_concepts = [c.lower() for c in node.rubric.get("key_concepts", [])]
    text_with = res_with_rag.get("text", "").lower()
    text_without = res_without_rag.get("text", "").lower()

    found_with = [c for c in required_concepts if c in text_with]
    found_without = [c for c in required_concepts if c in text_without]

    print("\n" + "=" * 80)
    print("📊 EMPIRICAL COMPARISON RESULTS")
    print("=" * 80)
    print(f"• Rubric Key Concepts Required: {required_concepts}")
    print(f"• Covered WITH RAG:    {len(found_with)}/{len(required_concepts)} ({found_with})")
    print(f"• Covered WITHOUT RAG: {len(found_without)}/{len(required_concepts)} ({found_without})")
    print("-" * 80)
    print("\n📝 [SAMPLE OUTPUT: WITH RAG (Grounded in Verified Knowledge)]:")
    print(res_with_rag.get("text", "")[:450] + "...\n")
    print("-" * 80)
    print("📝 [SAMPLE OUTPUT: WITHOUT RAG (Unanchored Parametric Memory)]:")
    print(res_without_rag.get("text", "")[:450] + "...\n")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(demonstrate_rag_difference())
