# agents/rag_agent.py
"""
RAG Retrieval Agent.
Interfaces with ChromaDB vector store to retrieve semantic context
chunks for specific prompt engineering topics, concepts, and challenges.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

CHROMA_DIR = Path(__file__).resolve().parent.parent / "data" / "db" / "chroma"
RAG_DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "rag_docs"


class RAGAgent:
    def __init__(self, chroma_path: Optional[str] = None):
        self.chroma_path = chroma_path or os.getenv("CHROMA_PATH", str(CHROMA_DIR))
        self._client = None
        self._collection = None

    def _get_collection(self):
        if self._collection is None:
            try:
                import chromadb
                os.makedirs(self.chroma_path, exist_ok=True)
                self._client = chromadb.PersistentClient(path=self.chroma_path)
                self._collection = self._client.get_or_create_collection(name="prompt_tutor_kb")
            except Exception as e:
                print(f"[RAGAgent] ChromaDB initialization note: {e}")
                self._collection = None
        return self._collection

    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """
        Queries ChromaDB collection for the top_k relevant chunks.
        Returns a formatted string of context chunks.
        """
        coll = self._get_collection()
        if coll is None:
            return ""

        try:
            results = coll.query(query_texts=[query], n_results=top_k)
            documents = results.get("documents", [[]])[0]
            if not documents:
                return ""
            
            context_blocks = []
            for i, doc in enumerate(documents, 1):
                context_blocks.append(f"[{i}] {doc.strip()}")
            return "\n\n".join(context_blocks)
        except Exception as e:
            print(f"[RAGAgent] Retrieval error: {e}")
            return ""

    def ingest_text_chunk(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        coll = self._get_collection()
        if coll:
            coll.upsert(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata or {}]
            )


# Global singleton instance
rag_agent = RAGAgent()
