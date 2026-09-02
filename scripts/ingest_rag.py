#!/usr/bin/env python3
# scripts/ingest_rag.py
"""
RAG Ingestion Script.
Loads prompt engineering QA samples and documentation into ChromaDB vector database.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from agents.rag_agent import rag_agent
from core.curriculum import curriculum_graph

OUTPUT_JSON_SOURCES = [
    root_dir / "data" / "rag_docs" / "output.json",
    Path("/tmp/roar-prompt-tutor/output.json")
]


def run_ingestion():
    print("[RAG Ingestion] Starting ingestion pipeline...")
    
    # 1. Ingest Curriculum Node definitions
    print(f"[RAG Ingestion] Ingesting {len(curriculum_graph.nodes)} curriculum ontology nodes...")
    for node in curriculum_graph.nodes:
        doc_id = f"ontology_{node.id}"
        content = (
            f"Topic: {node.path}\n"
            f"Category: {node.category}\n"
            f"Difficulty Tier: {node.difficulty_tier} (Weight: {node.weight})\n"
            f"Description: {node.description}\n"
            f"Key Concepts: {', '.join(node.rubric.get('key_concepts', []))}"
        )
        rag_agent.ingest_text_chunk(
            doc_id=doc_id,
            text=content,
            metadata={"type": "curriculum_node", "node_id": node.id, "tier": node.difficulty_tier}
        )

    # 2. Ingest output.json dataset if present
    found_dataset = False
    for src in OUTPUT_JSON_SOURCES:
        if src.exists():
            print(f"[RAG Ingestion] Found QA dataset at {src}, loading items...")
            with open(src, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                count = 0
                for i, item in enumerate(data):
                    ans = item.get("ANSWER", "").strip()
                    if not ans:
                        continue
                    topic = item.get("TOPIC", "")
                    sub1 = item.get("SUBTOPIC", "")
                    sub2 = item.get("SUBTOPIC 2", "")
                    diff = item.get("Difficality Level", "")
                    atype = item.get("Answer Type", "")
                    
                    path = " / ".join([x for x in (topic, sub1, sub2) if x])
                    text = f"Topic: {path}\nType: {atype} (Difficulty: {diff})\nExplanation & Example: {ans}"
                    
                    rag_agent.ingest_text_chunk(
                        doc_id=f"capstone_qa_{i}",
                        text=text,
                        metadata={"source": "capstone_qa", "topic": path}
                    )
                    count += 1
                print(f"[RAG Ingestion] Successfully ingested {count} QA knowledge chunks.")
                found_dataset = True
            break

    if not found_dataset:
        print("[RAG Ingestion] Note: capstone output.json not found locally; ingested ontology nodes only.")

    print("[RAG Ingestion] Ingestion complete. ChromaDB ready.")


if __name__ == "__main__":
    run_ingestion()
