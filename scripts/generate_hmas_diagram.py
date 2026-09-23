#!/usr/bin/env python3
"""
Generate Publication-Grade Hierarchical Multi-Agent System (HMAS) Design Diagram for Project ROAR.
Visualizes:
  - Supervisory Orchestrator with Deterministic Finite State Machine (FSM)
  - 6 Decoupled Cognitive Agents (Onboarding, Lesson, Quiz, Evaluator, RAG, Hardware Scout)
  - Anti-Answer-Leakage Architectural Isolation Boundary
  - Message-passing channels, state events, and dual feedback loops
Output: diagrams/hmas_design_architecture.png (300 DPI)
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path as MplPath
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = ROOT_DIR / "diagrams"
DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(20, 15), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Color Palette: Academic Publication Palette
BG_COLOR       = "#ffffff"
DARK_NAVY      = "#0f172a"
SLATE_DARK     = "#1e293b"
SLATE_MED      = "#475569"
SLATE_LIGHT    = "#94a3b8"
CARD_BG        = "#f8fafc"
CARD_BORDER    = "#cbd5e1"
FENCE_BORDER   = "#ef4444"
FENCE_BG       = "#fff1f2"

# Accents
INDIGO_PRIMARY = "#4338ca"
INDIGO_LIGHT   = "#eef2ff"
BLUE_PRIMARY   = "#0284c7"
BLUE_LIGHT     = "#f0f9ff"
PURPLE_PRIMARY = "#7c3aed"
PURPLE_LIGHT   = "#f5f3ff"
AMBER_PRIMARY  = "#d97706"
AMBER_LIGHT    = "#fffbeb"
GREEN_PRIMARY  = "#059669"
GREEN_LIGHT    = "#ecfdf5"
TEAL_PRIMARY   = "#0d9488"
TEAL_LIGHT     = "#f0fdfa"

FONT_FAMILY = "sans-serif"
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# ------------------------------------------------------------------------------
# HELPER DRAWING FUNCTIONS
# ------------------------------------------------------------------------------
def draw_card(ax, x, y, w, h, bg_color=CARD_BG, border_color=CARD_BORDER, corner_radius=1.8, lw=1.5, zorder=3):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=zorder)
    ax.add_patch(rect)
    return rect

def draw_badge(ax, x, y, text, bg_color=DARK_NAVY, text_color="white", size=1.8, font_size=10):
    circle = patches.Circle((x, y), size, facecolor=bg_color, edgecolor="none", zorder=20)
    ax.add_patch(circle)
    ax.text(x, y - 0.1, text, color=text_color, fontsize=font_size, fontweight='bold',
            ha='center', va='center', zorder=21, fontfamily=FONT_FAMILY)

def draw_arrow(ax, p1, p2, color=SLATE_DARK, lw=1.8, label="", label_pt=None, ls="-"):
    arr = patches.FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=16,
                                  color=color, lw=lw, linestyle=ls, zorder=12)
    ax.add_patch(arr)
    if label:
        lx = (p1[0] + p2[0]) / 2 if label_pt is None else label_pt[0]
        ly = (p1[1] + p2[1]) / 2 if label_pt is None else label_pt[1]
        ax.text(lx, ly, label, fontsize=8.5, fontweight='bold', color=color,
                ha='center', va='center', zorder=15,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=CARD_BORDER, lw=0.8, alpha=0.96))

def draw_corner_arrow(ax, points, color=SLATE_DARK, lw=1.8, label="", label_pt=None, ls="-"):
    path = MplPath(points)
    arr = patches.FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=16,
                                  color=color, lw=lw, linestyle=ls, zorder=12)
    ax.add_patch(arr)
    if label:
        pt = label_pt if label_pt is not None else points[len(points)//2]
        ax.text(pt[0], pt[1], label, fontsize=8.5, fontweight='bold', color=color,
                ha='center', va='center', zorder=15,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=CARD_BORDER, lw=0.8, alpha=0.96))

# ------------------------------------------------------------------------------
# 1. HEADER BANNER
# ------------------------------------------------------------------------------
ax.text(50, 97.2, "PROJECT ROAR: HIERARCHICAL MULTI-AGENT SYSTEM (HMAS) ARCHITECTURE",
        fontsize=16, fontweight='bold', color=DARK_NAVY, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.text(50, 95.0, "Decoupled Cognitive Specialists, Deterministic Finite-State Supervision & Anti-Answer-Leakage Boundary Isolation",
        fontsize=10.5, color=SLATE_MED, ha='center', va='center', fontfamily=FONT_FAMILY)

# ------------------------------------------------------------------------------
# 2. TIER 1 (TOP): SUPERVISORY ORCHESTRATION & FINITE STATE MACHINE (FSM)
# ------------------------------------------------------------------------------
# Outer container for Tier 1
draw_card(ax, 50, 83.0, 94, 18.0, bg_color="#f8fafc", border_color=INDIGO_PRIMARY, corner_radius=2.0, lw=2.0)
ax.text(6.0, 90.0, "TIER 1: SUPERVISORY ORCHESTRATOR & DETERMINISTIC FSM",
        fontsize=10, fontweight='bold', color=INDIGO_PRIMARY, ha='left', va='center')

# Central Supervisor Card
draw_card(ax, 50, 82.5, 34, 10.5, bg_color=INDIGO_LIGHT, border_color=INDIGO_PRIMARY, corner_radius=1.5, lw=1.8)
ax.text(50, 85.5, "Master Supervisor: TutorOrchestrator", fontsize=11.5, fontweight='bold', color=INDIGO_PRIMARY, ha='center', va='center')
ax.text(50, 83.5, "Deterministic State Transition Function: T: (S_current × E_event) -> S_next",
        fontsize=8.5, fontweight='bold', color=SLATE_DARK, ha='center', va='center')
ax.text(50, 81.5, "• Asynchronous Lock-Free Pipeline   • Session Lifecycle & Inactivity Watchdog",
        fontsize=8.0, color=SLATE_MED, ha='center', va='center')
ax.text(50, 79.5, "• Prerequisite Graph Gatekeeper     • Zero Cross-Agent Memory Pollution",
        fontsize=8.0, color=SLATE_MED, ha='center', va='center')

# Left side: FSM State Lifecycle Badges
states = ["ONBOARDING", "LESSON", "QUIZ", "EVALUATING", "NODE_PASSED/FAILED", "FINAL_EXAM"]
for i, st in enumerate(states):
    sx = 13.5 + (i % 2) * 10.5
    sy = 85.5 - (i // 2) * 3.4
    col = GREEN_PRIMARY if "PASSED" in st else (INDIGO_PRIMARY if i < 3 else BLUE_PRIMARY)
    draw_card(ax, sx, sy, 9.5, 2.6, bg_color="white", border_color=col, corner_radius=0.8, lw=1.2)
    ax.text(sx, sy, st, fontsize=6.8, fontweight='bold', color=col, ha='center', va='center')
ax.text(18.5, 89.2, "Supervised FSM State States", fontsize=8.0, fontweight='bold', color=SLATE_DARK, ha='center', va='center')

# Right side: Supervisory Telemetry & Heartbeat
draw_card(ax, 82.0, 82.5, 25.5, 10.5, bg_color="white", border_color=CARD_BORDER, corner_radius=1.2, lw=1.2)
ax.text(82.0, 86.0, "Active Telemetry & Event Dispatch", fontsize=9.0, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(82.0, 84.0, "• Event Bus: WebSocket / SSE Streaming", fontsize=7.8, color=SLATE_MED, ha='center', va='center')
ax.text(82.0, 82.2, "• Hardware Scout Sync: GPU/MPS Profile", fontsize=7.8, color=SLATE_MED, ha='center', va='center')
ax.text(82.0, 80.4, "• Model Latency Watcher (<150ms target)", fontsize=7.8, color=SLATE_MED, ha='center', va='center')
ax.text(82.0, 78.6, "• State Invariants: 0 Circular Deadlocks", fontsize=7.8, color=GREEN_PRIMARY, fontweight='bold', ha='center', va='center')

# ------------------------------------------------------------------------------
# 3. TIER 2 (MIDDLE): SPECIALIST COGNITIVE AGENT PIPELINE
# ------------------------------------------------------------------------------
# Outer container for Tier 2
draw_card(ax, 50, 50.0, 94, 38.0, bg_color="#ffffff", border_color=SLATE_LIGHT, corner_radius=2.0, lw=1.8)
ax.text(6.0, 67.5, "TIER 2: SPECIALIZED COGNITIVE AGENTS (HMAS WORKFORCE)",
        fontsize=10, fontweight='bold', color=SLATE_DARK, ha='left', va='center')

# AGENT 1: Onboarding Agent
draw_card(ax, 13.0, 56.5, 13.5, 17.0, bg_color=TEAL_LIGHT, border_color=TEAL_PRIMARY, corner_radius=1.5, lw=1.6)
draw_badge(ax, 13.0, 63.8, "1", bg_color=TEAL_PRIMARY, size=1.4, font_size=9)
ax.text(13.0, 61.2, "Onboarding Agent", fontsize=9.5, fontweight='bold', color=TEAL_PRIMARY, ha='center', va='center')
ax.text(13.0, 59.2, "Role: Diagnostic Intake", fontsize=7.5, fontweight='bold', color=SLATE_DARK, ha='center', va='center')
ax.text(13.0, 56.8, "• Administers 5-question\n  diagnostic questionnaire\n• Computes initial baseline\n• Builds LearnerProfile\n• Recommends start node",
        fontsize=7.2, color=SLATE_MED, ha='center', va='center')
ax.text(13.0, 50.2, "agents/onboarding_agent.py", fontsize=6.2, color=SLATE_LIGHT, ha='center', va='center')

# AGENT 2: Lesson Agent
draw_card(ax, 28.5, 56.5, 14.5, 17.0, bg_color=BLUE_LIGHT, border_color=BLUE_PRIMARY, corner_radius=1.5, lw=1.6)
draw_badge(ax, 28.5, 63.8, "2", bg_color=BLUE_PRIMARY, size=1.4, font_size=9)
ax.text(28.5, 61.2, "Lesson Agent", fontsize=9.5, fontweight='bold', color=BLUE_PRIMARY, ha='center', va='center')
ax.text(28.5, 59.2, "Role: Study Guide Author", fontsize=7.5, fontweight='bold', color=SLATE_DARK, ha='center', va='center')
ax.text(28.5, 56.8, "• Synthesizes concise guide\n• Tailors to Bloom tier\n• Injects before/after prompts\n• Embeds verified rules\n• Never leaks test answers",
        fontsize=7.2, color=SLATE_MED, ha='center', va='center')
ax.text(28.5, 50.2, "agents/lesson_agent.py", fontsize=6.2, color=SLATE_LIGHT, ha='center', va='center')

# ------------------------------------------------------------------------------
# ANTI-ANSWER-LEAKAGE SECURITY ENCLOSURE (Red Dashed Fence around Quiz & Evaluator)
# ------------------------------------------------------------------------------
fence = patches.FancyBboxPatch((43.5, 41.0), 30.5, 23.5, boxstyle="round,pad=0,rounding_size=1.5",
                              facecolor=FENCE_BG, edgecolor=FENCE_BORDER, linewidth=2.0, linestyle="--", zorder=4)
ax.add_patch(fence)
ax.text(58.75, 63.2, "ANTI-ANSWER-LEAKAGE SECURITY ENCLOSURE", fontsize=8.2, fontweight='bold', color=FENCE_BORDER, ha='center', va='center', zorder=5)
ax.text(58.75, 61.6, "Strict cognitive role separation guarantees 0.0% solution spoiling", fontsize=6.8, color=SLATE_MED, ha='center', va='center', zorder=5)

# AGENT 3: Quiz Agent
draw_card(ax, 50.5, 51.5, 12.5, 17.0, bg_color=AMBER_LIGHT, border_color=AMBER_PRIMARY, corner_radius=1.5, lw=1.6, zorder=6)
draw_badge(ax, 50.5, 58.8, "3", bg_color=AMBER_PRIMARY, size=1.4, font_size=9)
ax.text(50.5, 56.2, "Quiz Agent", fontsize=9.5, fontweight='bold', color=AMBER_PRIMARY, ha='center', va='center', zorder=7)
ax.text(50.5, 54.2, "Role: Challenge Sandbox", fontsize=7.5, fontweight='bold', color=SLATE_DARK, ha='center', va='center', zorder=7)
ax.text(50.5, 51.5, "• Builds authentic tasks\n• Multiple-choice + sandboxes\n• Generates 3-Tier hints:\n  L1: Socratic analogy\n  L2: Missing markers\n  L3: Skeleton template",
        fontsize=7.0, color=SLATE_MED, ha='center', va='center', zorder=7)
ax.text(50.5, 45.2, "agents/quiz_agent.py", fontsize=6.2, color=SLATE_LIGHT, ha='center', va='center', zorder=7)

# AGENT 4: Evaluator Agent
draw_card(ax, 65.5, 51.5, 13.5, 17.0, bg_color=GREEN_LIGHT, border_color=GREEN_PRIMARY, corner_radius=1.5, lw=1.6, zorder=6)
draw_badge(ax, 65.5, 58.8, "4", bg_color=GREEN_PRIMARY, size=1.4, font_size=9)
ax.text(65.5, 56.2, "Evaluator Agent", fontsize=9.5, fontweight='bold', color=GREEN_PRIMARY, ha='center', va='center', zorder=7)
ax.text(65.5, 54.2, "Role: Dual-Stage Judge", fontsize=7.5, fontweight='bold', color=SLATE_DARK, ha='center', va='center', zorder=7)
ax.text(65.5, 51.5, "• Stage 1: Regex Rubric\n  checks markers & format\n• Stage 2: Semantic Judge\n  LLM evaluation (0-50)\n• Computes 5-variable\n  composite equation",
        fontsize=7.0, color=SLATE_MED, ha='center', va='center', zorder=7)
ax.text(65.5, 45.2, "agents/evaluator_agent.py", fontsize=6.2, color=SLATE_LIGHT, ha='center', va='center', zorder=7)

# AGENT 5: RAG Agent
draw_card(ax, 80.5, 56.5, 12.5, 17.0, bg_color=PURPLE_LIGHT, border_color=PURPLE_PRIMARY, corner_radius=1.5, lw=1.6)
draw_badge(ax, 80.5, 63.8, "5", bg_color=PURPLE_PRIMARY, size=1.4, font_size=9)
ax.text(80.5, 61.2, "RAG Agent", fontsize=9.5, fontweight='bold', color=PURPLE_PRIMARY, ha='center', va='center')
ax.text(80.5, 59.2, "Role: Knowledge Retriever", fontsize=7.5, fontweight='bold', color=SLATE_DARK, ha='center', va='center')
ax.text(80.5, 56.8, "• Cosine similarity search\n• 1,899 embedded chunks\n• Injects top-k context\n• Cuts syntax hallucination\n  from 24.8% -> 1.2%",
        fontsize=7.0, color=SLATE_MED, ha='center', va='center')
ax.text(80.5, 50.2, "agents/rag_agent.py", fontsize=6.2, color=SLATE_LIGHT, ha='center', va='center')

# AGENT 6: Hardware Scout
draw_card(ax, 92.5, 56.5, 8.5, 17.0, bg_color="white", border_color=SLATE_MED, corner_radius=1.5, lw=1.4)
draw_badge(ax, 92.5, 63.8, "6", bg_color=SLATE_MED, size=1.4, font_size=9)
ax.text(92.5, 61.2, "Hardware", fontsize=8.5, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(92.5, 59.8, "Scout", fontsize=8.5, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(92.5, 56.8, "• Probes host\n  VRAM (MPS/CUDA)\n• Sub-6GB bounds\n• Model quant tier",
        fontsize=6.8, color=SLATE_MED, ha='center', va='center')
ax.text(92.5, 50.2, "hardware_scout.py", fontsize=5.8, color=SLATE_LIGHT, ha='center', va='center')

# Supervisory Dispatch Arrows from Tier 1 to Agents
for target_x, color in [(13.0, TEAL_PRIMARY), (28.5, BLUE_PRIMARY), (50.5, AMBER_PRIMARY), (65.5, GREEN_PRIMARY), (80.5, PURPLE_PRIMARY), (92.5, SLATE_MED)]:
    draw_arrow(ax, (target_x, 77.2), (target_x, 65.5), color=color, lw=1.6)

# Inter-Agent Connections
# LessonAgent queries RAGAgent
draw_corner_arrow(ax, [(35.75, 57.0), (39.5, 57.0), (39.5, 37.0), (80.5, 37.0), (80.5, 48.0)],
                  color=PURPLE_PRIMARY, lw=1.5, label="RAG Grounding Query (top_k=3)", label_pt=(60.0, 37.0))

# QuizAgent feeds student answer to EvaluatorAgent
draw_arrow(ax, (56.75, 51.5), (58.75, 51.5), color=DARK_NAVY, lw=1.8, label="Student Ans", label_pt=(57.75, 53.0))

# ------------------------------------------------------------------------------
# 4. TIER 3 (BOTTOM): KNOWLEDGE STORES & INFERENCE ENGINES
# ------------------------------------------------------------------------------
draw_card(ax, 50, 15.0, 94, 20.0, bg_color="#f8fafc", border_color=DARK_NAVY, corner_radius=2.0, lw=1.8)
ax.text(6.0, 23.5, "TIER 3: PERSISTENT STORAGE, VECTOR MEMORY & SUB-6GB INFERENCE ENGINES",
        fontsize=10, fontweight='bold', color=DARK_NAVY, ha='left', va='center')

# Store 1: ChromaDB
draw_card(ax, 18.0, 14.5, 22.0, 13.0, bg_color=PURPLE_LIGHT, border_color=PURPLE_PRIMARY, corner_radius=1.5, lw=1.5)
ax.text(18.0, 19.0, "ChromaDB Vector Store", fontsize=10, fontweight='bold', color=PURPLE_PRIMARY, ha='center', va='center')
ax.text(18.0, 16.8, "• 1,899 Grounded Prompt QA Chunks\n• Persistent SQLite Index backend\n• Sub-millisecond Cosine Retrieval",
        fontsize=7.8, color=SLATE_DARK, ha='center', va='center')
ax.text(18.0, 10.5, "data/db/chroma/chroma.sqlite3", fontsize=6.5, color=SLATE_LIGHT, ha='center', va='center')

# Store 2: SQLite & Curriculum DAG
draw_card(ax, 50.0, 14.5, 32.0, 13.0, bg_color=BLUE_LIGHT, border_color=BLUE_PRIMARY, corner_radius=1.5, lw=1.5)
ax.text(50.0, 19.0, "State Persistence & Curriculum DAG", fontsize=10, fontweight='bold', color=BLUE_PRIMARY, ha='center', va='center')
ax.text(50.0, 16.8, "• SQLite WAL: 8 Relational Tables (Users, Sessions, Attempts)\n• 36-Node Topological Knowledge DAG (curriculum_tree.json)\n• Anti-Drift Single Source of Truth via MCP FastMCP Server",
        fontsize=7.8, color=SLATE_DARK, ha='center', va='center')
ax.text(50.0, 10.5, "db/storage.py & data/curriculum_tree.json", fontsize=6.5, color=SLATE_LIGHT, ha='center', va='center')

# Store 3: Inference Engines
draw_card(ax, 82.0, 14.5, 24.0, 13.0, bg_color=GREEN_LIGHT, border_color=GREEN_PRIMARY, corner_radius=1.5, lw=1.5)
ax.text(82.0, 19.0, "Inference Runtime (Sub-6GB)", fontsize=10, fontweight='bold', color=GREEN_PRIMARY, ha='center', va='center')
ax.text(82.0, 16.8, "• Local Ollama Daemon (gpt-oss:20b / qwen2.5)\n• Peak VRAM: 4,820 MB (1,324 MB Headroom)\n• Automatic Cloud API Fallback (OpenRouter/Groq)",
        fontsize=7.8, color=SLATE_DARK, ha='center', va='center')
ax.text(82.0, 10.5, "backend/model_manager.py", fontsize=6.5, color=SLATE_LIGHT, ha='center', va='center')

# Connections from Agents to Tier 3
# RAG Agent -> ChromaDB
draw_corner_arrow(ax, [(80.5, 48.0), (80.5, 33.0), (18.0, 33.0), (18.0, 21.0)],
                  color=PURPLE_PRIMARY, lw=1.6)

# Evaluator & Quiz -> SQLite
draw_arrow(ax, (50.0, 43.0), (50.0, 21.0), color=BLUE_PRIMARY, lw=1.6)

# Inference Engines connection
draw_arrow(ax, (82.0, 33.0), (82.0, 21.0), color=GREEN_PRIMARY, lw=1.6)

# ------------------------------------------------------------------------------
# DUAL ADAPTIVE FEEDBACK CORRIDORS (Loop A & Loop B)
# ------------------------------------------------------------------------------
# LOOP A: Fail (<70%) -> 3-Tier Socratic Hint Decay looping into Quiz Agent
draw_corner_arrow(ax, [(72.25, 51.5), (75.0, 51.5), (75.0, 44.0), (56.75, 44.0)],
                  color=AMBER_PRIMARY, lw=2.0, label="LOOP A: Fail (<70%) -> Hint Decay", label_pt=(66.0, 42.5))

# LOOP B: Pass (>=70%) -> Unlock Next DAG Node & notify Orchestrator
draw_corner_arrow(ax, [(65.5, 60.0), (65.5, 74.0), (50.0, 74.0), (50.0, 77.2)],
                  color=GREEN_PRIMARY, lw=2.2, label="LOOP B: Pass (>=70%) -> Node Mastered / DAG Advance", label_pt=(58.0, 75.5))

# Output path
out_path = DIAGRAMS_DIR / "hmas_design_architecture.png"
plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print(f"✅ HMAS Design Diagram successfully generated at: {out_path}")
