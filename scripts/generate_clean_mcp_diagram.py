#!/usr/bin/env python3
"""
Generate a high-visibility, clean, large-font MCP Architecture Diagram
specifically engineered for IEEE two-column paper single-column placement.
Typography is large (11pt to 16pt bold), high contrast, with clean whitespace.
"""

from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_PATH = Path("/Users/a/thesis-prompt-tutor/ieee_paper/figures/fig3_mcp_orchestration.png")

# Dimensions optimized for single-column width in IEEE: 7.0 x 5.8 inches at 300 DPI
fig, ax = plt.subplots(figsize=(7.0, 5.8), dpi=300, facecolor='#ffffff')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Colors
BG_WHITE    = "#ffffff"
NAVY_DARK   = "#0f172a"
SLATE_BORDER= "#64748b"
BLUE_BG     = "#f0f9ff"
BLUE_BORDER = "#0284c7"
ORANGE_BG   = "#fff7ed"
ORANGE_BORDER="#ea580c"
GREEN_BG    = "#ecfdf5"
GREEN_BORDER= "#059669"
PURPLE_BG   = "#faf5ff"
PURPLE_BORDER="#7c3aed"

def draw_box(ax, x, y, w, h, bg, border, radius=2.0, lw=2.0):
    rect = patches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=bg, edgecolor=border, linewidth=lw, zorder=3
    )
    ax.add_patch(rect)

# 1. Top Section: Cognitive Agents Layer
draw_box(ax, 50, 84, 94, 24, BLUE_BG, BLUE_BORDER, radius=2.5, lw=2.2)
ax.text(50, 92, "COGNITIVE AGENTS (MCP CLIENTS)", ha='center', va='center',
        fontsize=12, fontweight='bold', color='#0369a1')

# 3 Agent Cards
agents = [
    ("Orchestrator Agent", "FSM Supervisory Control\n& Task Scheduling"),
    ("Socratic Coach", "Scaffolded Instruction\n& 3-Tier Guidance"),
    ("Evaluator Judge", "Dual-Stream Grading\n& Rubric Verification")
]
xs = [20, 50, 80]
for (name, desc), x in zip(agents, xs):
    draw_box(ax, x, 78, 26, 12, "#ffffff", "#0284c7", radius=1.5, lw=1.5)
    ax.text(x, 81.5, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color=NAVY_DARK)
    ax.text(x, 76.0, desc, ha='center', va='center', fontsize=8.0, color="#334155")

# 2. Middle Section: Model Context Protocol (MCP) Bus
draw_box(ax, 50, 50, 94, 22, ORANGE_BG, ORANGE_BORDER, radius=2.5, lw=2.5)
ax.text(50, 57.5, "MODEL CONTEXT PROTOCOL (MCP) BUS", ha='center', va='center',
        fontsize=12, fontweight='bold', color='#c2410c')

# Protocol Capabilities
draw_box(ax, 28, 47, 44, 9, "#ffffff", ORANGE_BORDER, radius=1.5, lw=1.4)
ax.text(28, 47, "Strict JSON-RPC 2.0 Contracts\n(100% Schema Validation)",
        ha='center', va='center', fontsize=8.5, fontweight='bold', color='#9a3412')

draw_box(ax, 72, 47, 40, 9, "#ffffff", ORANGE_BORDER, radius=1.5, lw=1.4)
ax.text(72, 47, "Immutable URI State Bus\n(Zero Cross-Agent Drift)",
        ha='center', va='center', fontsize=8.5, fontweight='bold', color='#9a3412')

# 3. Bottom Section: Decoupled Resources & Tools Layer
draw_box(ax, 50, 16, 94, 24, GREEN_BG, GREEN_BORDER, radius=2.5, lw=2.2)
ax.text(50, 24, "DECOUPLED RESOURCES & TOOLS (MCP SERVERS)", ha='center', va='center',
        fontsize=12, fontweight='bold', color='#047857')

# 3 Resource Cards
resources = [
    ("Knowledge Graph", "36-Node Curriculum DAG\nTopological Invariant"),
    ("Vector RAG Store", "ChromaDB Embeddings\n14.2 ms Retrieval Latency"),
    ("Execution Engine", "NF4 Local Model Inference\n& Deterministic Rubrics")
]
for (name, desc), x in zip(resources, xs):
    draw_box(ax, x, 10, 26, 12, "#ffffff", GREEN_BORDER, radius=1.5, lw=1.5)
    ax.text(x, 13.5, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color=NAVY_DARK)
    ax.text(x, 8.0, desc, ha='center', va='center', fontsize=8.0, color="#334155")

# Arrows between Layers with Clear Labels
# Top to Middle
ax.annotate("", xy=(50, 61), xytext=(50, 72),
            arrowprops=dict(arrowstyle="<->", color="#0284c7", lw=2.2))
ax.text(52, 66.5, "JSON-RPC Tool Invocations & Responses", ha='left', va='center',
        fontsize=8.5, fontweight='bold', color="#0369a1")

# Middle to Bottom
ax.annotate("", xy=(50, 28), xytext=(50, 39),
            arrowprops=dict(arrowstyle="<->", color="#ea580c", lw=2.2))
ax.text(52, 33.5, "Standardized Tool Calls & State Synchronization", ha='left', va='center',
        fontsize=8.5, fontweight='bold', color="#c2410c")

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300)
plt.close()
print(f"✓ High-visibility diagram successfully written to {OUT_PATH}")
