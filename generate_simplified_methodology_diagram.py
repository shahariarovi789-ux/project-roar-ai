#!/usr/bin/env python3
"""
Generate Simplified, Publication-Grade Research Methodology Diagram for Project ROAR
Enhanced with clean, elegant vector icons matching the reference diagram:
  - Node 1: User Learner (Student Avatar Icon)
  - Node 2: Diagnostic Intake (Survey / Checklist Icon)
  - Node 3: Interactive Workspace (Code Terminal / Monitor Icon)
  - Node 4: Multi-Agent Orchestrator HMAS (Interconnected Multi-Agent Icon)
  - Flanking Left: Vector RAG ChromaDB (Database Cylinders Icon)
  - Flanking Right: Model Context Protocol MCP 2.x (Protocol Bus / Interlock Icon)
  - Node 5: Prompt Execution & LLM (Neural Network Mesh Icon)
  - Node 6: Dual-Stage Evaluation (Rubric Shield & Checkmark Icon)
  - Node 7: Socratic Scaffolding (Lightbulb / Hints Icon)
  - Node 8: Mastery & DAG Unlock (Graduation / Trophy Shield Icon)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# Canvas setup - 300 DPI publication quality
fig, ax = plt.subplots(figsize=(16, 17.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 104)
ax.axis('off')

# Color Palette: Clean, elegant academic theme
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
# HELPER FUNCTIONS: ICONS & BADGES
# ----------------------------------------------------------------------
def draw_badge(ax, x, y, num_str, bg_color=DARK_NAVY, text_color="white", radius=1.9):
    """Draw circular numbered step badge"""
    circle = patches.Circle((x, y), radius, facecolor=bg_color, edgecolor="white", linewidth=1.5, zorder=30)
    ax.add_patch(circle)
    ax.text(x, y - 0.1, num_str, color=text_color, fontsize=12.0, fontweight='bold',
            ha='center', va='center', zorder=31, fontfamily=FONT_FAMILY)

def draw_vector_icon(ax, icon_type, cx, cy, size=2.8, color=DARK_NAVY):
    """Draw crisp vector icons inside each node card"""
    z = 12
    if icon_type == "user":
        # Head
        ax.add_patch(patches.Circle((cx, cy + size * 0.28), size * 0.22, facecolor=color, zorder=z))
        # Body
        ax.add_patch(patches.FancyBboxPatch((cx - size * 0.38, cy - size * 0.42), size * 0.76, size * 0.45,
                                           boxstyle="round,pad=0,rounding_size=0.35", facecolor=color, zorder=z))

    elif icon_type == "intake":
        # Document
        ax.add_patch(patches.FancyBboxPatch((cx - size * 0.32, cy - size * 0.44), size * 0.64, size * 0.88,
                                           boxstyle="round,pad=0,rounding_size=0.12",
                                           facecolor="white", edgecolor=color, linewidth=1.5, zorder=z))
        # Clip
        ax.add_patch(patches.FancyBboxPatch((cx - size * 0.16, cy + size * 0.34), size * 0.32, size * 0.14,
                                           boxstyle="round,pad=0,rounding_size=0.06",
                                           facecolor=color, edgecolor="none", zorder=z+1))
        # Lines
        for dy in [0.12, -0.06, -0.24]:
            ax.plot([cx - size * 0.18, cx + size * 0.18], [cy + size * dy, cy + size * dy],
                    color=color, lw=1.3, zorder=z+1)

    elif icon_type == "workspace":
        # Monitor frame
        ax.add_patch(patches.FancyBboxPatch((cx - size * 0.46, cy - size * 0.26), size * 0.92, size * 0.62,
                                           boxstyle="round,pad=0,rounding_size=0.12",
                                           facecolor="white", edgecolor=color, linewidth=1.5, zorder=z))
        # Stand & Base
        ax.plot([cx, cx], [cy - size * 0.26, cy - size * 0.42], color=color, lw=2.0, zorder=z)
        ax.plot([cx - size * 0.22, cx + size * 0.22], [cy - size * 0.42, cy - size * 0.42], color=color, lw=2.0, zorder=z)
        # </> symbol inside
        ax.text(cx, cy + size * 0.05, "</>", fontsize=9.0, fontweight='bold', color=color,
                ha='center', va='center', zorder=z+1, fontfamily=FONT_FAMILY)

    elif icon_type == "hmas":
        # 3 Multi-agent nodes in triangle
        p1 = (cx, cy + size * 0.28)
        p2 = (cx - size * 0.32, cy - size * 0.24)
        p3 = (cx + size * 0.32, cy - size * 0.24)
        ax.plot([p1[0], p2[0], p3[0], p1[0]], [p1[1], p2[1], p3[1], p1[1]], color=color, lw=1.6, zorder=z)
        for pt in [p1, p2, p3]:
            ax.add_patch(patches.Circle(pt, size * 0.16, facecolor=color, edgecolor="white", lw=1.2, zorder=z+1))
        # Central coordinator
        ax.add_patch(patches.Circle((cx, cy - size * 0.05), size * 0.10, facecolor=color, zorder=z+1))

    elif icon_type == "rag":
        # Stacked database cylinders
        h_d = size * 0.22
        for dy in [0.22, 0.0, -0.22]:
            ax.add_patch(patches.Ellipse((cx, cy + size * dy), size * 0.72, h_d,
                                        facecolor="white", edgecolor=color, linewidth=1.5, zorder=z))
        ax.plot([cx - size * 0.36, cx - size * 0.36], [cy + size * 0.22, cy - size * 0.22], color=color, lw=1.5, zorder=z+1)
        ax.plot([cx + size * 0.36, cx + size * 0.36], [cy + size * 0.22, cy - size * 0.22], color=color, lw=1.5, zorder=z+1)

    elif icon_type == "mcp":
        # Central hub with 4 radiating bus nodes
        ax.add_patch(patches.Circle((cx, cy), size * 0.18, facecolor=color, edgecolor="white", lw=1.2, zorder=z+1))
        coords = [(0, 0.36), (0, -0.36), (-0.36, 0), (0.36, 0)]
        for dx, dy in coords:
            ax.plot([cx, cx + size * dx], [cy, cy + size * dy], color=color, lw=1.6, zorder=z)
            ax.add_patch(patches.Circle((cx + size * dx, cy + size * dy), size * 0.11, facecolor=color, zorder=z+1))

    elif icon_type == "llm":
        # Neural network mesh: 3 inputs, 2 outputs
        inputs = [(cx - size * 0.32, cy + size * 0.24), (cx - size * 0.32, cy), (cx - size * 0.32, cy - size * 0.24)]
        outputs = [(cx + size * 0.32, cy + size * 0.16), (cx + size * 0.32, cy - size * 0.16)]
        for ip in inputs:
            for op in outputs:
                ax.plot([ip[0], op[0]], [ip[1], op[1]], color=SLATE_LIGHT, lw=1.0, zorder=z)
        for ip in inputs:
            ax.add_patch(patches.Circle(ip, size * 0.12, facecolor=color, zorder=z+1))
        for op in outputs:
            ax.add_patch(patches.Circle(op, size * 0.12, facecolor=color, zorder=z+1))

    elif icon_type == "evaluation":
        # Circular seal with checkmark
        ax.add_patch(patches.Circle((cx, cy), size * 0.42, facecolor="white", edgecolor=color, linewidth=1.6, zorder=z))
        # Clean checkmark
        ax.plot([cx - size * 0.22, cx - size * 0.05, cx + size * 0.22],
                [cy, cy - size * 0.16, cy + size * 0.20],
                color=color, lw=2.6, solid_capstyle='round', zorder=z+1)

    elif icon_type == "scaffolding":
        # Lightbulb with hint rays
        ax.add_patch(patches.Circle((cx, cy + size * 0.12), size * 0.26, facecolor="white", edgecolor=color, linewidth=1.6, zorder=z))
        ax.add_patch(patches.FancyBboxPatch((cx - size * 0.12, cy - size * 0.32), size * 0.24, size * 0.22,
                                           boxstyle="round,pad=0,rounding_size=0.06",
                                           facecolor=color, edgecolor="none", zorder=z))
        # 3 rays
        ax.plot([cx, cx], [cy + size * 0.44, cy + size * 0.54], color=color, lw=1.5, zorder=z)
        ax.plot([cx - size * 0.32, cx - size * 0.42], [cy + size * 0.34, cy + size * 0.44], color=color, lw=1.5, zorder=z)
        ax.plot([cx + size * 0.32, cx + size * 0.42], [cy + size * 0.34, cy + size * 0.44], color=color, lw=1.5, zorder=z)

    elif icon_type == "mastery":
        # Trophy / Shield with checkmark
        ax.add_patch(patches.Circle((cx, cy), size * 0.42, facecolor=color, edgecolor="white", linewidth=1.2, zorder=z))
        ax.plot([cx - size * 0.20, cx - size * 0.05, cx + size * 0.20],
                [cy, cy - size * 0.15, cy + size * 0.18],
                color="white", lw=2.6, solid_capstyle='round', zorder=z+1)

def draw_node_card(ax, x, y, w, h, title, subtitle="", badge_num=None, icon_type=None,
                   bg_color=CARD_BG, border_color=CARD_BORDER, title_color=DARK_NAVY,
                   badge_bg=DARK_NAVY, icon_color=None, zorder=3):
    """Draw a clean node card with top-center vector icon, title, and subtitle"""
    card = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle="round,pad=0,rounding_size=1.8",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=1.6, zorder=zorder)
    ax.add_patch(card)
    
    # Draw icon if provided
    ic_color = icon_color if icon_color is not None else title_color
    if icon_type:
        draw_vector_icon(ax, icon_type, x, y + h/2 - 3.4, size=2.8, color=ic_color)
        
    # Text placement below icon
    if subtitle:
        ax.text(x, y - 0.8, title, fontsize=11.2, fontweight='bold', color=title_color,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
        ax.text(x, y - 3.6, subtitle, fontsize=8.8, color=SLATE_MED,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
    else:
        ax.text(x, y - 1.8, title, fontsize=11.2, fontweight='bold', color=title_color,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
        
    if badge_num is not None:
        draw_badge(ax, x - w/2 + 2.0, y + h/2 - 0.5, str(badge_num), bg_color=badge_bg)
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
ax.text(50, 100.2, "PROJECT ROAR: RESEARCH METHODOLOGY & ADAPTIVE TUTORING WORKFLOW",
        fontsize=14.5, fontweight='bold', color=DARK_NAVY, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.text(50, 97.8, "A Grounded Multi-Agent System with Model Context Protocol (MCP) & Vector RAG",
        fontsize=10.0, fontstyle='italic', color=SLATE_MED, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.plot([6, 94], [96.0, 96.0], color=SLATE_LIGHT, lw=1.0)

# ==============================================================================
# ROW 1: INTAKE & WORKSPACE (y = 83)
# ==============================================================================

# Node 1: Learner / User
n1_x, n1_y = 18.0, 83.0
n1_w, n1_h = 22.0, 14.5
draw_node_card(ax, n1_x, n1_y, n1_w, n1_h, "Student Learner", "Intake & Active Submissions",
               badge_num=1, icon_type="user", icon_color=DARK_NAVY)

# Node 2: Diagnostic Onboarding
n2_x, n2_y = 50.0, 83.0
n2_w, n2_h = 24.0, 14.5
draw_node_card(ax, n2_x, n2_y, n2_w, n2_h, "Diagnostic Intake", "Skill Profiling & Calibration",
               badge_num=2, icon_type="intake", icon_color=DARK_NAVY)

# Node 3: Interactive Workspace
n3_x, n3_y = 82.0, 83.0
n3_w, n3_h = 24.0, 14.5
draw_node_card(ax, n3_x, n3_y, n3_w, n3_h, "Interactive Workspace", "Theory & Prompt Sandbox",
               badge_num=3, icon_type="workspace", icon_color=DARK_NAVY)

# Row 1 Horizontal Arrows
draw_arrow(ax, (n1_x + n1_w/2, n1_y), (n2_x - n2_w/2, n2_y), label="Intake Flow")
draw_arrow(ax, (n2_x + n2_w/2, n2_y), (n3_x - n3_w/2, n3_y), label="Start Lesson")

# ==============================================================================
# ROW 2: CORE INTELLIGENCE HUB (HMAS, RAG, MCP) (y = 58)
# ==============================================================================

# Node 4: Multi-Agent Orchestrator (HMAS) - Central Hub
n4_x, n4_y = 50.0, 58.0
n4_w, n4_h = 30.0, 15.0
draw_node_card(ax, n4_x, n4_y, n4_w, n4_h,
               "Multi-Agent Orchestrator (HMAS)",
               "Tutor FSM • Lesson, Quiz & Evaluator",
               badge_num=4, icon_type="hmas", icon_color=ACCENT_INDIGO,
               bg_color="#eef2ff", border_color=ACCENT_INDIGO,
               title_color=ACCENT_INDIGO, badge_bg=ACCENT_INDIGO)

# Flanking Block Left: Vector RAG Grounding
rag_x, rag_y = 18.0, 58.0
rag_w, rag_h = 22.0, 15.0
draw_node_card(ax, rag_x, rag_y, rag_w, rag_h,
               "Vector RAG (ChromaDB)",
               "1,899 Chunks • 4.1x Hallucination Drop",
               icon_type="rag", icon_color=ACCENT_PURPLE,
               bg_color="#f5f3ff", border_color=ACCENT_PURPLE,
               title_color=ACCENT_PURPLE)

# Flanking Block Right: Model Context Protocol (MCP 2.x)
mcp_x, mcp_y = 82.0, 58.0
mcp_w, mcp_h = 22.0, 15.0
draw_node_card(ax, mcp_x, mcp_y, mcp_w, mcp_h,
               "Model Context Protocol",
               "MCP 2.x Client-Server Bus\nCanonical URIs & Strict Schemas",
               icon_type="mcp", icon_color=ACCENT_BLUE,
               bg_color="#f0f9ff", border_color=ACCENT_BLUE,
               title_color=ACCENT_BLUE)

# Connect Flanking Blocks to Multi-Agent Orchestrator
draw_arrow(ax, (rag_x + rag_w/2, rag_y), (n4_x - n4_w/2, n4_y), color=ACCENT_PURPLE, lw=1.8, label="Grounding")
draw_arrow(ax, (mcp_x - mcp_w/2, mcp_y), (n4_x + n4_w/2, n4_y), color=ACCENT_BLUE, lw=1.8, label="Tools & Context")

# Workspace UI (3) connects down to Multi-Agent Orchestrator (4)
draw_corner_arrow(ax, [(n3_x - 4.0, n3_y - n3_h/2), (n3_x - 4.0, 71.5), (n4_x + 8.0, 71.5), (n4_x + 8.0, n4_y + n4_h/2)],
                  color=ARROW_COLOR, lw=1.8, label="User Submission / Query", label_pt=(67.0, 71.5))

# Multi-Agent Orchestrator (4) responds back to Workspace (3)
draw_corner_arrow(ax, [(n4_x + 12.0, n4_y + n4_h/2), (n4_x + 12.0, 74.8), (n3_x, 74.8), (n3_x, n3_y - n3_h/2)],
                  color=ACCENT_INDIGO, lw=1.6, label="Lesson / Challenge Content", label_pt=(67.0, 74.8))

# ==============================================================================
# ROW 3: EXECUTION LAYER (y = 38)
# ==============================================================================

# Node 5: Generative AI & Prompt Execution
n5_x, n5_y = 50.0, 38.0
n5_w, n5_h = 30.0, 13.5
draw_node_card(ax, n5_x, n5_y, n5_w, n5_h,
               "Prompt Execution & LLM",
               "Local Ollama (Llama 3 8B) / Cloud Fallback",
               badge_num=5, icon_type="llm", icon_color=DARK_NAVY)

# Multi-Agent Orchestrator (4) -> Prompt Execution (5)
draw_arrow(ax, (n4_x, n4_y - n4_h/2), (n5_x, n5_y + n5_h/2), label="Executes Prompt Challenge")

# ==============================================================================
# ROW 4: EVALUATION & DUAL ADAPTIVE BRANCHES (y = 15)
# ==============================================================================

# Node 6: Dual-Stage Evaluator (Center)
n6_x, n6_y = 50.0, 15.0
n6_w, n6_h = 28.0, 14.5
draw_node_card(ax, n6_x, n6_y, n6_w, n6_h,
               "Dual-Stage Evaluation",
               "Stage 1: Regex Pattern Rules\nStage 2: Semantic LLM Judge",
               badge_num=6, icon_type="evaluation", icon_color=ACCENT_GREEN,
               bg_color="#ecfdf5", border_color=ACCENT_GREEN,
               title_color=ACCENT_GREEN, badge_bg=ACCENT_GREEN)

# Node 7: Adaptive Socratic Scaffolding (Right Branch)
n7_x, n7_y = 82.0, 15.0
n7_w, n7_h = 24.0, 14.5
draw_node_card(ax, n7_x, n7_y, n7_w, n7_h,
               "Socratic Scaffolding",
               "3-Tier Progressive Hint Decay\nZero Direct Solution Spoilage",
               badge_num=7, icon_type="scaffolding", icon_color=ACCENT_AMBER,
               bg_color="#fffbeb", border_color=ACCENT_AMBER,
               title_color=ACCENT_AMBER, badge_bg=ACCENT_AMBER)

# Node 8: Student Mastery & DAG Unlock (Left Branch)
n8_x, n8_y = 18.0, 15.0
n8_w, n8_h = 24.0, 14.5
draw_node_card(ax, n8_x, n8_y, n8_w, n8_h,
               "Mastery & DAG Unlock",
               "Update 36-Node Mastery Vector\nUnlock Next Prerequisite Node",
               badge_num=8, icon_type="mastery", icon_color=DARK_NAVY,
               bg_color="#f8fafc", border_color=CARD_BORDER,
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

print(f"Generated successfully with vector icons:\n  {out1}\n  {out2}\n  {out3}")
