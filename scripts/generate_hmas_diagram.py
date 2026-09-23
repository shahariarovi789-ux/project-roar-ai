#!/usr/bin/env python3
"""
Generate Print-Optimized, Publication-Grade HMAS Design Diagram for Project ROAR.
Optimized for 8.5x11 / A4 printed technical reports:
  - Large, high-contrast typography (10pt to 18pt) legible when scaled to printed page
  - Compact, snug card padding with thick 2.0pt-2.5pt borders
  - High-contrast color hierarchy (#0f172a text on clean backgrounds)
  - Bold, prominent Anti-Answer-Leakage security barrier
  - Prominent dual adaptive feedback corridors
Output: diagrams/hmas_design_architecture.png (300 DPI)
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path as MplPath

ROOT_DIR = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = ROOT_DIR / "diagrams"
DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

# 16:11 Aspect ratio - ideal for landscape print on Letter / A4
fig, ax = plt.subplots(figsize=(16, 11.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# High-Contrast Academic Print Palette
BG_COLOR       = "#ffffff"
DARK_NAVY      = "#0f172a"  # Primary high-contrast text
SLATE_DARK     = "#1e293b"  # Secondary dark text
SLATE_MED      = "#475569"  # Explanatory text
CARD_BG        = "#f8fafc"
CARD_BORDER    = "#94a3b8"

# Accents with deep text counterparts
INDIGO_PRIMARY = "#3730a3"
INDIGO_BG      = "#eef2ff"
BLUE_PRIMARY   = "#0369a1"
BLUE_BG        = "#f0f9ff"
AMBER_PRIMARY  = "#b45309"
AMBER_BG       = "#fffbeb"
GREEN_PRIMARY  = "#047857"
GREEN_BG       = "#ecfdf5"
PURPLE_PRIMARY = "#6d28d9"
PURPLE_BG      = "#f5f3ff"
TEAL_PRIMARY   = "#0f766e"
TEAL_BG        = "#f0fdfa"
FENCE_BORDER   = "#b91c1c"
FENCE_BG       = "#fef2f2"

FONT_FAMILY = "sans-serif"
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

def draw_card(ax, x, y, w, h, bg_color=CARD_BG, border_color=CARD_BORDER, corner_radius=1.4, lw=1.8, zorder=3):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=zorder)
    ax.add_patch(rect)
    return rect

def draw_badge(ax, x, y, text, bg_color=DARK_NAVY, text_color="white", size=1.7, font_size=10.5, zorder=20):
    circle = patches.Circle((x, y), size, facecolor=bg_color, edgecolor="none", zorder=zorder)
    ax.add_patch(circle)
    ax.text(x, y - 0.1, text, color=text_color, fontsize=font_size, fontweight='bold',
            ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)

def draw_arrow(ax, p1, p2, color=SLATE_DARK, lw=2.0, label="", label_pt=None, ls="-"):
    arr = patches.FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=18,
                                  color=color, lw=lw, linestyle=ls, zorder=12)
    ax.add_patch(arr)
    if label:
        lx = (p1[0] + p2[0]) / 2 if label_pt is None else label_pt[0]
        ly = (p1[1] + p2[1]) / 2 if label_pt is None else label_pt[1]
        ax.text(lx, ly, label, fontsize=9.0, fontweight='bold', color=color,
                ha='center', va='center', zorder=15,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=CARD_BORDER, lw=1.0, alpha=0.98))

def draw_corner_arrow(ax, points, color=SLATE_DARK, lw=2.0, label="", label_pt=None, ls="-"):
    path = MplPath(points)
    arr = patches.FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=18,
                                  color=color, lw=lw, linestyle=ls, zorder=12)
    ax.add_patch(arr)
    if label:
        pt = label_pt if label_pt is not None else points[len(points)//2]
        ax.text(pt[0], pt[1], label, fontsize=9.2, fontweight='bold', color=color,
                ha='center', va='center', zorder=15,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=CARD_BORDER, lw=1.0, alpha=0.98))

# ------------------------------------------------------------------------------
# 1. HEADER (High-Contrast, Large Font)
# ------------------------------------------------------------------------------
ax.text(50, 97.2, "PROJECT ROAR: HIERARCHICAL MULTI-AGENT SYSTEM (HMAS)",
        fontsize=17, fontweight='bold', color=DARK_NAVY, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.text(50, 94.7, "Decoupled Cognitive Specialists, Deterministic FSM Supervision & Anti-Answer-Leakage Boundary Isolation",
        fontsize=10.5, fontweight='bold', color=SLATE_MED, ha='center', va='center', fontfamily=FONT_FAMILY)

# ------------------------------------------------------------------------------
# 2. TIER 1 (TOP): SUPERVISORY CONTROL & FINITE STATE MACHINE (FSM)
# ------------------------------------------------------------------------------
draw_card(ax, 50, 81.5, 96, 21.0, bg_color="#ffffff", border_color=INDIGO_PRIMARY, corner_radius=1.8, lw=2.2)
ax.text(5.5, 90.0, "TIER 1: SUPERVISORY ORCHESTRATOR & DETERMINISTIC FSM",
        fontsize=11.5, fontweight='bold', color=INDIGO_PRIMARY, ha='left', va='center')

# Left Box: Supervised FSM States
draw_card(ax, 19.5, 80.5, 25.0, 15.5, bg_color=CARD_BG, border_color=CARD_BORDER, corner_radius=1.2, lw=1.4)
ax.text(19.5, 86.2, "Supervised FSM States", fontsize=10.0, fontweight='bold', color=DARK_NAVY, ha='center', va='center')

fsm_states = [
    ("ONBOARDING", TEAL_PRIMARY), ("LESSON", BLUE_PRIMARY),
    ("QUIZ", AMBER_PRIMARY), ("EVALUATING", GREEN_PRIMARY),
    ("PASS / FAIL", INDIGO_PRIMARY), ("FINAL EXAM", PURPLE_PRIMARY)
]
for idx, (st, col) in enumerate(fsm_states):
    sx = 13.5 + (idx % 2) * 12.0
    sy = 83.2 - (idx // 2) * 3.6
    draw_card(ax, sx, sy, 10.8, 2.8, bg_color="white", border_color=col, corner_radius=0.7, lw=1.4)
    ax.text(sx, sy, st, fontsize=8.2, fontweight='bold', color=col, ha='center', va='center')

# Center Box: Master Supervisor
draw_card(ax, 52.0, 80.5, 36.0, 15.5, bg_color=INDIGO_BG, border_color=INDIGO_PRIMARY, corner_radius=1.4, lw=2.0)
ax.text(52.0, 85.8, "Master Supervisor: TutorOrchestrator", fontsize=12.0, fontweight='bold', color=INDIGO_PRIMARY, ha='center', va='center')
ax.text(52.0, 83.5, "T: (S_current × E_event) -> S_next", fontsize=10.5, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(52.0, 80.8, "• Asynchronous Lock-Free Transition Engine", fontsize=9.2, color=SLATE_DARK, ha='center', va='center')
ax.text(52.0, 78.8, "• Enforces Topological Prerequisite Graph Gating", fontsize=9.2, color=SLATE_DARK, ha='center', va='center')
ax.text(52.0, 76.8, "• Zero Cross-Agent Memory Contamination", fontsize=9.2, color=GREEN_PRIMARY, fontweight='bold', ha='center', va='center')
ax.text(52.0, 74.2, "agents/orchestrator.py", fontsize=7.5, color=SLATE_MED, ha='center', va='center')

# Right Box: Supervisory Telemetry
draw_card(ax, 84.5, 80.5, 23.0, 15.5, bg_color=CARD_BG, border_color=CARD_BORDER, corner_radius=1.2, lw=1.4)
ax.text(84.5, 86.2, "Runtime Telemetry", fontsize=10.0, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(84.5, 83.5, "• WebSocket Event Bus", fontsize=8.8, color=SLATE_DARK, ha='center', va='center')
ax.text(84.5, 81.2, "• Hardware Scout Sync", fontsize=8.8, color=SLATE_DARK, ha='center', va='center')
ax.text(84.5, 78.9, "• Latency Profiler (<150ms)", fontsize=8.8, color=SLATE_DARK, ha='center', va='center')
ax.text(84.5, 76.2, "Deadlocks: 0 (Verified)", fontsize=8.8, fontweight='bold', color=GREEN_PRIMARY, ha='center', va='center')

# ------------------------------------------------------------------------------
# 3. TIER 2 (MIDDLE): SPECIALIST COGNITIVE AGENT PIPELINE
# ------------------------------------------------------------------------------
draw_card(ax, 50, 48.0, 96, 40.0, bg_color="#ffffff", border_color=SLATE_DARK, corner_radius=1.8, lw=2.0)
ax.text(5.5, 66.2, "TIER 2: SPECIALIZED COGNITIVE AGENTS (DECOUPLED WORKFORCE)",
        fontsize=11.5, fontweight='bold', color=DARK_NAVY, ha='left', va='center')

card_y = 50.0
card_h = 28.0

# AGENT 1: Onboarding Agent
draw_card(ax, 11.0, card_y, 14.0, card_h, bg_color=TEAL_BG, border_color=TEAL_PRIMARY, corner_radius=1.4, lw=1.8)
draw_badge(ax, 11.0, card_y + 11.5, "1", bg_color=TEAL_PRIMARY)
ax.text(11.0, card_y + 8.8, "Onboarding Agent", fontsize=11.0, fontweight='bold', color=TEAL_PRIMARY, ha='center', va='center')
ax.text(11.0, card_y + 6.6, "Role: Diagnostic Intake", fontsize=9.2, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(11.0, card_y + 4.8, "• Conducts 5-item\n  diagnostic questionnaire\n• Evaluates skill level\n• Builds LearnerProfile\n• Recommends start node",
        fontsize=8.5, color=SLATE_DARK, ha='center', va='top')
ax.text(11.0, card_y - 12.0, "onboarding_agent.py", fontsize=7.5, color=SLATE_MED, ha='center', va='center')

# AGENT 2: Lesson Agent
draw_card(ax, 26.5, card_y, 14.5, card_h, bg_color=BLUE_BG, border_color=BLUE_PRIMARY, corner_radius=1.4, lw=1.8)
draw_badge(ax, 26.5, card_y + 11.5, "2", bg_color=BLUE_PRIMARY)
ax.text(26.5, card_y + 8.8, "Lesson Agent", fontsize=11.0, fontweight='bold', color=BLUE_PRIMARY, ha='center', va='center')
ax.text(26.5, card_y + 6.6, "Role: Study Guide Author", fontsize=9.2, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(26.5, card_y + 4.8, "• Synthesizes study notes\n• Tailors to Bloom tier\n• Injects before/after\n  concrete prompt models\n• ChromaDB RAG grounded\n• Never leaks test answers",
        fontsize=8.5, color=SLATE_DARK, ha='center', va='top')
ax.text(26.5, card_y - 12.0, "lesson_agent.py", fontsize=7.5, color=SLATE_MED, ha='center', va='center')

# ------------------------------------------------------------------------------
# ANTI-ANSWER-LEAKAGE SECURITY ENCLOSURE
# ------------------------------------------------------------------------------
fence = patches.FancyBboxPatch((42.5, card_y - 14.5), 30.5, 30.0, boxstyle="round,pad=0,rounding_size=1.4",
                              facecolor=FENCE_BG, edgecolor=FENCE_BORDER, linewidth=2.4, linestyle="--", zorder=4)
ax.add_patch(fence)
ax.text(57.75, card_y + 13.5, "ANTI-ANSWER-LEAKAGE SECURITY ENCLOSURE", fontsize=9.2, fontweight='bold', color=FENCE_BORDER, ha='center', va='center', zorder=5)
ax.text(57.75, card_y + 11.5, "Strict cognitive role separation guarantees 0.0% solution spoiling", fontsize=7.8, color=SLATE_DARK, ha='center', va='center', zorder=5)

# AGENT 3: Quiz Agent (Inside Fence)
draw_card(ax, 48.5, card_y - 1.5, 12.0, 23.0, bg_color=AMBER_BG, border_color=AMBER_PRIMARY, corner_radius=1.2, lw=1.8, zorder=6)
draw_badge(ax, 48.5, card_y + 8.0, "3", bg_color=AMBER_PRIMARY)
ax.text(48.5, card_y + 5.6, "Quiz Agent", fontsize=11.0, fontweight='bold', color=AMBER_PRIMARY, ha='center', va='center', zorder=7)
ax.text(48.5, card_y + 3.6, "Role: Challenge Sandbox", fontsize=8.8, fontweight='bold', color=DARK_NAVY, ha='center', va='center', zorder=7)
ax.text(48.5, card_y + 2.0, "• Builds authentic tasks\n• Applied prompt sandbox\n• 3-Tier Socratic hints:\n  L1: Socratic analogy\n  L2: Missing rubric\n  L3: Partial skeleton",
        fontsize=8.0, color=SLATE_DARK, ha='center', va='top', zorder=7)
ax.text(48.5, card_y - 11.2, "quiz_agent.py", fontsize=7.5, color=SLATE_MED, ha='center', va='center', zorder=7)

# AGENT 4: Evaluator Agent (Inside Fence)
draw_card(ax, 65.5, card_y - 1.5, 12.8, 23.0, bg_color=GREEN_BG, border_color=GREEN_PRIMARY, corner_radius=1.2, lw=1.8, zorder=6)
draw_badge(ax, 65.5, card_y + 8.0, "4", bg_color=GREEN_PRIMARY)
ax.text(65.5, card_y + 5.6, "Evaluator Agent", fontsize=11.0, fontweight='bold', color=GREEN_PRIMARY, ha='center', va='center', zorder=7)
ax.text(65.5, card_y + 3.6, "Role: Dual-Stage Judge", fontsize=8.8, fontweight='bold', color=DARK_NAVY, ha='center', va='center', zorder=7)
ax.text(65.5, card_y + 2.0, "• Stage 1: Regex Rubric\n  checks markers & format\n• Stage 2: Semantic Judge\n  LLM-as-a-judge (0-50)\n• 5-Variable composite\n  calibrated grading",
        fontsize=8.0, color=SLATE_DARK, ha='center', va='top', zorder=7)
ax.text(65.5, card_y - 11.2, "evaluator_agent.py", fontsize=7.5, color=SLATE_MED, ha='center', va='center', zorder=7)

# AGENT 5: RAG Agent
draw_card(ax, 79.5, card_y, 13.5, card_h, bg_color=PURPLE_BG, border_color=PURPLE_PRIMARY, corner_radius=1.4, lw=1.8)
draw_badge(ax, 79.5, card_y + 11.5, "5", bg_color=PURPLE_PRIMARY)
ax.text(79.5, card_y + 8.8, "RAG Agent", fontsize=11.0, fontweight='bold', color=PURPLE_PRIMARY, ha='center', va='center')
ax.text(79.5, card_y + 6.6, "Role: Vector Retriever", fontsize=9.2, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(79.5, card_y + 4.8, "• ChromaDB cosine search\n• 1,899 technical chunks\n• Injects top-k grounding\n• Cuts syntax hallucination\n  from 24.8% -> 1.2%\n• Zero parametric drift",
        fontsize=8.5, color=SLATE_DARK, ha='center', va='top')
ax.text(79.5, card_y - 12.0, "rag_agent.py", fontsize=7.5, color=SLATE_MED, ha='center', va='center')

# AGENT 6: Hardware Scout
draw_card(ax, 92.5, card_y, 9.5, card_h, bg_color=CARD_BG, border_color=SLATE_DARK, corner_radius=1.4, lw=1.8)
draw_badge(ax, 92.5, card_y + 11.5, "6", bg_color=SLATE_DARK)
ax.text(92.5, card_y + 8.8, "Hardware Scout", fontsize=10.0, fontweight='bold', color=DARK_NAVY, ha='center', va='center')
ax.text(92.5, card_y + 6.6, "Role: Host Profiler", fontsize=8.8, fontweight='bold', color=SLATE_MED, ha='center', va='center')
ax.text(92.5, card_y + 4.8, "• Probes host hardware\n  VRAM (MPS/CUDA)\n• Sub-6GB limit\n• Selects model tier",
        fontsize=8.2, color=SLATE_DARK, ha='center', va='top')
ax.text(92.5, card_y - 12.0, "hardware_scout.py", fontsize=7.5, color=SLATE_MED, ha='center', va='center')

# Dispatch Arrows from Tier 1 Orchestrator to Tier 2 Agents
for tx, col in [(11.0, TEAL_PRIMARY), (26.5, BLUE_PRIMARY), (48.5, AMBER_PRIMARY), (65.5, GREEN_PRIMARY), (79.5, PURPLE_PRIMARY), (92.5, SLATE_DARK)]:
    draw_arrow(ax, (tx, 71.0), (tx, card_y + card_h/2), color=col, lw=1.8)

# Student Answer submission arrow
draw_arrow(ax, (54.5, card_y - 1.5), (59.1, card_y - 1.5), color=DARK_NAVY, lw=2.2, label="Student Ans", label_pt=(56.8, card_y + 0.6))

# Lesson Agent queries RAG Agent (Clean path below cards, label positioned to avoid vertical SQLite line)
draw_corner_arrow(ax, [(33.75, card_y - 9.0), (37.0, card_y - 9.0), (37.0, 31.5), (79.5, 31.5), (79.5, card_y - card_h/2)],
                  color=PURPLE_PRIMARY, lw=1.8, label="RAG Grounding Query (top_k=3)", label_pt=(67.0, 31.5))

# ------------------------------------------------------------------------------
# 4. TIER 3 (BOTTOM): KNOWLEDGE STORES & INFERENCE ENGINES
# ------------------------------------------------------------------------------
draw_card(ax, 50, 13.5, 96, 20.0, bg_color="#ffffff", border_color=DARK_NAVY, corner_radius=1.8, lw=2.2)
ax.text(5.5, 21.8, "TIER 3: PERSISTENT STORAGE, VECTOR MEMORY & SUB-6GB INFERENCE ENGINES",
        fontsize=11.5, fontweight='bold', color=DARK_NAVY, ha='left', va='center')

# Store 1: ChromaDB
draw_card(ax, 19.0, 12.0, 24.0, 14.5, bg_color=PURPLE_BG, border_color=PURPLE_PRIMARY, corner_radius=1.2, lw=1.8)
ax.text(19.0, 16.8, "ChromaDB Vector Store", fontsize=11.0, fontweight='bold', color=PURPLE_PRIMARY, ha='center', va='center')
ax.text(19.0, 14.0, "• 1,899 Grounded QA Chunks\n• Sub-millisecond Cosine Retrieval\n• Domain Verification Anchor",
        fontsize=8.8, color=SLATE_DARK, ha='center', va='center')
ax.text(19.0, 7.0, "data/db/chroma/chroma.sqlite3", fontsize=7.5, color=SLATE_MED, ha='center', va='center')

# Store 2: SQLite & Curriculum DAG
draw_card(ax, 51.0, 12.0, 33.0, 14.5, bg_color=BLUE_BG, border_color=BLUE_PRIMARY, corner_radius=1.2, lw=1.8)
ax.text(51.0, 16.8, "SQLite Database & Curriculum DAG", fontsize=11.0, fontweight='bold', color=BLUE_PRIMARY, ha='center', va='center')
ax.text(51.0, 14.0, "• SQLite WAL: 8 Relational Tables (Users, Sessions, Attempts)\n• 36-Node Topological Knowledge DAG (curriculum_tree.json)\n• Single Source of Truth via FastMCP Server (Zero Drift)",
        fontsize=8.8, color=SLATE_DARK, ha='center', va='center')
ax.text(51.0, 7.0, "db/storage.py & data/curriculum_tree.json", fontsize=7.5, color=SLATE_MED, ha='center', va='center')

# Store 3: Inference Engines
draw_card(ax, 83.5, 12.0, 25.0, 14.5, bg_color=GREEN_BG, border_color=GREEN_PRIMARY, corner_radius=1.2, lw=1.8)
ax.text(83.5, 16.8, "Inference Runtime (Sub-6GB)", fontsize=11.0, fontweight='bold', color=GREEN_PRIMARY, ha='center', va='center')
ax.text(83.5, 14.0, "• Local Ollama: gpt-oss:20b / qwen2.5\n• Peak VRAM: 4,820 MB (<6GB Budget)\n• Air-gapped 100% Offline Capability",
        fontsize=8.8, color=SLATE_DARK, ha='center', va='center')
ax.text(83.5, 7.0, "backend/model_manager.py", fontsize=7.5, color=SLATE_MED, ha='center', va='center')

# Connect RAG Agent down to ChromaDB (Clean route through inter-tier channel y=25.5)
draw_corner_arrow(ax, [(79.5, card_y - card_h/2), (79.5, 25.5), (19.0, 25.5), (19.0, 19.3)],
                  color=PURPLE_PRIMARY, lw=1.8)

# Connect Quiz & Evaluator to SQLite
draw_arrow(ax, (51.0, card_y - 13.0), (51.0, 19.3), color=BLUE_PRIMARY, lw=1.8)

# Connect Inference Engines
draw_arrow(ax, (83.5, 27.5), (83.5, 19.3), color=GREEN_PRIMARY, lw=1.8)

# ------------------------------------------------------------------------------
# 5. DUAL ADAPTIVE FEEDBACK CORRIDORS (High-Contrast for Print)
# ------------------------------------------------------------------------------
# LOOP A: Fail (<70%) -> 3-Tier Socratic Hint Decay looping into Quiz Agent
draw_corner_arrow(ax, [(71.25, card_y - 1.5), (74.0, card_y - 1.5), (74.0, card_y - 9.0), (55.75, card_y - 9.0)],
                  color=AMBER_PRIMARY, lw=2.2, label="LOOP A: Fail (<70%) -> Socratic Hint Decay", label_pt=(64.5, card_y - 7.5))

# LOOP B: Pass (>=70%) -> Unlock Next DAG Node & notify Orchestrator
draw_corner_arrow(ax, [(64.5, card_y + card_h/2), (64.5, 72.5), (52.0, 72.5)],
                  color=GREEN_PRIMARY, lw=2.4, label="LOOP B: Pass (>=70%) -> DAG Advance & Node Unlock", label_pt=(60.0, 74.0))

# Save print-optimized diagram
out_path = DIAGRAMS_DIR / "hmas_design_architecture.png"
plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print(f"✅ Print-Optimized HMAS Design Diagram successfully generated at: {out_path}")
