#!/usr/bin/env python3
"""
Generate Print-Optimized, Publication-Grade Curriculum Knowledge Graph & Prerequisite Gating Diagram.
Optimized for 8.5x11 / A4 printed technical reports:
  - Large typography (9.0pt to 17pt) legible when scaled down to paper
  - Mathematical Invariant Gating Formulation (Unlocked(v, C) <=> Parents(v) subset C)
  - Side-by-side Dual Operational Gating Verification (Unlocked vs Blocked Anti-Skip)
  - Core Competency Milestone Flow across Cognitive Progression Tiers
  - Complete 36-Node Curriculum Knowledge Grid (Zero omission, full academic rigor)
Output: diagrams/curriculum_knowledge_graph_gating.png (300 DPI)
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

# 16:11.5 Aspect Ratio - Standard Print Dimension
fig, ax = plt.subplots(figsize=(16, 11.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Academic Print Palette
BG_COLOR       = "#ffffff"
DARK_NAVY      = "#0f172a"
SLATE_DARK     = "#1e293b"
SLATE_MED      = "#475569"
CARD_BG        = "#f8fafc"
CARD_BORDER    = "#94a3b8"

# Cognitive Tier Palette
T1_COLOR = "#0284c7"  # Sky Blue (Foundations)
T1_BG    = "#f0f9ff"
T2_COLOR = "#3730a3"  # Indigo (Techniques & Applied)
T2_BG    = "#eef2ff"
T3_COLOR = "#6d28d9"  # Purple (Output Eng & Schemas)
T3_BG    = "#f5f3ff"
T4_COLOR = "#047857"  # Emerald (Reasoning & Capstone)
T4_BG    = "#ecfdf5"

GREEN_SUCCESS = "#047857"
GREEN_BG      = "#ecfdf5"
RED_LOCK      = "#b91c1c"
RED_BG        = "#fef2f2"
AMBER_WARN    = "#b45309"
AMBER_BG       = "#fffbeb"

FONT_FAMILY = "sans-serif"
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

def draw_card(ax, x, y, w, h, bg_color=CARD_BG, border_color=CARD_BORDER, corner_radius=1.2, lw=1.8, zorder=3):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=zorder)
    ax.add_patch(rect)
    return rect

def draw_badge(ax, x, y, text, bg_color=DARK_NAVY, text_color="white", w=4.5, h=2.2, font_size=9.0, zorder=20):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle="round,pad=0,rounding_size=0.6",
                                  facecolor=bg_color, edgecolor="none", zorder=zorder)
    ax.add_patch(rect)
    ax.text(x, y - 0.05, text, color=text_color, fontsize=font_size, fontweight='bold',
            ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)

def draw_arrow(ax, p1, p2, color=SLATE_DARK, lw=2.0, zorder=10):
    arr = patches.FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=16,
                                  color=color, lw=lw, zorder=zorder)
    ax.add_patch(arr)

def draw_corner_arrow(ax, points, color=SLATE_DARK, lw=2.0, zorder=10):
    path = MplPath(points)
    arr = patches.FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=16,
                                  color=color, lw=lw, zorder=zorder)
    ax.add_patch(arr)

# ------------------------------------------------------------------------------
# 1. HEADER (High-Contrast, Large Typography)
# ------------------------------------------------------------------------------
ax.text(50, 97.4, "PROJECT ROAR: CURRICULUM KNOWLEDGE GRAPH & PREREQUISITE GATING",
        fontsize=16.5, fontweight='bold', color=DARK_NAVY, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.text(50, 94.8, "Topological Competency DAG, Bloom's Taxonomy Alignment & Deterministic Anti-Skip Gating Engine",
        fontsize=10.5, fontweight='bold', color=SLATE_MED, ha='center', va='center', fontfamily=FONT_FAMILY)

# ------------------------------------------------------------------------------
# 2. MATHEMATICAL GATING INVARIANT BANNER
# ------------------------------------------------------------------------------
draw_card(ax, 50, 89.8, 96, 5.4, bg_color="#ffffff", border_color=DARK_NAVY, corner_radius=1.2, lw=2.0)
ax.text(5.5, 89.8, "MATHEMATICAL GATING INVARIANT:", fontsize=10.0, fontweight='bold', color=DARK_NAVY, ha='left', va='center')
ax.text(48.5, 89.8, r"$\mathbf{Unlocked}(v, \mathcal{C}) \Longleftrightarrow \forall u \in \mathbf{Parents}(v),\; u \in \mathcal{C}, \quad \text{where } \mathcal{C} = \{ u \in \mathcal{V} \mid S_{\mathrm{final}}(u) \geq \theta_{\mathrm{pass}}(u) \}$",
        fontsize=10.2, fontweight='bold', color=T2_COLOR, ha='center', va='center')
ax.text(94.5, 89.8, "Anti-Skip: 100% Enforced", fontsize=9.5, fontweight='bold', color=GREEN_SUCCESS, ha='right', va='center')

# ------------------------------------------------------------------------------
# 3. DUAL OPERATIONAL GATING VERIFICATION (Side-by-Side Live Proofs)
# ------------------------------------------------------------------------------
# Panel A: Unlocked Gate
draw_card(ax, 27.5, 78.5, 48.0, 13.5, bg_color=GREEN_BG, border_color=GREEN_SUCCESS, corner_radius=1.4, lw=2.0)
draw_badge(ax, 46.0, 83.2, "GATE OPEN", bg_color=GREEN_SUCCESS, text_color="white", w=6.8, h=2.5, font_size=9.2)
ax.text(5.5, 83.2, "SCENARIO A: PREREQUISITE GATE SATISFIED", fontsize=10.5, fontweight='bold', color=GREEN_SUCCESS, ha='left', va='center')
ax.text(5.5, 80.4, "Target Node: node_11 (Contextual Prompting & Delimiters)", fontsize=9.2, fontweight='bold', color=DARK_NAVY, ha='left', va='center')
ax.text(5.5, 78.0, "• Parent 1: node_09 (System Prompting) -> Score: 82% [PASS >= 60%]  -->  [OK]", fontsize=8.6, color=SLATE_DARK, ha='left', va='center')
ax.text(5.5, 75.8, "• Parent 2: node_10 (Role Prompting)   -> Score: 76% [PASS >= 60%]  -->  [OK]", fontsize=8.6, color=SLATE_DARK, ha='left', va='center')
ax.text(5.5, 73.4, "VERDICT: All parents satisfied in LearnerHistory -> Access Granted to Lesson/Quiz", fontsize=8.6, fontweight='bold', color=GREEN_SUCCESS, ha='left', va='center')

# Panel B: Locked Gate (Anti-Skip)
draw_card(ax, 72.5, 78.5, 48.0, 13.5, bg_color=RED_BG, border_color=RED_LOCK, corner_radius=1.4, lw=2.0)
draw_badge(ax, 91.0, 83.2, "LOCKED", bg_color=RED_LOCK, text_color="white", w=6.5, h=2.5, font_size=9.2)
ax.text(50.5, 83.2, "SCENARIO B: PREREQUISITE GATE BLOCKED (ANTI-SKIP)", fontsize=10.5, fontweight='bold', color=RED_LOCK, ha='left', va='center')
ax.text(50.5, 80.4, "Target Node: node_16 (ReAct Agentic Loops)", fontsize=9.2, fontweight='bold', color=DARK_NAVY, ha='left', va='center')
ax.text(50.5, 78.0, "• Required Parent: node_13 (Chain-of-Thought) -> Score: 52% [FAIL < 60%]", fontsize=8.6, color=RED_LOCK, fontweight='bold', ha='left', va='center')
ax.text(50.5, 75.8, "• Security Action: TutorOrchestrator rejects node dispatch (Zero Bypass)", fontsize=8.6, color=SLATE_DARK, ha='left', va='center')
ax.text(50.5, 73.4, "VERDICT: Locked -> Student routed to Socratic Hint Remediation on Node 13", fontsize=8.6, fontweight='bold', color=RED_LOCK, ha='left', va='center')

# ------------------------------------------------------------------------------
# 4. CORE TOPOLOGICAL BACKBONE & BLOOM TAXONOMY PROGRESSION (Milestones)
# ------------------------------------------------------------------------------
# Container for Milestone DAG
draw_card(ax, 50, 52.2, 96, 35.0, bg_color="#ffffff", border_color=SLATE_DARK, corner_radius=1.8, lw=2.2)
ax.text(5.5, 67.8, "CORE TOPOLOGICAL PROGRESSION BACKBONE & BLOOM COGNITIVE TIERS",
        fontsize=11.5, fontweight='bold', color=DARK_NAVY, ha='left', va='center')

# 4 Tier Column Headers
col_x = [15.5, 38.5, 61.5, 84.5]
col_w = 21.0

tier_info = [
    ("TIER 1: FOUNDATIONS", "Remember / Understand", "Pass >= 50%", "W: 1.0 - 1.5", T1_COLOR, T1_BG),
    ("TIER 2: TECHNIQUES", "Apply & Practice", "Pass >= 60%", "W: 1.8 - 2.8", T2_COLOR, T2_BG),
    ("TIER 3: OUTPUT & SCHEMAS", "Analyze & Formulate", "Pass >= 70%", "W: 3.0 - 3.5", T3_COLOR, T3_BG),
    ("TIER 4: REASONING & CAPSTONE", "Evaluate & Create", "Pass >= 75%", "W: 3.8 - 4.0", T4_COLOR, T4_BG),
]

for idx, (tname, bloom, pthresh, wrange, tcol, tbg) in enumerate(tier_info):
    cx = col_x[idx]
    draw_card(ax, cx, 63.8, col_w, 5.0, bg_color=tbg, border_color=tcol, corner_radius=1.0, lw=1.6)
    ax.text(cx, 65.0, tname, fontsize=9.2, fontweight='bold', color=tcol, ha='center', va='center')
    ax.text(cx, 62.8, f"{bloom} | {pthresh} | {wrange}", fontsize=7.5, fontweight='bold', color=SLATE_MED, ha='center', va='center')

# Milestone Cards Data: (col_idx, y, node_id, title, prereq_text, weight, color, bg)
milestones = [
    # Tier 1
    (0, 56.5, "node_01", "01. Prompt Eng. Foundations", "Roots / None", 1.0, T1_COLOR, T1_BG),
    (0, 48.0, "node_04", "04. Sampling: Temperature", "Requires: node_03", 1.5, T1_COLOR, T1_BG),
    (0, 39.5, "node_07", "07. Zero-Shot Directives", "Requires: node_01", 1.2, T1_COLOR, T1_BG),
    
    # Tier 2
    (1, 56.5, "node_05", "05. Top-K & Top-P Sampling", "Requires: node_04", 2.0, T2_COLOR, T2_BG),
    (1, 48.0, "node_08", "08. Few-Shot In-Context", "Requires: node_07", 2.0, T2_COLOR, T2_BG),
    (1, 39.5, "node_11", "11. Context & Delimiters", "Requires: node_09, 10", 2.2, T2_COLOR, T2_BG),
    
    # Tier 3
    (2, 56.5, "node_13", "13. Chain-of-Thought (CoT)", "Requires: node_08", 2.8, T3_COLOR, T3_BG),
    (2, 48.0, "node_28", "28. Variables & Templates", "Requires: node_07", 2.2, T3_COLOR, T3_BG),
    (2, 39.5, "node_34", "34. Pydantic Schemas", "Requires: node_33", 3.2, T3_COLOR, T3_BG),
    
    # Tier 4
    (3, 56.5, "node_15", "15. Tree-of-Thoughts (ToT)", "Requires: node_13", 3.8, T4_COLOR, T4_BG),
    (3, 48.0, "node_16", "16. ReAct Agentic Loops", "Requires: node_13", 4.0, T4_COLOR, T4_BG),
    (3, 39.5, "capstone", "36. Capstone Examination", "Requires: node_16, 34", 4.0, T4_COLOR, T4_BG),
]

m_coords = {}
card_mw = 20.0
card_mh = 6.0

for c_idx, my, nid, title, prereq, w, col, bg in milestones:
    mx = col_x[c_idx]
    m_coords[nid] = (mx, my)
    draw_card(ax, mx, my, card_mw, card_mh, bg_color=bg, border_color=col, corner_radius=1.0, lw=1.8)
    # Title
    ax.text(mx - card_mw/2 + 0.8, my + 1.3, title, fontsize=9.2, fontweight='bold', color=DARK_NAVY, ha='left', va='center')
    # Prerequisites
    ax.text(mx - card_mw/2 + 0.8, my - 1.2, prereq, fontsize=7.8, color=SLATE_MED, ha='left', va='center')
    # Weight Badge
    draw_badge(ax, mx + card_mw/2 - 2.5, my, f"W:{w}", bg_color=col, text_color="white", w=3.8, h=2.0, font_size=8.0)

# Connect Milestone Dependencies with Clean Bold Arrows
# 1. Sampling Dynamics: node_04 -> node_05
draw_arrow(ax, (m_coords["node_04"][0] + card_mw/2, m_coords["node_04"][1]),
               (m_coords["node_05"][0] - card_mw/2, m_coords["node_05"][1]), color=T1_COLOR, lw=2.0)

# 2. Instruction to Few-Shot: node_07 -> node_08
draw_arrow(ax, (m_coords["node_07"][0] + card_mw/2, m_coords["node_07"][1]),
               (m_coords["node_08"][0] - card_mw/2, m_coords["node_08"][1]), color=T1_COLOR, lw=2.0)

# 3. Instruction to Context: node_07 -> node_11
draw_arrow(ax, (m_coords["node_07"][0] + card_mw/2, m_coords["node_07"][1] - 0.5),
               (m_coords["node_11"][0] - card_mw/2, m_coords["node_11"][1] - 0.5), color=T1_COLOR, lw=1.8)

# 4. Few-Shot to CoT: node_08 -> node_13
draw_arrow(ax, (m_coords["node_08"][0] + card_mw/2, m_coords["node_08"][1]),
               (m_coords["node_13"][0] - card_mw/2, m_coords["node_13"][1]), color=T2_COLOR, lw=2.2)

# 5. CoT to ToT: node_13 -> node_15
draw_arrow(ax, (m_coords["node_13"][0] + card_mw/2, m_coords["node_13"][1]),
               (m_coords["node_15"][0] - card_mw/2, m_coords["node_15"][1]), color=T3_COLOR, lw=2.0)

# 6. CoT to ReAct: node_13 -> node_16
draw_arrow(ax, (m_coords["node_13"][0] + card_mw/2, m_coords["node_13"][1] - 1.0),
               (m_coords["node_16"][0] - card_mw/2, m_coords["node_16"][1]), color=T3_COLOR, lw=2.2)

# 7. ReAct to Capstone: node_16 -> Capstone
draw_arrow(ax, (m_coords["node_16"][0], m_coords["node_16"][1] - card_mh/2),
               (m_coords["capstone"][0], m_coords["capstone"][1] + card_mh/2), color=T4_COLOR, lw=2.2)

# 8. Schema to Capstone: node_34 -> Capstone
draw_arrow(ax, (m_coords["node_34"][0] + card_mw/2, m_coords["node_34"][1]),
               (m_coords["capstone"][0] - card_mw/2, m_coords["capstone"][1]), color=T3_COLOR, lw=2.2)

# ------------------------------------------------------------------------------
# 5. COMPLETE 36-NODE CURRICULUM KNOWLEDGE BASE (Directory Grid)
# ------------------------------------------------------------------------------
draw_card(ax, 50, 16.5, 96, 27.0, bg_color="#ffffff", border_color=DARK_NAVY, corner_radius=1.6, lw=2.0)
ax.text(5.5, 28.5, "FULL 36-NODE CURRICULUM TOPOLOGY (Single Source of Truth: data/curriculum_tree.json)",
        fontsize=11.0, fontweight='bold', color=DARK_NAVY, ha='left', va='center')

# 4 Columns of Node Text
tier_lists = [
    # Tier 1 (10 nodes)
    ("FOUNDATIONS & SYNTAX (10 Nodes)", T1_COLOR, [
        "node_01: Intro to Prompt Eng. (W:1.0)",
        "node_03: Output Length / max_tokens (W:1.2)",
        "node_04: Temperature Dynamics (W:1.5)",
        "node_07: Zero-Shot Directives (W:1.2)",
        "node_23: Concrete Demonstrations (W:1.4)",
        "node_24: Design with Simplicity (W:1.3)",
        "node_25: Specific Output Directives (W:1.4)",
        "node_27: Context Window Limits (W:1.5)",
        "node_35: Collaborative Reviews (W:1.2)",
        "node_37: Prompt Versioning & Logs (W:1.3)"
    ]),
    # Tier 2 Part 1
    ("APPLIED TECHNIQUES (9 Nodes)", T2_COLOR, [
        "node_05: Top-K & Top-P Sampling (W:2.0)",
        "node_06: Unified Sampling Dynamics (W:2.2)",
        "node_08: One-Shot & Few-Shot (W:2.0)",
        "node_09: System Prompting (W:2.0)",
        "node_10: Role & Persona Steering (W:1.8)",
        "node_11: Contextual Grounding (W:2.2)",
        "node_12: Step-Back Abstraction (W:2.5)",
        "node_18: Code Generation Prompts (W:2.4)",
        "node_19: Code Explanation & ASTs (W:2.2)",
    ]),
    # Tier 2 Part 2 & Tier 3
    ("ADVANCED TECHNIQUES (9 Nodes)", T3_COLOR, [
        "node_20: Polyglot Code Translation (W:2.5)",
        "node_26: Instructions vs Constraints (W:2.0)",
        "node_28: Variables & Templates (W:2.2)",
        "node_29: Input Formats & Noise (W:2.0)",
        "node_31: Model Update Adaptation (W:2.2)",
        "node_32: Experiment Output Formats (W:2.0)",
        "node_33: JSON Repair & Recovery (W:2.5)",
        "node_36: Chain-of-Thought Traps (W:2.6)",
        "node_13: Chain-of-Thought (CoT) (W:2.8)"
    ]),
    # Tier 3 Expert / Capstone (8 nodes)
    ("EXPERT REASONING & CAPSTONE (8 Nodes)", T4_COLOR, [
        "node_14: Self-Consistency Consensus (W:3.2)",
        "node_15: Tree-of-Thoughts (ToT) (W:3.8)",
        "node_16: ReAct Agentic Loops (W:4.0)",
        "node_17: Automatic Prompt Opt (APO) (W:3.5)",
        "node_21: Vulnerability Review (W:3.2)",
        "node_22: Multimodal Vision Prompts (W:3.4)",
        "node_30: Balanced Few-Shot Mix (W:3.0)",
        "node_34: Pydantic Schema Guards (W:3.2)"
    ])
]

for c_idx, (t_title, t_col, items) in enumerate(tier_lists):
    tx = 6.0 + c_idx * 23.5
    ax.text(tx, 26.2, t_title, fontsize=8.8, fontweight='bold', color=t_col, ha='left', va='center')
    for row_idx, item in enumerate(items):
        iy = 23.8 - row_idx * 2.2
        ax.text(tx, iy, f"• {item}", fontsize=7.6, color=DARK_NAVY, ha='left', va='center')

# Save print-optimized diagram
out_path = DIAGRAMS_DIR / "curriculum_knowledge_graph_gating.png"
plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print(f"✅ Print-Optimized Curriculum Knowledge Graph Diagram successfully generated at: {out_path}")
