#!/usr/bin/env python3
"""
Generate a Publication-Grade, Balanced (Non-Squeezed) IEEE Conference Diagram for Project ROAR Curriculum DAG (Fig. 2).
Form-factor: 16:8.5 aspect ratio, 300 DPI.
Generous vertical card proportions, normal padding, clean academic light theme, high contrast.
"""

from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path as MplPath

OUT_PATH = Path("/Users/a/thesis-prompt-tutor/ieee_paper/figures/fig2_curriculum_dag.png")

fig, ax = plt.subplots(figsize=(16, 8.5), dpi=300, facecolor='#ffffff')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Professional Academic Color Palette
NAVY_HEADER    = "#0f172a"
DARK_NAVY      = "#0f172a"
SLATE_DARK     = "#1e293b"
SLATE_BORDER   = "#64748b"
SLATE_MED      = "#475569"

T1_COLOR = "#0284c7"  # Sky Blue (Foundations)
T1_BG    = "#f0f9ff"
T2_COLOR = "#3730a3"  # Indigo (Techniques)
T2_BG    = "#eef2ff"
T3_COLOR = "#6d28d9"  # Purple (Output & Schemas)
T3_BG    = "#f5f3ff"
T4_COLOR = "#047857"  # Emerald (Reasoning & Capstone)
T4_BG    = "#ecfdf5"

GREEN_SUCCESS = "#047857"
RED_LOCK      = "#b91c1c"
RED_BG        = "#fef2f2"
AMBER_PRIMARY = "#b45309"

FONT_FAMILY = "sans-serif"

def draw_box(ax, x, y, w, h, bg_color="#ffffff", border_color=SLATE_BORDER, corner_radius=1.2, lw=1.6, zorder=3):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=zorder)
    ax.add_patch(rect)
    return rect

def draw_arrow(ax, p1, p2, color=SLATE_DARK, lw=1.8, zorder=10):
    arr = patches.FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                                  color=color, lw=lw, zorder=zorder)
    ax.add_patch(arr)

def draw_corner_arrow(ax, points, color=SLATE_DARK, lw=1.8, zorder=10):
    path = MplPath(points)
    arr = patches.FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=14,
                                  color=color, lw=lw, zorder=zorder)
    ax.add_patch(arr)

# ==============================================================================
# TOP BANNER: MATHEMATICAL GATING INVARIANT & PASS CRITERIA
# ==============================================================================
draw_box(ax, 50, 93.0, 98, 12.0, bg_color="#ffffff", border_color=NAVY_HEADER, corner_radius=1.2, lw=1.8)
ax.text(3.0, 96.5, "CURRICULUM KNOWLEDGE GRAPH: 36-NODE TOPOLOGICAL PREREQUISITE DAG & GATING INVARIANT", 
        fontsize=10.5, fontweight='bold', color=NAVY_HEADER, ha='left', va='center')

inv_latex = r"$\mathbf{Unlocked}(v, \mathcal{C}) \Longleftrightarrow \forall u \in \mathbf{Parents}(v),\; u \in \mathcal{C}, \quad \text{where } \mathcal{C} = \{ u \in \mathcal{V} \mid S_{\mathrm{final}}(u) \geq \theta_{\mathrm{pass}}(u) \}$"
ax.text(50.0, 92.2, inv_latex, fontsize=9.8, fontweight='bold', color=T2_COLOR, ha='center', va='center')

thresh_text = r"Pass Thresholds: $\theta_{\mathrm{pass}} = 0.50$ (Tier 1) $\;\longrightarrow\; 0.60$ (Tier 2) $\;\longrightarrow\; 0.70$ (Tier 3) $\;\longrightarrow\; 0.75$ (Tier 4)  •  Anti-Skip Engine: 100% Enforced"
ax.text(50.0, 88.5, thresh_text, fontsize=8.6, fontweight='bold', color=GREEN_SUCCESS, ha='center', va='center')

# ==============================================================================
# CORE 4-TIER TOPOLOGICAL PROGRESSION
# ==============================================================================
draw_box(ax, 50, 43.0, 98, 84.0, bg_color="#ffffff", border_color=SLATE_DARK, corner_radius=1.5, lw=1.8)

col_x = [14.0, 38.0, 62.0, 86.0]
col_w = 22.0

tier_info = [
    ("TIER 1: FOUNDATIONS", "Remember / Understand", r"$\theta_{\mathrm{pass}} \geq 0.50$", T1_COLOR, T1_BG),
    ("TIER 2: TECHNIQUES", "Apply & Practice", r"$\theta_{\mathrm{pass}} \geq 0.60$", T2_COLOR, T2_BG),
    ("TIER 3: SCHEMAS", "Analyze & Formulate", r"$\theta_{\mathrm{pass}} \geq 0.70$", T3_COLOR, T3_BG),
    ("TIER 4: REASONING & CAPSTONE", "Evaluate & Create", r"$\theta_{\mathrm{pass}} \geq 0.75$", T4_COLOR, T4_BG),
]

for idx, (tname, bloom, pthresh, tcol, tbg) in enumerate(tier_info):
    cx = col_x[idx]
    # Header card for column
    draw_box(ax, cx, 79.5, col_w, 8.5, bg_color=tbg, border_color=tcol, corner_radius=0.9, lw=1.5)
    ax.text(cx, 81.8, tname, fontsize=9.0, fontweight='bold', color=tcol, ha='center', va='center')
    ax.text(cx, 77.2, f"{bloom}  ({pthresh})", fontsize=7.6, fontweight='bold', color=SLATE_MED, ha='center', va='center')

# Milestone Cards Data: (col_idx, y, node_id, title, prereq_text, weight, color, bg)
milestones = [
    # Tier 1 (x=14.0)
    (0, 61.5, "node_01", "01. Prompt Foundations", "Root Node / Unlocked", "W: 1.0", T1_COLOR, T1_BG),
    (0, 39.5, "node_04", "04. Sampling & Temperature", "Prereq: node_01", "W: 1.5", T1_COLOR, T1_BG),
    (0, 17.5, "node_07", "07. Zero-Shot Directives", "Prereq: node_01", "W: 1.2", T1_COLOR, T1_BG),

    # Tier 2 (x=38.0)
    (1, 61.5, "node_05", "05. Top-K & Top-P Sampling", "Prereq: node_04", "W: 2.0", T2_COLOR, T2_BG),
    (1, 39.5, "node_08", "08. Few-Shot In-Context", "Prereq: node_07", "W: 2.0", T2_COLOR, T2_BG),
    (1, 17.5, "node_11", "11. Context & Delimiters", "Prereq: node_07, 08", "W: 2.2", T2_COLOR, T2_BG),

    # Tier 3 (x=62.0)
    (2, 61.5, "node_13", "13. Chain-of-Thought (CoT)", "Prereq: node_08", "W: 2.8", T3_COLOR, T3_BG),
    (2, 39.5, "node_28", "28. Variables & Templates", "Prereq: node_11", "W: 2.2", T3_COLOR, T3_BG),
    (2, 17.5, "node_34", "34. Pydantic Schema Guards", "Prereq: node_28", "W: 3.2", T3_COLOR, T3_BG),

    # Tier 4 (x=86.0)
    (3, 61.5, "node_15", "15. Tree-of-Thoughts (ToT)", "Prereq: node_13", "W: 3.8", T4_COLOR, T4_BG),
    (3, 39.5, "node_16", "16. ReAct Agentic Loops", "Prereq: node_13, 28", "W: 4.0", T4_COLOR, T4_BG),
    (3, 17.5, "node_36", "36. Capstone Examination", "Prereq: node_16, 34", "W: 4.0", T4_COLOR, T4_BG),
]

card_w = 21.0
card_h = 16.5

for (c_idx, cy, nid, title, prereq, weight, col, bg) in milestones:
    cx = col_x[c_idx]
    draw_box(ax, cx, cy, card_w, card_h, bg_color="#ffffff", border_color=col, corner_radius=1.0, lw=1.5)
    
    # Title & Badge
    ax.text(cx - card_w/2 + 1.2, cy + 4.8, title, fontsize=8.6, fontweight='bold', color=DARK_NAVY, ha='left', va='center')
    draw_box(ax, cx + card_w/2 - 2.8, cy + 4.8, 4.4, 3.8, bg_color=col, border_color=col, corner_radius=0.5, lw=1.0)
    ax.text(cx + card_w/2 - 2.8, cy + 4.8, weight, fontsize=7.4, fontweight='bold', color='white', ha='center', va='center')
    
    # Prerequisite status
    ax.text(cx - card_w/2 + 1.2, cy - 0.2, prereq, fontsize=7.8, color=SLATE_MED, ha='left', va='center')
    
    # Gate status pill
    if c_idx == 0 and cy == 61.5:
        pill_text = "ROOT UNLOCKED"
        p_col = GREEN_SUCCESS
        p_bg = T4_BG
    elif c_idx == 3:
        pill_text = "GATE: S_final >= 75%"
        p_col = RED_LOCK
        p_bg = RED_BG
    else:
        pill_text = "PREREQUISITE VERIFIED"
        p_col = T2_COLOR
        p_bg = T2_BG
    draw_box(ax, cx, cy - 5.0, card_w - 2.4, 3.4, bg_color=p_bg, border_color=p_col, corner_radius=0.5, lw=0.9)
    ax.text(cx, cy - 5.0, pill_text, fontsize=7.4, fontweight='bold', color=p_col, ha='center', va='center')

# ==============================================================================
# PREREQUISITE ARROWS (Clean, non-crossing paths)
# ==============================================================================
# Tier 1 Internal: 01 -> 04, 01 -> 07
draw_arrow(ax, (14.0, 53.0), (14.0, 48.0), color=T1_COLOR, lw=1.6)
draw_arrow(ax, (8.5, 53.0), (8.5, 26.0), color=T1_COLOR, lw=1.6)

# Tier 1 to Tier 2:
# 04 -> 05
draw_corner_arrow(ax, [(24.5, 39.5), (26.0, 39.5), (26.0, 61.5), (27.5, 61.5)], color=T2_COLOR, lw=1.6)
# 07 -> 08
draw_corner_arrow(ax, [(24.5, 17.5), (26.0, 17.5), (26.0, 39.5), (27.5, 39.5)], color=T2_COLOR, lw=1.6)
# 07 -> 11
draw_arrow(ax, (24.5, 17.5), (27.5, 17.5), color=T2_COLOR, lw=1.6)

# Tier 2 to Tier 3:
# 08 -> 13
draw_corner_arrow(ax, [(48.5, 39.5), (50.0, 39.5), (50.0, 61.5), (51.5, 61.5)], color=T3_COLOR, lw=1.6)
# 11 -> 28
draw_corner_arrow(ax, [(48.5, 17.5), (50.0, 17.5), (50.0, 39.5), (51.5, 39.5)], color=T3_COLOR, lw=1.6)
# 28 -> 34 (Tier 3 internal)
draw_arrow(ax, (62.0, 31.0), (62.0, 26.0), color=T3_COLOR, lw=1.6)

# Tier 3 to Tier 4:
# 13 -> 15
draw_arrow(ax, (72.5, 61.5), (75.5, 61.5), color=T4_COLOR, lw=1.6)
# 13 -> 16
draw_corner_arrow(ax, [(72.5, 59.0), (74.0, 59.0), (74.0, 39.5), (75.5, 39.5)], color=T4_COLOR, lw=1.6)
# 16 -> 36 (Tier 4 internal)
draw_arrow(ax, (86.0, 31.0), (86.0, 26.0), color=T4_COLOR, lw=1.6)
# 34 -> 36
draw_arrow(ax, (72.5, 17.5), (75.5, 17.5), color=T4_COLOR, lw=1.6)

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300, bbox_inches='tight', facecolor='#ffffff')
plt.close()
print(f"Publication-Grade Balanced Fig 2 successfully rendered to: {OUT_PATH}")
