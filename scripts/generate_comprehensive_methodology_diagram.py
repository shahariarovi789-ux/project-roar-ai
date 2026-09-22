#!/usr/bin/env python3
"""
Generate Publication-Grade End-to-End Comprehensive Methodology Diagram for Project ROAR
Structure:
  - 5 Distinct Horizontal Tiers with Left-Side Vertical Tier Category Badges
  - Tier 1: Student Workspace & Interaction Layer (User, Diagnostic Onboarding, Workspace UI)
  - Tier 2: Hierarchical Multi-Agent Orchestration (HMAS) (Tutor Orchestrator FSM + 5 Sub-Agents)
  - Tier 3: Model Context Protocol (MCP 2.x) Protocol Bus (Full-width Bus + 4 Canonical URIs)
  - Tier 4: Grounded Knowledge, RAG & Persistent Repository (Curriculum DAG, ChromaDB, Student Repo)
  - Tier 5: Inference Engine & Dual Adaptive Feedback Loops (LLM Arbiter + Dual-Stage Evaluator)
  - 10 Numbered Lifecycle Step Badges (1 to 10)
  - 2 Dedicated Feedback Corridors: Loop A (Socratic Scaffolding) and Loop B (Mastery & DAG Unlock)
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path as MplPath

ROOT_DIR = Path(__file__).resolve().parent.parent

# Canvas setup - 300 DPI publication quality
fig, ax = plt.subplots(figsize=(18, 26), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(140)
ax.set_ylim(0, 140)
ax.axis('off')

# Color Palette (Publication-Grade Academic Palette)
DARK_NAVY    = "#0f172a"
SLATE_DARK   = "#1e293b"
SLATE_MED    = "#475569"
SLATE_LIGHT  = "#94a3b8"
BG_COLOR     = "#ffffff"
PANEL_BG     = "#f8fafc"
PANEL_BORDER = "#cbd5e1"

INDIGO_ACCENT = "#4338ca"
INDIGO_BG     = "#eef2ff"
BLUE_ACCENT   = "#0284c7"
BLUE_BG       = "#f0f9ff"
PURPLE_ACCENT = "#7c3aed"
PURPLE_BG     = "#f5f3ff"
GREEN_ACCENT  = "#059669"
GREEN_BG      = "#ecfdf5"
AMBER_ACCENT  = "#d97706"
AMBER_BG      = "#fffbeb"
CORAL_ACCENT  = "#e11d48"

ARROW_COLOR = "#1e293b"
FONT_FAMILY = "sans-serif"

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------
def draw_badge(ax, x, y, num_str, bg_color=DARK_NAVY, text_color="white", radius=1.6):
    """Draw circular numbered step badge"""
    circle = patches.Circle((x, y), radius, facecolor=bg_color, edgecolor="white", linewidth=1.2, zorder=30)
    ax.add_patch(circle)
    ax.text(x, y - 0.1, num_str, color=text_color, fontsize=10.5, fontweight='bold',
            ha='center', va='center', zorder=31, fontfamily=FONT_FAMILY)

def draw_tier_tab(ax, x, y, w, h, tier_label, sub_label="", bg_color=DARK_NAVY, border_color=DARK_NAVY):
    """Draw prominent vertical tab pill on the left of each tier"""
    tab = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.5",
                                facecolor=bg_color, edgecolor=border_color, linewidth=1.2, zorder=2)
    ax.add_patch(tab)
    
    # Combined vertical text
    full_text = f"{tier_label}  •  {sub_label}" if sub_label else tier_label
    ax.text(x + w/2, y + h/2, full_text, fontsize=9.5, fontweight='bold', color="white",
            ha='center', va='center', rotation=90, zorder=3, fontfamily=FONT_FAMILY)

def draw_panel(ax, x, y, w, h, subtitle="", bg_color=PANEL_BG, border_color=PANEL_BORDER):
    """Draw section container panel with right-aligned subtitle"""
    panel = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=2.0",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=1.4, zorder=1)
    ax.add_patch(panel)
    if subtitle:
        ax.text(x + w - 2.5, y + h - 2.2, subtitle, fontsize=9.0, fontstyle='italic',
                color=SLATE_MED, ha='right', va='center', zorder=2, fontfamily=FONT_FAMILY)
    return panel

def draw_card(ax, x, y, w, h, title, subtitle="", items=None, bg_color="white", border_color=PANEL_BORDER,
              title_color=DARK_NAVY, corner_radius=1.2, zorder=3):
    """Draw card box with title, subtitle, and bullet points with proper padding"""
    card = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=1.4, zorder=zorder)
    ax.add_patch(card)
    
    if subtitle:
        ax.text(x, y + h/2 - 1.8, title, fontsize=10.5, fontweight='bold', color=title_color,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
        ax.text(x, y + h/2 - 3.4, subtitle, fontsize=8.5, color=SLATE_MED,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
    else:
        ax.text(x, y + h/2 - 2.2, title, fontsize=10.5, fontweight='bold', color=title_color,
                ha='center', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
    
    if items:
        sep_y = y + h/2 - 4.5
        ax.plot([x - w/2 + 1.2, x + w/2 - 1.2], [sep_y, sep_y], color=border_color, lw=0.8, zorder=zorder+1)
        for i, item in enumerate(items):
            item_y = sep_y - 1.8 - i * 1.9
            ax.text(x - w/2 + 1.5, item_y, f"• {item}", fontsize=8.2, color=SLATE_DARK,
                    ha='left', va='center', zorder=zorder+1, fontfamily=FONT_FAMILY)
    return card

def draw_arrow(ax, p1, p2, color=ARROW_COLOR, lw=1.6, label="", rad=0.0):
    if rad == 0.0:
        arr = patches.FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14, color=color, lw=lw, zorder=10)
    else:
        arr = patches.FancyArrowPatch(p1, p2, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                      mutation_scale=14, color=color, lw=lw, zorder=10)
    ax.add_patch(arr)
    if label:
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2 + rad * 5 + 0.8
        ax.text(mid_x, mid_y, label, fontsize=8, fontweight='bold', color=color,
                ha='center', va='center', zorder=15,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=PANEL_BORDER, lw=0.8, alpha=0.95))

def draw_corner_arrow(ax, points, color=ARROW_COLOR, lw=1.6, label="", label_pt=None):
    path = MplPath(points)
    arr = patches.FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=14, color=color, lw=lw, zorder=10)
    ax.add_patch(arr)
    if label:
        pt = label_pt if label_pt is not None else points[len(points)//2]
        ax.text(pt[0], pt[1], label, fontsize=8, fontweight='bold', color=color,
                ha='center', va='center', zorder=15,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=PANEL_BORDER, lw=0.8, alpha=0.95))

# ==============================================================================
# HEADER BANNER (Top)
# ==============================================================================
ax.text(50, 137.2, "PROJECT ROAR: END-TO-END SYSTEM ARCHITECTURE & METHODOLOGY",
        fontsize=15.5, fontweight='bold', color=DARK_NAVY, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.text(50, 134.8, "Hierarchical Multi-Agent Orchestration • Model Context Protocol (MCP 2.x) • Vector RAG • Socratic Tutoring",
        fontsize=10.5, fontstyle='italic', color=SLATE_MED, ha='center', va='center', fontfamily=FONT_FAMILY)
ax.plot([3, 97], [133.2, 133.2], color=SLATE_LIGHT, lw=1.2)

# ==============================================================================
# TIER 1: STUDENT WORKSPACE & INTERACTION LAYER (y: 111 to 131)
# ==============================================================================
draw_tier_tab(ax, 2.0, 111, 4.2, 20, "TIER 1", "STUDENT INTERACTION", bg_color=DARK_NAVY, border_color=DARK_NAVY)
draw_panel(ax, 7.2, 111, 90.6, 20, subtitle="Client-Facing Presentation & Diagnostic Intake")

# 1. USER
user_x, user_y = 15.5, 121
user_circle = patches.Circle((user_x, user_y), 4.2, facecolor=DARK_NAVY, edgecolor="none", zorder=4)
ax.add_patch(user_circle)
ax.add_patch(patches.Circle((user_x, user_y + 1.2), 1.3, facecolor="white", zorder=5))
ax.add_patch(patches.Polygon([[user_x - 2.5, user_y - 3.2], [user_x - 1.4, user_y - 0.5],
                              [user_x + 1.4, user_y - 0.5], [user_x + 2.5, user_y - 3.2]],
                             facecolor="white", zorder=5))
draw_badge(ax, user_x - 3.8, user_y + 3.8, "1")
ax.text(user_x, user_y - 5.5, "USER\n(Student Learner)", fontsize=9.5, fontweight='bold',
        ha='center', va='center', color=DARK_NAVY, fontfamily=FONT_FAMILY)

# 2. Diagnostic Onboarding
diag_x, diag_y = 39.0, 121
draw_card(ax, diag_x, diag_y, 22, 12.5, "Diagnostic Onboarding", "Intake Assessment",
          items=["Goal & Track Calibration", "Baseline Skill Profiling", "Cold-Start State Init"],
          bg_color="white", border_color=PANEL_BORDER)
draw_badge(ax, diag_x - 9.5, diag_y + 4.8, "2")

# 3. Interactive Student Workspace UI
ui_x, ui_y = 75.5, 121
draw_card(ax, ui_x, ui_y, 37, 12.5, "Interactive Student Workspace UI", "Web GUI (Streamlit / FastAPI)",
          items=["Lesson & Theory Viewer (Markdown / Code)", "Prompt Engineering Sandbox & Terminal", "Socratic Chat Dialogue & Real-Time Hints"],
          bg_color="white", border_color=PANEL_BORDER)
draw_badge(ax, ui_x - 17.0, ui_y + 4.8, "3")

# Direct arrow: User -> Diagnostic Onboarding
draw_arrow(ax, (user_x + 4.5, user_y), (diag_x - 11, diag_y), label="Intake Flow")
# Direct arrow: Diagnostic Onboarding -> Workspace UI
draw_arrow(ax, (diag_x + 11, diag_y), (ui_x - 18.5, ui_y), label="Start Curriculum")
# User direct ongoing interaction (routes cleanly below)
draw_corner_arrow(ax, [(user_x, user_y - 4.5), (user_x, 113.5), (ui_x - 10, 113.5), (ui_x - 10, ui_y - 6.25)],
                  color=DARK_NAVY, lw=1.3, label="Active Prompt Submissions", label_pt=(46, 113.5))

# ==============================================================================
# TIER 2: HIERARCHICAL MULTI-AGENT ORCHESTRATION (HMAS) (y: 83 to 109)
# ==============================================================================
draw_tier_tab(ax, 2.0, 83, 4.2, 26, "TIER 2", "HMAS ORCHESTRATION", bg_color=INDIGO_ACCENT, border_color=INDIGO_ACCENT)
draw_panel(ax, 7.2, 83, 90.6, 26, subtitle="Decoupled Cognitive Roles & State Supervision")

# Central Orchestrator / State Machine
orch_x, orch_y = 52.5, 101.5
draw_card(ax, orch_x, orch_y, 48, 7.5, "Tutor Orchestrator & State Machine",
          "Deterministic FSM: Intake -> Teach -> Challenge -> Evaluate -> Scaffold -> Advance",
          bg_color=INDIGO_BG, border_color=INDIGO_ACCENT, title_color=INDIGO_ACCENT)
draw_badge(ax, orch_x - 22.5, orch_y + 2.5, "4", bg_color=INDIGO_ACCENT)

# 5 Specialized Sub-Agents
agent_y = 89.5
w_ag = 16.5
h_ag = 11.5

# Agent 1: Lesson Agent
ag1_x = 16.5
draw_card(ax, ag1_x, agent_y, w_ag, h_ag, "Lesson Agent", "Theory & Concepts",
          items=["Bloom-aligned theory", "Grounded code examples", "Anti-answer leakage"],
          bg_color="white", border_color=PANEL_BORDER)

# Agent 2: Quiz Agent
ag2_x = 34.5
draw_card(ax, ag2_x, agent_y, w_ag, h_ag, "Quiz Agent", "Challenge Synthesis",
          items=["Context-aware tasks", "Few-shot rubrics", "Adversarial test cases"],
          bg_color="white", border_color=PANEL_BORDER)

# Agent 3: Evaluator Agent
ag3_x = 52.5
draw_card(ax, ag3_x, agent_y, w_ag, h_ag, "Evaluator Agent", "Dual-Stage Scoring",
          items=["Regex pattern check", "Semantic LLM judge", "5-variable scoring"],
          bg_color=GREEN_BG, border_color=GREEN_ACCENT, title_color=GREEN_ACCENT)

# Agent 4: Hint Agent (Socratic Scaffolding)
ag4_x = 70.5
draw_card(ax, ag4_x, agent_y, w_ag, h_ag, "Hint Agent", "Socratic Scaffolding",
          items=["Tier 1: Conceptual", "Tier 2: Structural", "Tier 3: Corrective"],
          bg_color=AMBER_BG, border_color=AMBER_ACCENT, title_color=AMBER_ACCENT)

# Agent 5: Hardware Scout
ag5_x = 88.5
draw_card(ax, ag5_x, agent_y, w_ag, h_ag, "Hardware Scout", "Inference Arbiter",
          items=["VRAM & GPU monitor", "Ollama local check", "Cloud LLM fallback"],
          bg_color="white", border_color=PANEL_BORDER)

# Connect Orchestrator to Agents
for ag_x in [ag1_x, ag2_x, ag3_x, ag4_x, ag5_x]:
    draw_corner_arrow(ax, [(orch_x, orch_y - 3.75), (orch_x, 96.5), (ag_x, 96.5), (ag_x, agent_y + h_ag/2)], color=INDIGO_ACCENT, lw=1.3)

# UI to Orchestrator connection
draw_arrow(ax, (ui_x - 6, ui_y - 6.25), (orch_x + 14, orch_y + 3.75), rad=0.2, label="Events / Prompts")
draw_arrow(ax, (orch_x + 18, orch_y + 3.75), (ui_x - 2, ui_y - 6.25), rad=-0.2, label="Agent Responses")

# ==============================================================================
# TIER 3: MODEL CONTEXT PROTOCOL (MCP 2.x) PROTOCOL BUS (y: 55 to 81)
# ==============================================================================
draw_tier_tab(ax, 2.0, 55, 4.2, 26, "TIER 3", "MCP 2.x PROTOCOL BUS", bg_color=BLUE_ACCENT, border_color=BLUE_ACCENT)
draw_panel(ax, 7.2, 55, 90.6, 26, subtitle="", bg_color=BLUE_BG, border_color=BLUE_ACCENT)

# MCP Bus Center Node - Full-Width Hardware-Style System Bus
mcp_x, mcp_y = 52.5, 74.5
draw_card(ax, mcp_x, mcp_y, 86.0, 5.5, "MCP 2.x Client-Server Bus  [ mcp_server/server.py <-> client.py ]",
          "Standardized JSON-RPC 2.0 Dispatcher • Strict Pydantic Schema Validation • 0% Context Drift",
          bg_color="white", border_color=BLUE_ACCENT, title_color=BLUE_ACCENT)
draw_badge(ax, mcp_x - 41.5, mcp_y + 1.8, "5", bg_color=BLUE_ACCENT)

# Straight down vertical arrows from Tier 2 Agents into MCP Bus Top
for ag_x in [ag1_x, ag2_x, ag3_x, ag4_x, ag5_x]:
    draw_arrow(ax, (ag_x, agent_y - h_ag/2), (ag_x, mcp_y + 2.75), color=BLUE_ACCENT, lw=1.3)

# MCP 4 Canonical Tools/Resources - Sized and Spaced to leave open corridor at x=66
w_mcp = 18.0
h_mcp = 11.5
mcp_res_y = 62.5

# Resource 1: Curriculum DAG Resource
r1_x = 17.5
draw_card(ax, r1_x, mcp_res_y, w_mcp, h_mcp, "roar://curriculum/dag", "Knowledge Graph URI",
          items=["get_curriculum_structure()", "validate_prerequisites()", "get_next_lesson()"],
          bg_color="white", border_color=BLUE_ACCENT)

# Resource 2: RAG Vector Search Tool
r2_x = 37.5
draw_card(ax, r2_x, mcp_res_y, w_mcp, h_mcp, "roar://rag/search", "Vector Grounding URI",
          items=["fetch_rag_context()", "similarity_search(k=3)", "query_expansion()"],
          bg_color="white", border_color=BLUE_ACCENT)

# Resource 3: Rubric Tool
r3_x = 56.5
draw_card(ax, r3_x, mcp_res_y, 16.5, h_mcp, "roar://rubric", "Evaluation Tool URI",
          items=["evaluate_prompt()", "compute_5var_score()", "trigger_scaffolding()"],
          bg_color="white", border_color=BLUE_ACCENT)

# Resource 4: Student State Resource
r4_x = 81.0
draw_card(ax, r4_x, mcp_res_y, 20.0, h_mcp, "roar://student/mastery", "Student State URI",
          items=["get_student_profile()", "update_mastery_vector()", "log_student_attempt()"],
          bg_color="white", border_color=BLUE_ACCENT)

# Connect MCP Bus to its 4 resources
for rx in [r1_x, r2_x, r3_x, r4_x]:
    draw_arrow(ax, (rx, mcp_y - 2.75), (rx, mcp_res_y + h_mcp/2), color=BLUE_ACCENT, lw=1.3)

# ==============================================================================
# TIER 4: GROUNDED KNOWLEDGE, RAG & PERSISTENT REPOSITORY (y: 27 to 53)
# ==============================================================================
draw_tier_tab(ax, 2.0, 27, 4.2, 26, "TIER 4", "KNOWLEDGE & RAG LAYER", bg_color=PURPLE_ACCENT, border_color=PURPLE_ACCENT)
draw_panel(ax, 7.2, 27, 90.6, 26, subtitle="Vector Retrieval & Relational State Storage")

# 1. 36-Node Curriculum DAG (Aligned with r1_x)
dag_x, dag_y = 19.5, 38.5
draw_card(ax, dag_x, dag_y, 24.0, 16.5, "36-Node Curriculum DAG", "Knowledge Graph Topology",
          items=["4 Tiers: Foundational -> Frontier", "Bloom's Taxonomy Progression", "Strict Topological Sorting", "Prerequisite Gating & Lock/Unlock"],
          bg_color="white", border_color=PANEL_BORDER)
draw_badge(ax, dag_x - 10.5, dag_y + 6.8, "6")

# 2. ChromaDB Vector Store (RAG) (Aligned with r2_x)
rag_x, rag_y = 49.0, 38.5
draw_card(ax, rag_x, rag_y, 27.0, 16.5, "ChromaDB Vector Store (RAG)", "Semantic Grounding Engine",
          items=["1,899 Vetted Technical Chunks", "all-MiniLM-L6-v2 Embeddings", "Cosine Similarity Threshold (>= 0.72)", "4.1x Hallucination Reduction (Cat 2)"],
          bg_color=PURPLE_BG, border_color=PURPLE_ACCENT, title_color=PURPLE_ACCENT)
draw_badge(ax, rag_x - 12.0, rag_y + 6.8, "7", bg_color=PURPLE_ACCENT)

# 3. Student Data Repository (SQLite) (Aligned with r4_x)
repo_x, repo_y = 81.0, 38.5
draw_card(ax, repo_x, repo_y, 24.0, 16.5, "Student Data Repository", "SQLite Persistent Storage",
          items=["Mastery Vector (36 Nodes)", "Session & Attempt Audit Logs", "Scaffolding Decay Tracker", "Latency & VRAM Telemetry"],
          bg_color="white", border_color=PANEL_BORDER)
draw_badge(ax, repo_x - 10.5, rag_y + 6.8, "8")

# Connect Tier 3 MCP URIs straight down to Tier 4 Backends (Zero text collision)
draw_arrow(ax, (r1_x, mcp_res_y - h_mcp/2), (dag_x, dag_y + 8.25), color=BLUE_ACCENT, lw=1.3, label="Queries DAG")
draw_arrow(ax, (r2_x, mcp_res_y - h_mcp/2), (rag_x - 5, rag_y + 8.25), color=PURPLE_ACCENT, lw=1.3, label="Dense Retrieval")
draw_arrow(ax, (r4_x, mcp_res_y - h_mcp/2), (repo_x, repo_y + 8.25), color=BLUE_ACCENT, lw=1.3, label="Read/Write State")

# ==============================================================================
# TIER 5: INFERENCE ENGINE & DUAL ADAPTIVE FEEDBACK LOOPS (y: 3 to 25)
# ==============================================================================
draw_tier_tab(ax, 2.0, 3, 4.2, 22.5, "TIER 5", "INFERENCE & LOOPS", bg_color=GREEN_ACCENT, border_color=GREEN_ACCENT)
draw_panel(ax, 7.2, 3, 90.6, 22.5, subtitle="Execution, Multi-Metric Evaluation & Feedback Cycles")

# Dual-Engine LLM Inference
llm_x, llm_y = 27.5, 13.5
draw_card(ax, llm_x, llm_y, 38.0, 15, "Dual-Engine LLM Inference Arbiter", "Execution Layer",
          items=["Primary: Local Ollama (Llama 3 8B, Q4_K_M)", "Secondary: Remote Cloud Fallback (OpenAI / Claude)", "Zero-Leakage System Prompt Isolation", "Context Injection from ChromaDB RAG"],
          bg_color="white", border_color=PANEL_BORDER)
draw_badge(ax, llm_x - 17.5, llm_y + 6.2, "9")

# Dual-Stage Evaluator Engine
eval_engine_x, eval_engine_y = 76.5, 13.5
draw_card(ax, eval_engine_x, eval_engine_y, 40.0, 15, "Dual-Stage Evaluator & Scoring Engine", "Assessment Layer",
          items=["Stage 1: Deterministic Regex & Pattern Validation", "Stage 2: Semantic LLM Judge (Bloom Rubrics)", "5-Variable Formula (Score, Latency, Hints...)", "Inter-Rater Reliability: Cohen's Kappa kappa = 0.8963"],
          bg_color=GREEN_BG, border_color=GREEN_ACCENT, title_color=GREEN_ACCENT)
draw_badge(ax, eval_engine_x - 18.5, eval_engine_y + 6.2, "10", bg_color=GREEN_ACCENT)

# Connect RAG to LLM Inference (routed cleanly)
draw_corner_arrow(ax, [(rag_x - 6, dag_y - 8.25), (rag_x - 6, 22.0), (llm_x + 10, 22.0), (llm_x + 10, llm_y + 7.5)],
                  color=PURPLE_ACCENT, lw=1.4, label="Grounded Chunks", label_pt=(38, 22.0))

# Connect LLM Inference to Evaluator
draw_arrow(ax, (llm_x + 19, llm_y), (eval_engine_x - 20, eval_engine_y), color=ARROW_COLOR, lw=1.6, label="Student Submission")

# ==============================================================================
# DUAL FEEDBACK LOOPS (Cleanly routed through dedicated corridors)
# ==============================================================================
# FEEDBACK LOOP A: Real-Time Socratic Scaffolding Loop (Score < 70%)
# Evaluator -> Hint Agent (Routes cleanly through the dedicated channel at x = 66.5)
draw_corner_arrow(ax, [(eval_engine_x - 10, eval_engine_y + 7.5), (66.5, 25.5), (66.5, 83.5), (ag4_x, 83.5)],
                  color=AMBER_ACCENT, lw=2.2, label="LOOP A: Fail / Low Score -> 3-Tier Socratic Hint Decay", label_pt=(66.5, 54.0))

# FEEDBACK LOOP B: Macro Curriculum Progression Loop (Score >= 70%)
# Evaluator -> Student Repository & DAG Unlock
draw_corner_arrow(ax, [(eval_engine_x + 8, eval_engine_y + 7.5), (eval_engine_x + 8, 25.5), (repo_x, 25.5), (repo_x, repo_y - 8.25)],
                  color=GREEN_ACCENT, lw=2.2, label="LOOP B: Pass (>=70%) -> Update Mastery & Unlock Next DAG Node", label_pt=(81.0, 25.5))

# Output paths
os.makedirs(ROOT_DIR / "assets" / "screenshots", exist_ok=True)
os.makedirs(ROOT_DIR / "evaluation" / "plots", exist_ok=True)

out1 = str(ROOT_DIR / "assets" / "screenshots" / "comprehensive_methodology_architecture.png")
out2 = str(ROOT_DIR / "evaluation" / "plots" / "figure_comprehensive_methodology_architecture.png")

plt.tight_layout()
plt.savefig(out1, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.savefig(out2, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print(f"Generated successfully: {out1} and {out2}")
