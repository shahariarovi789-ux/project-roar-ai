#!/usr/bin/env python3
"""
Generate a Publication-Grade, Balanced (Non-Squeezed) IEEE Conference Diagram for Project ROAR HMAS (Fig. 1).
Form-factor: 16:7.8 aspect ratio, 300 DPI.
Generous vertical card proportions, normal padding, clean academic light theme, high contrast.
"""

from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path as MplPath

OUT_PATH = Path("/Users/a/thesis-prompt-tutor/ieee_paper/figures/fig1_hmas_architecture.png")

fig, ax = plt.subplots(figsize=(16, 7.8), dpi=300, facecolor='#ffffff')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Professional Academic Color Palette
NAVY_HEADER    = "#0f172a"
SLATE_BORDER   = "#64748b"
SLATE_TEXT     = "#1e293b"
SLATE_MED      = "#475569"

INDIGO_PRIMARY = "#3730a3"
INDIGO_BG      = "#eef2ff"
BLUE_PRIMARY   = "#0284c7"
BLUE_BG        = "#f0f9ff"
GREEN_PRIMARY  = "#047857"
GREEN_BG       = "#ecfdf5"
AMBER_PRIMARY  = "#b45309"
AMBER_BG       = "#fffbeb"
PURPLE_PRIMARY = "#6d28d9"
PURPLE_BG      = "#f5f3ff"
TEAL_PRIMARY   = "#0f766e"
TEAL_BG        = "#f0fdfa"
FENCE_BORDER   = "#b91c1c"
FENCE_BG       = "#fef2f2"

FONT_FAMILY = "sans-serif"

def draw_box(ax, x, y, w, h, bg_color="#ffffff", border_color=SLATE_BORDER, corner_radius=1.2, lw=1.6, zorder=3):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=zorder)
    ax.add_patch(rect)
    return rect

def draw_arrow(ax, p1, p2, color=NAVY_HEADER, lw=1.8, label="", label_pt=None, ls="-", zorder=12):
    arr = patches.FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                                  color=color, lw=lw, linestyle=ls, zorder=zorder)
    ax.add_patch(arr)
    if label:
        lx = (p1[0] + p2[0]) / 2 if label_pt is None else label_pt[0]
        ly = (p1[1] + p2[1]) / 2 if label_pt is None else label_pt[1]
        ax.text(lx, ly, label, fontsize=8.6, fontweight='bold', color=color,
                ha='center', va='center', zorder=zorder+2,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=SLATE_BORDER, lw=0.9, alpha=0.98))

# ==============================================================================
# TIER 1: SUPERVISORY ORCHESTRATOR & FSM
# ==============================================================================
draw_box(ax, 50, 91.0, 98, 15.5, bg_color="#ffffff", border_color=INDIGO_PRIMARY, corner_radius=1.5, lw=2.0)
ax.text(3.0, 96.2, "TIER 1: SUPERVISORY ORCHESTRATOR & FINITE STATE MACHINE (FSM)",
        fontsize=10.5, fontweight='bold', color=INDIGO_PRIMARY, ha='left', va='center')

# FSM Pipeline display in center
fsm_steps = [
    ("Diagnostic Intake", TEAL_PRIMARY, TEAL_BG),
    ("Curriculum Lesson", BLUE_PRIMARY, BLUE_BG),
    ("Authentic Challenge", AMBER_PRIMARY, AMBER_BG),
    ("Dual-Stream Eval", GREEN_PRIMARY, GREEN_BG),
    ("Mastery Verified", INDIGO_PRIMARY, INDIGO_BG)
]

for idx, (sname, scol, sbg) in enumerate(fsm_steps):
    bx = 13.0 + idx * 18.5
    by = 87.5
    draw_box(ax, bx, by, 16.0, 7.5, bg_color=sbg, border_color=scol, corner_radius=0.9, lw=1.5)
    ax.text(bx, by, sname, fontsize=8.8, fontweight='bold', color=scol, ha='center', va='center')
    if idx < len(fsm_steps) - 1:
        draw_arrow(ax, (bx + 8.0, by), (bx + 10.5, by), color=SLATE_BORDER, lw=1.6)

# ==============================================================================
# TIER 2: SPECIALIZED COGNITIVE AGENTS (DECOUPLED VIA MCP BUS)
# ==============================================================================
draw_box(ax, 50, 52.5, 98, 55.0, bg_color="#ffffff", border_color=NAVY_HEADER, corner_radius=1.5, lw=2.0)
ax.text(3.0, 77.2, "TIER 2: SPECIALIZED COGNITIVE AGENTS (MODEL CONTEXT PROTOCOL DECOUPLING)",
        fontsize=10.5, fontweight='bold', color=NAVY_HEADER, ha='left', va='center')

# Anti-Answer-Leakage Boundary around Socratic Coach & Evaluator Judge
leak_fence = patches.FancyBboxPatch((3.5, 27.5), 51.5, 47.0, boxstyle="round,pad=0,rounding_size=1.2",
                                    facecolor=FENCE_BG, edgecolor=FENCE_BORDER, linewidth=1.8, linestyle="--", zorder=4)
ax.add_patch(leak_fence)
ax.text(29.25, 71.5, "ZERO SOLUTION-LEAKAGE SECURITY BOUNDARY",
        fontsize=8.8, fontweight='bold', color=FENCE_BORDER, ha='center', va='center', zorder=5)

# Agent 1: Socratic Coach
draw_box(ax, 16.0, 48.0, 22.0, 39.0, bg_color=AMBER_BG, border_color=AMBER_PRIMARY, corner_radius=1.0, lw=1.6, zorder=6)
ax.text(16.0, 63.5, "Socratic Coach Agent", fontsize=10.2, fontweight='bold', color=AMBER_PRIMARY, ha='center', va='center', zorder=7)
ax.text(16.0, 59.5, "Scaffolded Instruction", fontsize=8.6, fontweight='bold', color=NAVY_HEADER, ha='center', va='center', zorder=7)
coach_bullets = "• Tiered Socratic Hints\n• Exponential Hint Decay\n• Bloom-Calibrated Tasks\n• Strict Answer Redaction\n• Remediation Routing"
ax.text(16.0, 55.0, coach_bullets, fontsize=8.4, color=SLATE_TEXT, ha='center', va='top', zorder=7, linespacing=1.45)

# Agent 2: Evaluator Judge
draw_box(ax, 42.5, 48.0, 22.0, 39.0, bg_color=GREEN_BG, border_color=GREEN_PRIMARY, corner_radius=1.0, lw=1.6, zorder=6)
ax.text(42.5, 63.5, "Evaluator Judge Agent", fontsize=10.2, fontweight='bold', color=GREEN_PRIMARY, ha='center', va='center', zorder=7)
ax.text(42.5, 59.5, "Dual-Stream Grading", fontsize=8.6, fontweight='bold', color=NAVY_HEADER, ha='center', va='center', zorder=7)
eval_bullets = "• Regex Syntax Verifier\n• LLM Semantic Grader\n• 5-Variable Formulation\n• Inter-Rater Kappa = 0.896\n• Objective Scoring Bounds"
ax.text(42.5, 55.0, eval_bullets, fontsize=8.4, color=SLATE_TEXT, ha='center', va='top', zorder=7, linespacing=1.45)

# Student submission arrow between Coach & Evaluator
draw_arrow(ax, (27.0, 48.0), (31.5, 48.0), color=NAVY_HEADER, lw=1.8, label="Submit", label_pt=(29.25, 51.5), zorder=8)
# Hint feedback loop
path_hint = MplPath([(42.5, 30.5), (42.5, 29.0), (16.0, 29.0), (16.0, 30.5)])
arr_hint = patches.FancyArrowPatch(path=path_hint, arrowstyle="-|>", mutation_scale=12,
                                   color=AMBER_PRIMARY, lw=1.6, zorder=8)
ax.add_patch(arr_hint)
ax.text(29.25, 30.8, "Remediation: Progressive Hint Decay", fontsize=8.0, fontweight='bold', color=AMBER_PRIMARY, ha='center', va='center', zorder=9,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=AMBER_PRIMARY, lw=0.8))

# Agent 3: Knowledge Gatekeeper
draw_box(ax, 68.5, 48.0, 22.0, 45.0, bg_color=BLUE_BG, border_color=BLUE_PRIMARY, corner_radius=1.0, lw=1.6)
ax.text(68.5, 66.5, "Knowledge Gatekeeper", fontsize=10.2, fontweight='bold', color=BLUE_PRIMARY, ha='center', va='center')
ax.text(68.5, 62.5, "DAG Prerequisite Engine", fontsize=8.6, fontweight='bold', color=NAVY_HEADER, ha='center', va='center')
gate_bullets = "• 36-Node Curriculum DAG\n• Topological Invariants\n• 100% Anti-Skip Lock\n• Dynamic Pass Thresholds\n• Prerequisite Traversal"
ax.text(68.5, 57.5, gate_bullets, fontsize=8.4, color=SLATE_TEXT, ha='center', va='top', linespacing=1.45)

# Agent 4: Reflection & State Agent
draw_box(ax, 89.5, 48.0, 17.0, 45.0, bg_color=PURPLE_BG, border_color=PURPLE_PRIMARY, corner_radius=1.0, lw=1.6)
ax.text(89.5, 66.5, "Reflection Agent", fontsize=10.2, fontweight='bold', color=PURPLE_PRIMARY, ha='center', va='center')
ax.text(89.5, 62.5, "Cognitive Tracing", fontsize=8.6, fontweight='bold', color=NAVY_HEADER, ha='center', va='center')
ref_bullets = "• Mastery Tracking\n• EMA Updates (lambda=0.35)\n• Dynamic Time Budgets\n• Learner Analytics\n• Session Profiles"
ax.text(89.5, 57.5, ref_bullets, fontsize=8.4, color=SLATE_TEXT, ha='center', va='top', linespacing=1.45)

# ==============================================================================
# TIER 3: DECOUPLED MCP INFRASTRUCTURE & EDGE RUNTIME
# ==============================================================================
draw_box(ax, 50, 11.5, 98, 19.0, bg_color="#ffffff", border_color=INDIGO_PRIMARY, corner_radius=1.5, lw=2.0)
ax.text(3.0, 18.2, "TIER 3: PERSISTENT STORES & LOCAL EDGE INFERENCE (MCP PROTOCOL TOOLS)",
        fontsize=10.5, fontweight='bold', color=INDIGO_PRIMARY, ha='left', va='center')

# Service 1: ChromaDB RAG
draw_box(ax, 19.0, 9.5, 28.0, 12.5, bg_color=PURPLE_BG, border_color=PURPLE_PRIMARY, corner_radius=0.9, lw=1.4)
ax.text(19.0, 13.0, "ChromaDB Vector RAG", fontsize=9.4, fontweight='bold', color=PURPLE_PRIMARY, ha='center', va='center')
ax.text(19.0, 8.2, "1,899 Grounded Exemplars • Sub-ms Retrieval\nHallucination Reduction: 24.8% -> 1.2%",
        fontsize=8.0, color=SLATE_TEXT, ha='center', va='center')

# Service 2: SQLite & Curriculum DAG
draw_box(ax, 50.0, 9.5, 31.0, 12.5, bg_color=BLUE_BG, border_color=BLUE_PRIMARY, corner_radius=0.9, lw=1.4)
ax.text(50.0, 13.0, "Curriculum Knowledge DAG", fontsize=9.4, fontweight='bold', color=BLUE_PRIMARY, ha='center', va='center')
ax.text(50.0, 8.2, "36 Competency Nodes • Strict DAG Prerequisite Graph\nFastMCP Server JSON-RPC 2.0 Dispatch",
        fontsize=8.0, color=SLATE_TEXT, ha='center', va='center')

# Service 3: Quantized Local LLM
draw_box(ax, 81.0, 9.5, 28.0, 12.5, bg_color=GREEN_BG, border_color=GREEN_PRIMARY, corner_radius=0.9, lw=1.4)
ax.text(81.0, 13.0, "Edge Quantized Inference", fontsize=9.4, fontweight='bold', color=GREEN_PRIMARY, ha='center', va='center')
ax.text(81.0, 8.2, "4-bit NF4 QLoRA • DeepSeek / Qwen 7B\nPeak VRAM < 5.8 GB • 100% Offline Capable",
        fontsize=8.0, color=SLATE_TEXT, ha='center', va='center')

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300, bbox_inches='tight', facecolor='#ffffff')
plt.close()
print(f"Publication-Grade Balanced Fig 1 successfully rendered to: {OUT_PATH}")
