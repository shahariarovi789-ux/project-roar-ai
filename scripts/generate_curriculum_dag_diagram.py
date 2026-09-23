#!/usr/bin/env python3
"""
Generate Publication-Grade Curriculum Knowledge Graph & Prerequisite Gating Diagram for Project ROAR.
Visualizes:
  - 36-Node Directed Acyclic Graph (DAG) structured across cognitive tiers
  - Topological prerequisite dependency edges
  - Mathematical Prerequisite Gating Mechanism (Unlocked(v, C) <=> Parents(v) subset C)
  - Live Gating Example: Unlocked vs Locked nodes
  - Bloom's Taxonomy alignment, difficulty weights (1.0 to 4.0), and pass thresholds
Output: diagrams/curriculum_knowledge_graph_gating.png (300 DPI)
"""

import os
import json
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

fig, ax = plt.subplots(figsize=(24, 16), dpi=300)
ax.set_xlim(0, 120)
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

# Tier Palettes
T1_COLOR = "#0284c7"  # Sky Blue (Foundations)
T1_BG    = "#f0f9ff"
T2_COLOR = "#4338ca"  # Indigo (Techniques)
T2_BG    = "#eef2ff"
T3_COLOR = "#7c3aed"  # Purple (Reasoning & Output)
T3_BG    = "#f5f3ff"
T4_COLOR = "#059669"  # Green / Emerald (Security & Capstone)
T4_BG    = "#ecfdf5"

GREEN_SUCCESS = "#059669"
RED_LOCK      = "#dc2626"
AMBER_WARN    = "#d97706"

FONT_FAMILY = "sans-serif"
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# ------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------------------
def draw_card(ax, x, y, w, h, bg_color=CARD_BG, border_color=CARD_BORDER, corner_radius=1.2, lw=1.2, zorder=3):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=zorder)
    ax.add_patch(rect)
    return rect

def draw_badge(ax, x, y, text, bg_color=DARK_NAVY, text_color="white", w=3.6, h=1.8, font_size=7.5, zorder=20):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle="round,pad=0,rounding_size=0.6",
                                  facecolor=bg_color, edgecolor="none", zorder=zorder)
    ax.add_patch(rect)
    ax.text(x, y - 0.1, text, color=text_color, fontsize=font_size, fontweight='bold',
            ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)

def draw_arrow(ax, p1, p2, color=SLATE_MED, lw=1.2, zorder=5):
    arr = patches.FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11,
                                  color=color, lw=lw, zorder=zorder)
    ax.add_patch(arr)

# ------------------------------------------------------------------------------
# 1. HEADER BANNER & MATHEMATICAL FORMULATION
# ------------------------------------------------------------------------------
ax.text(60, 97.5, "PROJECT ROAR: CURRICULUM KNOWLEDGE GRAPH & PREREQUISITE GATING",
        fontsize=17, fontweight='bold', color=DARK_NAVY, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.text(60, 95.2, "36-Node Directed Acyclic Graph (DAG) Formalizing Prompt Engineering Competencies across Bloom's Taxonomy",
        fontsize=11, color=SLATE_MED, ha='center', va='center', fontfamily=FONT_FAMILY)

# Mathematical Invariant Box
math_box = draw_card(ax, 60, 89.8, 114, 5.8, bg_color="#f8fafc", border_color=DARK_NAVY, corner_radius=1.2, lw=1.5)
ax.text(12, 90.0, "MATHEMATICAL GATING INVARIANT:", fontsize=8.5, fontweight='bold', color=DARK_NAVY, ha='left', va='center')
ax.text(52, 90.0, "Unlocked(v, C)  <===>  ALL u in Parents(v):  u in C,   where C = { u in V | S_final(u) >= theta_pass(u) }",
        fontsize=10.0, fontweight='bold', color=INDIGO_PRIMARY if 'INDIGO_PRIMARY' in globals() else T2_COLOR, ha='center', va='center')
ax.text(108, 90.0, "Anti-Skip Guarantee: 100%", fontsize=8.5, fontweight='bold', color=GREEN_SUCCESS, ha='right', va='center')

# ------------------------------------------------------------------------------
# 2. PREREQUISITE GATING MECHANISM LIVE SHOWCASE (Interactive Callout)
# ------------------------------------------------------------------------------
# Left Showcase: UNLOCKED NODE
draw_card(ax, 30.0, 81.5, 54.0, 7.8, bg_color="#f0fdf4", border_color=GREEN_SUCCESS, corner_radius=1.2, lw=1.5)
ax.text(6.0, 83.6, "SCENARIO A: PREREQUISITE GATE SATISFIED (NODE UNLOCKED)", fontsize=8.5, fontweight='bold', color=GREEN_SUCCESS, ha='left', va='center')
ax.text(6.0, 81.2, "Target: Node 11 (Contextual Prompting)  |  Prerequisites: [Node 09, Node 10]", fontsize=8.0, color=SLATE_DARK, ha='left', va='center')
ax.text(6.0, 79.2, "• Parent Node 09 (System Prompting): S_final = 82% [PASS >= 60%]  -->  [OK]\n• Parent Node 10 (Role Prompting):   S_final = 76% [PASS >= 60%]  -->  [OK]",
        fontsize=7.2, color=SLATE_MED, ha='left', va='center')
draw_badge(ax, 52.0, 81.5, "GATE OPEN", bg_color=GREEN_SUCCESS, text_color="white", w=6.8, h=2.6, font_size=8.0)

# Right Showcase: LOCKED NODE
draw_card(ax, 89.0, 81.5, 54.0, 7.8, bg_color="#fef2f2", border_color=RED_LOCK, corner_radius=1.2, lw=1.5)
ax.text(65.0, 83.6, "SCENARIO B: PREREQUISITE GATE BLOCKED (NODE LOCKED)", fontsize=8.5, fontweight='bold', color=RED_LOCK, ha='left', va='center')
ax.text(65.0, 81.2, "Target: Node 16 (ReAct Agentic Loops)  |  Prerequisites: [Node 13 (CoT)]", fontsize=8.0, color=SLATE_DARK, ha='left', va='center')
ax.text(65.0, 79.2, "• Parent Node 13 (Chain-of-Thought): S_final = 52% [FAIL < 60%]   -->  [BLOCKED]\n• Access Denied: Student routed to Socratic Remediation before attempting ReAct",
        fontsize=7.2, color=SLATE_MED, ha='left', va='center')
draw_badge(ax, 111.0, 81.5, "LOCKED", bg_color=RED_LOCK, text_color="white", w=6.8, h=2.6, font_size=8.0)

# ------------------------------------------------------------------------------
# 3. 4-TIER KNOWLEDGE GRAPH VISUALIZATION (Columns)
# ------------------------------------------------------------------------------
# Tier Column Definitions
col_w = 27.5
tier_x = [16.0, 45.0, 74.0, 103.0]

tier_meta = [
    {"name": "TIER 1: FOUNDATIONS & SYNTAX", "bloom": "Remember / Understand", "thresh": "Pass >= 50%", "weight": "W: 1.0 - 1.5", "color": T1_COLOR, "bg": T1_BG},
    {"name": "TIER 2: TECHNIQUES & APPLIED", "bloom": "Apply / Practice", "thresh": "Pass >= 60%", "weight": "W: 1.8 - 2.8", "color": T2_COLOR, "bg": T2_BG},
    {"name": "TIER 3: OUTPUT ENG. & SCHEMAS", "bloom": "Analyze / Formulate", "thresh": "Pass >= 70%", "weight": "W: 3.0 - 3.5", "color": T3_COLOR, "bg": T3_BG},
    {"name": "TIER 4: REASONING & CAPSTONE", "bloom": "Evaluate / Create", "thresh": "Pass >= 75%", "weight": "W: 3.8 - 4.0", "color": T4_COLOR, "bg": T4_BG},
]

# Draw Column Banners
for i, tm in enumerate(tier_meta):
    cx = tier_x[i]
    draw_card(ax, cx, 73.0, col_w, 5.0, bg_color=tm["bg"], border_color=tm["color"], corner_radius=1.0, lw=1.6)
    ax.text(cx, 74.3, tm["name"], fontsize=8.5, fontweight='bold', color=tm["color"], ha='center', va='center')
    ax.text(cx, 72.2, f"Bloom: {tm['bloom']}  |  {tm['thresh']}  |  {tm['weight']}", fontsize=7.0, color=SLATE_MED, ha='center', va='center')

# Node definitions per tier with layout coordinates
# Node dict: id, title, weight, prereqs, x, y
node_cards = {}

tier1_nodes = [
    ("node_01", "01. Introduction to Prompt Eng.", 1.0, [], 16.0, 66.5),
    ("node_03", "03. Output Length (max_tokens)", 1.2, ["node_01"], 16.0, 59.8),
    ("node_04", "04. Sampling: Temperature", 1.5, ["node_03"], 16.0, 53.1),
    ("node_07", "07. Zero-Shot Direct Instruction", 1.2, ["node_01"], 16.0, 46.4),
    ("node_24", "24. Simplicity in Prompt Design", 1.3, ["node_07"], 16.0, 39.7),
    ("node_25", "25. Specific Output Directives", 1.4, ["node_07"], 16.0, 33.0),
    ("node_27", "27. Context Window & Truncation", 1.5, ["node_03"], 16.0, 26.3),
    ("node_35", "35. Collaborative Prompt Reviews", 1.2, ["node_01"], 16.0, 19.6),
    ("node_37", "37. Prompt Versioning & Logs", 1.3, ["node_01"], 16.0, 12.9),
]

tier2_nodes = [
    ("node_05", "05. Sampling: Top-K & Top-P", 2.0, ["node_04"], 45.0, 66.5),
    ("node_06", "06. Unified Sampling Dynamics", 2.2, ["node_04", "node_05"], 45.0, 59.8),
    ("node_08", "08. One-Shot & Few-Shot Learning", 2.0, ["node_07"], 45.0, 53.1),
    ("node_09", "09. System Behavioral Prompting", 2.0, ["node_07"], 45.0, 46.4),
    ("node_10", "10. Role & Persona Steering", 1.8, ["node_07"], 45.0, 39.7),
    ("node_11", "11. Contextual Grounding & Delimiters", 2.2, ["node_09", "node_10"], 45.0, 33.0),
    ("node_12", "12. Step-Back Abstraction", 2.5, ["node_07"], 45.0, 26.3),
    ("node_18", "18. Code Generation Prompts", 2.4, ["node_07"], 45.0, 19.6),
    ("node_28", "28. Variables & Templates", 2.2, ["node_07"], 45.0, 12.9),
]

tier3_nodes = [
    ("node_13", "13. Chain-of-Thought (CoT)", 2.8, ["node_08"], 74.0, 66.5),
    ("node_26", "26. Positive vs Negative Bounds", 2.0, ["node_25"], 74.0, 59.8),
    ("node_29", "29. Format Robustness & Noise", 2.0, ["node_28"], 74.0, 53.1),
    ("node_32", "32. Experiment Output Formats", 2.0, ["node_25"], 74.0, 46.4),
    ("node_33", "33. JSON Repair & Format Fixing", 2.5, ["node_32"], 74.0, 39.7),
    ("node_34", "34. Pydantic & Schema Enforcement", 3.2, ["node_33"], 74.0, 33.0),
    ("node_19", "19. Code Explanation & ASTs", 2.2, ["node_07"], 74.0, 26.3),
    ("node_20", "20. Polyglot Code Translation", 2.5, ["node_18"], 74.0, 19.6),
    ("node_36", "36. CoT Best Practices & Traps", 2.6, ["node_13"], 74.0, 12.9),
]

tier4_nodes = [
    ("node_14", "14. Self-Consistency Consensus", 3.2, ["node_13"], 103.0, 66.5),
    ("node_15", "15. Tree-of-Thoughts (ToT)", 3.8, ["node_13"], 103.0, 59.8),
    ("node_16", "16. ReAct Agentic Loops", 4.0, ["node_13"], 103.0, 53.1),
    ("node_17", "17. Automatic Prompt Opt (APO)", 3.5, ["node_08", "node_13"], 103.0, 46.4),
    ("node_21", "21. Debugging & Vulnerability Review", 3.2, ["node_18"], 103.0, 39.7),
    ("node_22", "22. Multimodal Vision Prompting", 3.4, ["node_07", "node_11"], 103.0, 33.0),
    ("node_30", "30. Balanced Few-Shot Sampling", 3.0, ["node_08"], 103.0, 26.3),
    ("node_31", "31. Model Update Regression Test", 2.2, ["node_07"], 103.0, 19.6),
    ("capstone", "36. Summative Capstone Exam", 4.0, ["node_16", "node_34"], 103.0, 12.9),
]

all_nodes_data = [
    (tier1_nodes, T1_COLOR, T1_BG),
    (tier2_nodes, T2_COLOR, T2_BG),
    (tier3_nodes, T3_COLOR, T3_BG),
    (tier4_nodes, T4_COLOR, T4_BG),
]

card_w = 26.0
card_h = 4.8

# Draw Cards
for nodes, color, bg in all_nodes_data:
    for nid, title, weight, prereqs, x, y in nodes:
        node_cards[nid] = (x, y, color, prereqs)
        # Background card
        draw_card(ax, x, y, card_w, card_h, bg_color=bg, border_color=color, corner_radius=0.9, lw=1.2)
        # Node Title
        ax.text(x - card_w/2 + 1.2, y + 0.6, title, fontsize=7.6, fontweight='bold', color=DARK_NAVY, ha='left', va='center')
        # Prerequisites text
        prereq_str = "None (Root)" if not prereqs else f"Requires: {', '.join(prereqs)}"
        ax.text(x - card_w/2 + 1.2, y - 1.0, prereq_str, fontsize=6.2, color=SLATE_MED, ha='left', va='center')
        # Weight Badge
        badge_bg = GREEN_SUCCESS if weight >= 3.8 else (T3_COLOR if weight >= 3.0 else (T2_COLOR if weight >= 2.0 else T1_COLOR))
        draw_badge(ax, x + card_w/2 - 2.5, y, f"W: {weight}", bg_color=badge_bg, text_color="white", w=4.2, h=2.2, font_size=6.8)

# ------------------------------------------------------------------------------
# 4. DRAW PREREQUISITE DIRECTED EDGES (Cleanly Routed)
# ------------------------------------------------------------------------------
# Sample critical cross-tier dependencies
cross_edges = [
    ("node_01", "node_03"),
    ("node_03", "node_04"),
    ("node_04", "node_05"),
    ("node_05", "node_06"),
    ("node_01", "node_07"),
    ("node_07", "node_08"),
    ("node_07", "node_09"),
    ("node_07", "node_10"),
    ("node_09", "node_11"),
    ("node_10", "node_11"),
    ("node_08", "node_13"),
    ("node_13", "node_14"),
    ("node_13", "node_15"),
    ("node_13", "node_16"),
    ("node_07", "node_18"),
    ("node_18", "node_20"),
    ("node_18", "node_21"),
    ("node_25", "node_32"),
    ("node_32", "node_33"),
    ("node_33", "node_34"),
    ("node_34", "capstone"),
    ("node_16", "capstone")
]

for src_id, dst_id in cross_edges:
    if src_id in node_cards and dst_id in node_cards:
        sx, sy, scolor, _ = node_cards[src_id]
        dx, dy, dcolor, _ = node_cards[dst_id]
        
        # If in adjacent columns, draw clean arrow from right edge of src to left edge of dst
        if abs(dx - sx) > 10.0:
            p1 = (sx + card_w/2, sy)
            p2 = (dx - card_w/2, dy)
            draw_arrow(ax, p1, p2, color=scolor, lw=1.2)
        else:
            # Vertical connection in same column
            p1 = (sx, sy - card_h/2)
            p2 = (dx, dy + card_h/2)
            draw_arrow(ax, p1, p2, color=scolor, lw=1.2)

# ------------------------------------------------------------------------------
# 5. FOOTER LEGEND & SPECIFICATIONS
# ------------------------------------------------------------------------------
draw_card(ax, 60, 4.2, 114, 4.6, bg_color="#f8fafc", border_color=DARK_NAVY, corner_radius=1.0, lw=1.2)
ax.text(12, 4.2, "CURRICULUM SPECIFICATIONS:", fontsize=8.0, fontweight='bold', color=DARK_NAVY, ha='left', va='center')
ax.text(32, 4.2, "• Total Nodes: 36 Leaf Competencies", fontsize=7.5, color=SLATE_DARK, ha='left', va='center')
ax.text(54, 4.2, "• Cognitive Weights: W in [1.0, 4.0]", fontsize=7.5, color=SLATE_DARK, ha='left', va='center')
ax.text(76, 4.2, "• Prerequisite Gating: 100% DAG Enforced", fontsize=7.5, color=GREEN_SUCCESS, fontweight='bold', ha='left', va='center')
ax.text(102, 4.2, "• Serialization: data/curriculum_tree.json", fontsize=7.5, color=SLATE_MED, ha='left', va='center')

# Output Path
out_path = DIAGRAMS_DIR / "curriculum_knowledge_graph_gating.png"
plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print(f"✅ Curriculum Knowledge Graph Diagram successfully generated at: {out_path}")
