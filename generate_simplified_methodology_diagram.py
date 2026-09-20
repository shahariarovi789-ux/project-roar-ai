#!/usr/bin/env python3
"""
Generate Simplified, Publication-Grade Research Methodology Diagram for Project ROAR
Symmetrical 8-node loop matching the simplicity and clarity of the user's reference:
  - Top Row: Learner (1) -> Diagnostic Intake (2) -> Interactive Workspace (3)
  - Core Hub: Multi-Agent Orchestrator (4), flanked by Vector RAG (left) & MCP 2.x Bus (right)
  - Execution: Prompt Execution & LLM (5)
  - Assessment: Dual-Stage Evaluation (6)
  - Symmetrical Dual Loops:
      * Right Branch (Fail < 70%): Socratic Scaffolding (7) -> loops up to Workspace (3)
      * Left Branch (Pass >= 70%): Mastery & DAG Unlock (8) -> loops up to Learner / Next Lesson (1)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# Canvas setup - 300 DPI publication quality, balanced aspect ratio
fig, ax = plt.subplots(figsize=(16, 17), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 102)
ax.axis('off')

# Color Palette: Clean, elegant academic theme (neutral slate with purposeful accents)
BG_COLOR       = "#ffffff"
DARK_NAVY      = "#0f172a"
SLATE_DARK     = "#1e293b"
SLATE_MED      = "#475569"
SLATE_LIGHT    = "#94a3b8"
CARD_BG        = "#f8fafc"
CARD_BORDER    = "#cbd5e1"

# Semantic Accents
ACCENT_BLUE    = "#0284c7"   # MCP / Tools
ACCENT_PURPLE  = "#7c3aed"   # RAG / Knowledge
ACCENT_INDIGO  = "#4338ca"   # Multi-Agent
ACCENT_AMBER   = "#d97706"   # Socratic Hints
ACCENT_GREEN   = "#059669"   # Evaluation & Pass
ARROW_COLOR    = "#334155"
FONT_FAMILY    = "sans-serif"

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------
def draw_badge(ax, x, y, num_str, bg_color=DARK_NAVY, text_color="white", radius=1.9):
    """Draw circular numbered step badge matching the reference"""
    circle = patches.Circle((x, y), radius, facecolor=bg_color, edgecolor="white", linewidth=1.5, zorder=30)
    ax.add_patch(circle)
    ax.text(x, y - 0.1, num_str, color=text_color, fontsize=12.0, fontweight='bold',
            ha='center', va='center', zorder=31, fontfamily=FONT_FAMILY)

def draw_node_card(ax, x, y, w, h, title, subtitle="", badge_num=None,
                   bg_color=CARD_BG, border_color=CARD_BORDER, title_color=DARK_NAVY,
                   badge_bg=DARK_NAVY, zorder=3):
    """Draw a clean, spacious node card matching the reference style"""
    card = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle="round,pad=0,rounding_size=1.8",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=1.6, zorder=zorder)
    ax.add_patch(card)
    
    # Title & Subtitle with clean vertical alignment
    if subtitle:
        ax.text(x, y + 1.3, title, fontsize=11.5, fontweight='bold', color=title_color,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
        ax.text(x, y - 1.8, subtitle, fontsize=9.0, color=SLATE_MED,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
    else:
        ax.text(x, y, title, fontsize=11.5, fontweight='bold', color=title_color,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
        
    if badge_num is not None:
        draw_badge(ax, x - w/2 + 2.0, y + h/2 - 0.4, str(badge_num), bg_color=badge_bg)
    return card

def draw_arrow(ax, p1, p2, color=ARROW_COLOR, lw=1.8, label="", rad=0.0):
    """Draw smooth arrow between nodes"""
    if rad == 0.0:
        arr = patches.FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=15, color=color, lw=lw, zorder=10)
    else:
        arr = patches.FancyArrowPatch(p1, p2, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                      mutation_scale=15, color=color, lw=lw, zorder=10)
    ax.add_patch(arr)
    if label:
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2 + rad * 4 + 0.8
        ax.text(mid_x, mid_y, label, fontsize=8.5, fontweight='bold', color=color,
                ha='center', va='center', zorder=15,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=CARD_BORDER, lw=0.8, alpha=0.95))

def draw_corner_arrow(ax, points, color=ARROW_COLOR, lw=1.8, label="", label_pt=None):
    """Draw right-angled arrow corridor"""
    path = Path(points)
    arr = patches.FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=15, color=color, lw=lw, zorder=10)
    ax.add_patch(arr)
    if label:
        pt = label_pt if label_pt is not None else points[len(points)//2]
        ax.text(pt[0], pt[1], label, fontsize=8.5, fontweight='bold', color=color,
                ha='center', va='center', zorder=15,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=CARD_BORDER, lw=0.8, alpha=0.95))

# ==============================================================================
# HEADER BANNER (Top)
# ==============================================================================
ax.text(50, 98.2, "PROJECT ROAR: RESEARCH METHODOLOGY & ADAPTIVE TUTORING WORKFLOW",
        fontsize=14.5, fontweight='bold', color=DARK_NAVY, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.text(50, 95.8, "A Grounded Multi-Agent System with Model Context Protocol (MCP) & Vector RAG",
        fontsize=10.0, fontstyle='italic', color=SLATE_MED, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.plot([6, 94], [94.2, 94.2], color=SLATE_LIGHT, lw=1.0)

# ==============================================================================
# ROW 1: INTAKE & WORKSPACE (y = 82)
# ==============================================================================

# Node 1: Learner / User
n1_x, n1_y = 18.0, 82.0
n1_w, n1_h = 22.0, 11.5
draw_node_card(ax, n1_x, n1_y, n1_w, n1_h, "Student Learner", "Intake & Interaction", badge_num=1)

# Node 2: Diagnostic Onboarding
n2_x, n2_y = 50.0, 82.0
n2_w, n2_h = 24.0, 11.5
draw_node_card(ax, n2_x, n2_y, n2_w, n2_h, "Diagnostic Intake", "Skill Profiling & Calibration", badge_num=2)

# Node 3: Interactive Workspace
n3_x, n3_y = 82.0, 82.0
n3_w, n3_h = 24.0, 11.5
draw_node_card(ax, n3_x, n3_y, n3_w, n3_h, "Interactive Workspace", "Theory & Prompt Sandbox", badge_num=3)

# Row 1 Horizontal Arrows
draw_arrow(ax, (n1_x + n1_w/2, n1_y), (n2_x - n2_w/2, n2_y), label="Intake Flow")
draw_arrow(ax, (n2_x + n2_w/2, n2_y), (n3_x - n3_w/2, n3_y), label="Start Lesson")

# ==============================================================================
# ROW 2: CORE INTELLIGENCE HUB (HMAS, RAG, MCP) (y = 58)
# ==============================================================================

# Node 4: Multi-Agent Orchestrator (HMAS) - Central Hub
n4_x, n4_y = 50.0, 58.0
n4_w, n4_h = 30.0, 13.5
draw_node_card(ax, n4_x, n4_y, n4_w, n4_h,
               "Multi-Agent Orchestrator (HMAS)",
               "Tutor FSM • Lesson, Quiz & Evaluator Agents",
               badge_num=4, bg_color="#eef2ff", border_color=ACCENT_INDIGO,
               title_color=ACCENT_INDIGO, badge_bg=ACCENT_INDIGO)

# Flanking Block Left: Vector RAG Grounding
rag_x, rag_y = 18.0, 58.0
rag_w, rag_h = 22.0, 13.5
draw_node_card(ax, rag_x, rag_y, rag_w, rag_h,
               "Vector RAG (ChromaDB)",
               "1,899 Vetted Chunks\n4.1x Hallucination Drop",
               bg_color="#f5f3ff", border_color=ACCENT_PURPLE,
               title_color=ACCENT_PURPLE)

# Flanking Block Right: Model Context Protocol (MCP 2.x)
mcp_x, mcp_y = 82.0, 58.0
mcp_w, mcp_h = 22.0, 13.5
draw_node_card(ax, mcp_x, mcp_y, mcp_w, mcp_h,
               "Model Context Protocol",
               "MCP 2.x Client-Server Bus\nCanonical URIs & Strict Schemas",
               bg_color="#f0f9ff", border_color=ACCENT_BLUE,
               title_color=ACCENT_BLUE)

# Connect Flanking Blocks to Multi-Agent Orchestrator
draw_arrow(ax, (rag_x + rag_w/2, rag_y), (n4_x - n4_w/2, n4_y), color=ACCENT_PURPLE, lw=1.8, label="Grounding")
draw_arrow(ax, (mcp_x - mcp_w/2, mcp_y), (n4_x + n4_w/2, n4_y), color=ACCENT_BLUE, lw=1.8, label="Tools & Context")

# Workspace UI (3) connects down to Multi-Agent Orchestrator (4)
draw_corner_arrow(ax, [(n3_x - 4.0, n3_y - n3_h/2), (n3_x - 4.0, 71.0), (n4_x + 8.0, 71.0), (n4_x + 8.0, n4_y + n4_h/2)],
                  color=ARROW_COLOR, lw=1.8, label="User Submission / Query", label_pt=(67.0, 71.0))

# Multi-Agent Orchestrator (4) responds back to Workspace (3)
draw_corner_arrow(ax, [(n4_x + 12.0, n4_y + n4_h/2), (n4_x + 12.0, 74.5), (n3_x, 74.5), (n3_x, n3_y - n3_h/2)],
                  color=ACCENT_INDIGO, lw=1.6, label="Lesson / Challenge Content", label_pt=(67.0, 74.5))

# ==============================================================================
# ROW 3: EXECUTION LAYER (y = 39)
# ==============================================================================

# Node 5: Generative AI & Prompt Execution
n5_x, n5_y = 50.0, 39.0
n5_w, n5_h = 30.0, 11.5
draw_node_card(ax, n5_x, n5_y, n5_w, n5_h,
               "Prompt Execution & LLM",
               "Local Ollama (Llama 3 8B) / Cloud Fallback",
               badge_num=5)

# Multi-Agent Orchestrator (4) -> Prompt Execution (5)
draw_arrow(ax, (n4_x, n4_y - n4_h/2), (n5_x, n5_y + n5_h/2), label="Executes Prompt Challenge")

# ==============================================================================
# ROW 4: EVALUATION & DUAL ADAPTIVE BRANCHES (y = 16)
# ==============================================================================

# Node 6: Dual-Stage Evaluator (Center)
n6_x, n6_y = 50.0, 16.0
n6_w, n6_h = 28.0, 13.5
draw_node_card(ax, n6_x, n6_y, n6_w, n6_h,
               "Dual-Stage Evaluation",
               "Stage 1: Regex Pattern Rules\nStage 2: Semantic LLM Judge",
               badge_num=6, bg_color="#ecfdf5", border_color=ACCENT_GREEN,
               title_color=ACCENT_GREEN, badge_bg=ACCENT_GREEN)

# Node 7: Adaptive Socratic Scaffolding (Right Branch)
n7_x, n7_y = 82.0, 16.0
n7_w, n7_h = 24.0, 13.5
draw_node_card(ax, n7_x, n7_y, n7_w, n7_h,
               "Socratic Scaffolding",
               "3-Tier Progressive Hint Decay\nZero Direct Solution Spoilage",
               badge_num=7, bg_color="#fffbeb", border_color=ACCENT_AMBER,
               title_color=ACCENT_AMBER, badge_bg=ACCENT_AMBER)

# Node 8: Student Mastery & DAG Unlock (Left Branch)
n8_x, n8_y = 18.0, 16.0
n8_w, n8_h = 24.0, 13.5
draw_node_card(ax, n8_x, n8_y, n8_w, n8_h,
               "Mastery & DAG Unlock",
               "Update 36-Node Mastery Vector\nUnlock Next Prerequisite Node",
               badge_num=8, bg_color="#f8fafc", border_color=CARD_BORDER,
               title_color=DARK_NAVY, badge_bg=DARK_NAVY)

# Prompt Execution (5) -> Dual-Stage Evaluation (6) (Straight Down)
draw_arrow(ax, (n5_x, n5_y - n5_h/2), (n6_x, n6_y + n6_h/2), label="Student Output to Grade")

# ==============================================================================
# DUAL ADAPTIVE FEEDBACK LOOPS (PERFECT SYMMETRY)
# ==============================================================================

# RIGHT BRANCH: Fail (<70%) -> Node 7 (Socratic Scaffolding)
draw_arrow(ax, (n6_x + n6_w/2, n6_y), (n7_x - n7_w/2, n7_y),
           color=ACCENT_AMBER, lw=2.0, label="Score < 70% (Fail)")

# LOOP A: Socratic Hints loop straight up into Workspace (3) along the right perimeter
draw_corner_arrow(ax, [(n7_x + n7_w/2, n7_y), (96.5, n7_y), (96.5, n3_y), (n3_x + n3_w/2, n3_y)],
                  color=ACCENT_AMBER, lw=2.2, label="LOOP A: Tiered Socratic Hints", label_pt=(96.5, 49.0))

# LEFT BRANCH: Pass (>=70%) -> Node 8 (Mastery & DAG Unlock)
draw_arrow(ax, (n6_x - n6_w/2, n6_y), (n8_x + n8_w/2, n6_y),
           color=ACCENT_GREEN, lw=2.0, label="Score >= 70% (Pass)")

# LOOP B: Mastery loops straight up into Learner / Next Lesson (1) along the left perimeter
draw_corner_arrow(ax, [(n8_x - n8_w/2, n8_y), (3.5, n8_y), (3.5, n1_y), (n1_x - n1_w/2, n1_y)],
                  color=ACCENT_GREEN, lw=2.2, label="LOOP B: Advance Curriculum DAG", label_pt=(3.5, 49.0))

# Output paths
os.makedirs("/Users/a/thesis-prompt-tutor/assets/screenshots", exist_ok=True)
os.makedirs("/Users/a/thesis-prompt-tutor/evaluation/plots", exist_ok=True)

out1 = "/Users/a/thesis-prompt-tutor/assets/screenshots/simplified_methodology_diagram.png"
out2 = "/Users/a/thesis-prompt-tutor/assets/screenshots/methodology_flow_diagram.png"
out3 = "/Users/a/thesis-prompt-tutor/evaluation/plots/figure_simplified_methodology_diagram.png"

plt.tight_layout()
plt.savefig(out1, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.savefig(out2, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.savefig(out3, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print(f"Generated successfully:\n  {out1}\n  {out2}\n  {out3}")
