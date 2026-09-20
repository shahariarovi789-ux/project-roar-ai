import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

# Canvas Setup - High Resolution Publication Grade
fig, ax = plt.subplots(figsize=(15, 16.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 105)
ax.set_aspect('equal')
ax.axis('off')

# Color palette: Academic Monochrome / Grayscale matching reference
BG_COLOR = "#ffffff"
DARK_CHARCOAL = "#212529"
MED_GRAY = "#495057"
LIGHT_GRAY = "#e9ecef"
BORDER_GRAY = "#ced4da"
WHITE = "#ffffff"
ARROW_COLOR = "#212529"
FONT_FAMILY = "Georgia"

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------
def draw_badge(ax, x, y, num):
    """Circular numbered badge with dark charcoal fill and crisp white number"""
    circle = patches.Circle((x, y), 2.2, facecolor=DARK_CHARCOAL, edgecolor="none", zorder=15)
    ax.add_patch(circle)
    ax.text(x, y - 0.1, str(num), color="white", fontsize=13, fontweight='bold',
            ha='center', va='center', zorder=16, fontfamily=FONT_FAMILY)

def draw_card(ax, x, y, w, h, bg_color=LIGHT_GRAY, border_color=BORDER_GRAY, corner_radius=1.8):
    """Rounded rectangular card container"""
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={corner_radius}",
                                  facecolor=bg_color, edgecolor=border_color, linewidth=1.5, zorder=3)
    ax.add_patch(rect)
    return rect

def draw_hexagon(ax, x, y, size, bg_color=DARK_CHARCOAL, border_color="none", linewidth=1.5):
    """Regular hexagon patch"""
    angles = np.linspace(0, 2*np.pi, 7)[:-1] + np.pi/6
    hx = x + size * np.cos(angles)
    hy = y + size * np.sin(angles)
    poly = patches.Polygon(np.column_stack([hx, hy]), closed=True,
                           facecolor=bg_color, edgecolor=border_color, linewidth=linewidth, zorder=3)
    ax.add_patch(poly)
    return poly

def draw_isometric_cube(ax, x, y, size, face_color="#ffffff", edge_color=DARK_CHARCOAL):
    """3D Isometric cube outline"""
    w = size
    h = size * 0.55
    d = size * 0.85
    # Top face
    top = patches.Polygon([[x, y + h], [x + w, y], [x, y - h], [x - w, y]],
                          closed=True, facecolor=face_color, edgecolor=edge_color, linewidth=1.5, zorder=3)
    # Left face
    left = patches.Polygon([[x - w, y], [x, y - h], [x, y - h - d], [x - w, y - d]],
                           closed=True, facecolor="#f8f9fa", edgecolor=edge_color, linewidth=1.5, zorder=3)
    # Right face
    right = patches.Polygon([[x + w, y], [x, y - h], [x, y - h - d], [x + w, y - d]],
                            closed=True, facecolor="#e9ecef", edgecolor=edge_color, linewidth=1.5, zorder=3)
    ax.add_patch(left)
    ax.add_patch(right)
    ax.add_patch(top)

# ----------------------------------------------------------------------
# 1. USER (Top-Left)
# ----------------------------------------------------------------------
user_x, user_y = 11, 89
user_circle = patches.Circle((user_x, user_y), 5.8, facecolor=DARK_CHARCOAL, edgecolor="none", zorder=3)
ax.add_patch(user_circle)

head = patches.Circle((user_x, user_y + 1.8), 1.8, facecolor=WHITE, zorder=4)
ax.add_patch(head)
body = patches.Polygon([[user_x - 3.5, user_y - 4.5], [user_x - 2.0, user_y - 0.7],
                        [user_x + 2.0, user_y - 0.7], [user_x + 3.5, user_y - 4.5]],
                       facecolor=WHITE, zorder=4)
ax.add_patch(body)

draw_badge(ax, user_x, user_y + 8.8, 1)
ax.text(user_x, user_y - 9.0, "USER", fontsize=14, fontweight='bold', ha='center', va='center',
        color=DARK_CHARCOAL, fontfamily=FONT_FAMILY)

# ----------------------------------------------------------------------
# 2. Basic info & Answering some questions (Top-Center)
# ----------------------------------------------------------------------
binfo_x, binfo_y = 43, 89
draw_card(ax, binfo_x, binfo_y, 11, 12, bg_color=LIGHT_GRAY, border_color=BORDER_GRAY)
draw_badge(ax, binfo_x, binfo_y + 8.8, 2)

doc = patches.Rectangle((binfo_x - 3.4, binfo_y - 3.2), 5.0, 7.0, facecolor=WHITE, edgecolor="#adb5bd", linewidth=1.2, zorder=4)
ax.add_patch(doc)
for i in range(4):
    ax.plot([binfo_x - 2.5, binfo_x + 0.6], [binfo_y + 2.2 - i*1.3, binfo_y + 2.2 - i*1.3], color="#ced4da", lw=2, zorder=5)

gear_bg = patches.Circle((binfo_x + 2.4, binfo_y - 2.2), 1.8, facecolor=WHITE, edgecolor="#adb5bd", linewidth=1.2, zorder=5)
ax.add_patch(gear_bg)
for angle in np.linspace(0, 2*np.pi, 9)[:-1]:
    gx = binfo_x + 2.4 + 1.8 * np.cos(angle)
    gy = binfo_y - 2.2 + 1.8 * np.sin(angle)
    ax.add_patch(patches.Circle((gx, gy), 0.35, facecolor="#adb5bd", zorder=6))
gear_hole = patches.Circle((binfo_x + 2.4, binfo_y - 2.2), 0.75, facecolor=LIGHT_GRAY, edgecolor="#adb5bd", linewidth=1, zorder=7)
ax.add_patch(gear_hole)

ax.text(binfo_x, binfo_y - 9.8, "Basic info &\nAnswering some\nquestions", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ----------------------------------------------------------------------
# 3. Starting Lesson (Top-Right)
# ----------------------------------------------------------------------
start_x, start_y = 75, 89
draw_card(ax, start_x, start_y, 11, 12, bg_color=DARK_CHARCOAL, border_color="none")
draw_badge(ax, start_x, start_y + 8.8, 3)

win = patches.Rectangle((start_x - 4.2, start_y - 3.8), 8.4, 7.6, facecolor="#2d3238", edgecolor=WHITE, linewidth=1.2, zorder=4)
ax.add_patch(win)
ax.plot([start_x - 4.2, start_x + 4.2], [start_y + 2.3, start_y + 2.3], color=WHITE, lw=1.2, zorder=5)
for i, bx in enumerate([-3.2, -2.2, -1.2]):
    ax.add_patch(patches.Circle((start_x + bx, start_y + 2.9), 0.35, facecolor=WHITE, zorder=6))
ax.text(start_x, start_y - 0.9, "</>", color=WHITE, fontsize=16, fontweight='bold', ha='center', va='center', zorder=5)

ax.text(start_x, start_y - 9.8, "Starting Lesson", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY)

# ----------------------------------------------------------------------
# User Interface (Center-Upper)
# ----------------------------------------------------------------------
ui_x, ui_y = 48, 70
ui_circle = patches.Circle((ui_x, ui_y), 5.8, facecolor="#b4bcc4", edgecolor="none", zorder=3)
ax.add_patch(ui_circle)

mon = patches.Rectangle((ui_x - 3.5, ui_y - 1.6), 5.2, 3.8, facecolor=WHITE, edgecolor=DARK_CHARCOAL, linewidth=1.2, zorder=4)
ax.add_patch(mon)
mon_screen = patches.Rectangle((ui_x - 3.1, ui_y - 1.2), 4.4, 3.0, facecolor="#dee2e6", zorder=5)
ax.add_patch(mon_screen)
stand = patches.Rectangle((ui_x - 1.2, ui_y - 2.8), 0.6, 1.2, facecolor=WHITE, edgecolor=DARK_CHARCOAL, linewidth=1.2, zorder=4)
ax.add_patch(stand)
base = patches.Rectangle((ui_x - 2.0, ui_y - 3.1), 2.2, 0.4, facecolor=WHITE, edgecolor=DARK_CHARCOAL, linewidth=1.2, zorder=4)
ax.add_patch(base)
tower = patches.Rectangle((ui_x + 2.1, ui_y - 2.8), 1.6, 4.8, facecolor=WHITE, edgecolor=DARK_CHARCOAL, linewidth=1.2, zorder=4)
ax.add_patch(tower)
ax.plot([ui_x + 2.4, ui_x + 3.4], [ui_y + 1.2, ui_y + 1.2], color=DARK_CHARCOAL, lw=1, zorder=5)
ax.add_patch(patches.Circle((ui_x + 2.9, ui_y - 1.8), 0.25, facecolor=DARK_CHARCOAL, zorder=5))

ax.text(ui_x, ui_y - 8.8, "User Interface", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY)

# ----------------------------------------------------------------------
# Student Data Repository (Middle-Left)
# ----------------------------------------------------------------------
repo_x, repo_y = 18, 64
draw_card(ax, repo_x, repo_y, 11, 12, bg_color=DARK_CHARCOAL, border_color="none")

for offset in [2.4, 0.4, -1.6]:
    cyl_side = patches.Rectangle((repo_x - 2.5, repo_y + offset - 1.0), 5.0, 1.0, facecolor=WHITE, edgecolor=WHITE, zorder=4)
    ax.add_patch(cyl_side)
    cyl_bot = patches.Ellipse((repo_x, repo_y + offset - 1.0), 5.0, 1.2, facecolor=WHITE, edgecolor=WHITE, zorder=4)
    ax.add_patch(cyl_bot)
    cyl_top = patches.Ellipse((repo_x, repo_y + offset), 5.0, 1.2, facecolor="#e9ecef", edgecolor="#adb5bd", linewidth=0.8, zorder=5)
    ax.add_patch(cyl_top)

s_badge = patches.Circle((repo_x - 2.4, repo_y - 2.8), 1.8, facecolor="#343a40", edgecolor=WHITE, linewidth=1.2, zorder=6)
ax.add_patch(s_badge)
for i, sx in enumerate([-3.1, -2.4, -1.7]):
    ax.plot([repo_x + sx, repo_x + sx], [repo_y - 3.8, repo_y - 1.8], color=WHITE, lw=1, zorder=7)
    node_y = repo_y - 3.2 if i==0 else (repo_y - 2.4 if i==1 else repo_y - 2.8)
    ax.add_patch(patches.Circle((repo_x + sx, node_y), 0.35, facecolor=WHITE, zorder=8))

ax.text(repo_x, repo_y - 9.8, "Student Data\nRepository", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ----------------------------------------------------------------------
# Project ROAR: Our AI Agent (Center)
# ----------------------------------------------------------------------
agent_x, agent_y = 48, 49
draw_hexagon(ax, agent_x, agent_y, 6.4, bg_color="#ffffff", border_color=DARK_CHARCOAL, linewidth=1.8)

# Isometric 3D frame wireframe
ax.plot([agent_x, agent_x], [agent_y + 6.4, agent_y + 2.6], color="#ced4da", lw=1.2, zorder=3)
ax.plot([agent_x - 5.54, agent_x], [agent_y - 3.2, agent_y - 0.5], color="#ced4da", lw=1.2, zorder=3)
ax.plot([agent_x + 5.54, agent_x], [agent_y - 3.2, agent_y - 0.5], color="#ced4da", lw=1.2, zorder=3)

# Professional Tutor Avatar
t_head = patches.Circle((agent_x, agent_y + 1.8), 1.7, facecolor="#ffffff", edgecolor=DARK_CHARCOAL, linewidth=1.5, zorder=4)
ax.add_patch(t_head)
hair = patches.Arc((agent_x, agent_y + 2.4), 3.2, 1.8, theta1=0, theta2=180, edgecolor=DARK_CHARCOAL, linewidth=2, zorder=5)
ax.add_patch(hair)
# Sleek modern glasses
g1 = patches.FancyBboxPatch((agent_x - 1.35, agent_y + 1.3), 1.1, 0.9, boxstyle="round,pad=0,rounding_size=0.3",
                            facecolor="none", edgecolor=DARK_CHARCOAL, linewidth=1.4, zorder=6)
g2 = patches.FancyBboxPatch((agent_x + 0.25, agent_y + 1.3), 1.1, 0.9, boxstyle="round,pad=0,rounding_size=0.3",
                            facecolor="none", edgecolor=DARK_CHARCOAL, linewidth=1.4, zorder=6)
ax.add_patch(g1); ax.add_patch(g2)
ax.plot([agent_x - 0.25, agent_x + 0.25], [agent_y + 1.75, agent_y + 1.75], color=DARK_CHARCOAL, lw=1.4, zorder=6)

shoulders = patches.Polygon([[agent_x - 3.2, agent_y - 3.2], [agent_x - 1.5, agent_y - 0.5],
                             [agent_x + 1.5, agent_y - 0.5], [agent_x + 3.2, agent_y - 3.2]],
                            closed=True, facecolor="#f8f9fa", edgecolor=DARK_CHARCOAL, linewidth=1.5, zorder=4)
ax.add_patch(shoulders)
tie = patches.Polygon([[agent_x - 0.5, agent_y - 0.5], [agent_x + 0.5, agent_y - 0.5],
                       [agent_x + 0.3, agent_y - 2.8], [agent_x, agent_y - 3.4], [agent_x - 0.3, agent_y - 2.8]],
                      closed=True, facecolor=DARK_CHARCOAL, zorder=5)
ax.add_patch(tie)

ax.text(agent_x, agent_y - 9.4, "Project ROAR:\nOur AI Agent", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ----------------------------------------------------------------------
# Generative AI (Center-Lower)
# ----------------------------------------------------------------------
gen_x, gen_y = 48, 33
draw_isometric_cube(ax, gen_x, gen_y, 4.4, face_color="#ffffff", edge_color=DARK_CHARCOAL)

nn_nodes = [[gen_x - 2.2, gen_y - 0.2], [gen_x, gen_y + 1.4], [gen_x + 2.2, gen_y - 0.2],
            [gen_x - 1.4, gen_y - 1.8], [gen_x + 1.4, gen_y - 1.8]]
for p1 in nn_nodes:
    for p2 in nn_nodes:
        if p1 != p2:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#adb5bd", lw=1.0, zorder=5)
for pt in nn_nodes:
    ax.add_patch(patches.Circle((pt[0], pt[1]), 0.45, facecolor=DARK_CHARCOAL, edgecolor=WHITE, linewidth=0.8, zorder=6))

ax.text(gen_x, gen_y - 8.2, "Generative\nAI", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ----------------------------------------------------------------------
# 4. Adapting Learning and Pace (Middle-Right)
# ----------------------------------------------------------------------
adapt_x, adapt_y = 90, 40
draw_hexagon(ax, adapt_x, adapt_y, 5.8, bg_color=DARK_CHARCOAL, border_color="none")
draw_badge(ax, adapt_x + 6.6, adapt_y, 4)

a_head = patches.Circle((adapt_x - 1.5, adapt_y + 1.4), 1.3, facecolor=WHITE, zorder=4)
ax.add_patch(a_head)
a_body = patches.Polygon([[adapt_x - 3.4, adapt_y - 2.8], [adapt_x - 2.2, adapt_y - 0.4],
                          [adapt_x - 0.6, adapt_y - 0.4], [adapt_x + 0.6, adapt_y - 2.8]],
                         facecolor=WHITE, zorder=4)
ax.add_patch(a_body)
a_gear = patches.Circle((adapt_x + 2.0, adapt_y + 0.6), 1.6, facecolor=WHITE, edgecolor=DARK_CHARCOAL, linewidth=1.2, zorder=5)
ax.add_patch(a_gear)
for angle in np.linspace(0, 2*np.pi, 9)[:-1]:
    gx = adapt_x + 2.0 + 1.6 * np.cos(angle)
    gy = adapt_y + 0.6 + 1.6 * np.sin(angle)
    ax.add_patch(patches.Circle((gx, gy), 0.35, facecolor=WHITE, zorder=6))
a_inner = patches.Circle((adapt_x + 2.0, adapt_y + 0.6), 0.7, facecolor=DARK_CHARCOAL, zorder=7)
ax.add_patch(a_inner)

ax.text(adapt_x, adapt_y - 9.5, "Adapting\nLearning and\nPace", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ----------------------------------------------------------------------
# 5. Continuous Feedback & Adjustment (Bottom-Right)
# ----------------------------------------------------------------------
fb_x, fb_y = 72, 21
draw_card(ax, fb_x, fb_y, 11, 12, bg_color=LIGHT_GRAY, border_color=BORDER_GRAY)
draw_badge(ax, fb_x, fb_y + 8.8, 5)

fb_mon = patches.Rectangle((fb_x - 3.8, fb_y - 2.5), 7.6, 5.2, facecolor=WHITE, edgecolor="#adb5bd", linewidth=1.2, zorder=4)
ax.add_patch(fb_mon)
pie = patches.Wedge((fb_x - 1.4, fb_y + 0.4), 1.5, 30, 300, facecolor="#adb5bd", edgecolor=WHITE, linewidth=1, zorder=5)
ax.add_patch(pie)
for i, bar_w in enumerate([2.2, 1.6, 2.6]):
    ax.plot([fb_x + 0.6, fb_x + 0.6 + bar_w], [fb_y + 1.4 - i*1.0, fb_y + 1.4 - i*1.0], color="#adb5bd", lw=2.5, zorder=5)

ax.text(fb_x, fb_y - 9.8, "Continuous\nFeedback &\nAdjustment", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ----------------------------------------------------------------------
# 6. Content Generation (Bottom-Center)
# ----------------------------------------------------------------------
cg_x, cg_y = 50, 13
draw_card(ax, cg_x, cg_y, 11, 12, bg_color=LIGHT_GRAY, border_color=BORDER_GRAY)
draw_badge(ax, cg_x + 6.6, cg_y, 6)

cg_nodes = [[cg_x - 2.4, cg_y + 1.2], [cg_x - 0.8, cg_y + 2.5], [cg_x + 0.6, cg_y + 1.2],
            [cg_x - 2.0, cg_y - 0.8], [cg_x - 0.4, cg_y - 1.6]]
for p1 in cg_nodes:
    for p2 in cg_nodes:
        if p1 != p2:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#adb5bd", lw=1.0, zorder=4)
for pt in cg_nodes:
    ax.add_patch(patches.Circle((pt[0], pt[1]), 0.45, facecolor="#6c757d", edgecolor=WHITE, linewidth=0.6, zorder=5))
cg_gear = patches.Circle((cg_x + 2.2, cg_y - 1.0), 1.6, facecolor=WHITE, edgecolor="#adb5bd", linewidth=1.2, zorder=5)
ax.add_patch(cg_gear)
for angle in np.linspace(0, 2*np.pi, 9)[:-1]:
    gx = cg_x + 2.2 + 1.6 * np.cos(angle)
    gy = cg_y - 1.0 + 1.6 * np.sin(angle)
    ax.add_patch(patches.Circle((gx, gy), 0.35, facecolor="#adb5bd", zorder=6))
cg_hole = patches.Circle((cg_x + 2.2, cg_y - 1.0), 0.7, facecolor=LIGHT_GRAY, edgecolor="#adb5bd", linewidth=0.8, zorder=7)
ax.add_patch(cg_hole)

ax.text(cg_x, cg_y - 9.8, "Content\nGeneration", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ----------------------------------------------------------------------
# 7. Evaluate Performance & Learning Outcome (Bottom-Left-Center)
# ----------------------------------------------------------------------
eval_x, eval_y = 28, 21
draw_card(ax, eval_x, eval_y, 11, 12, bg_color=LIGHT_GRAY, border_color=BORDER_GRAY)
draw_badge(ax, eval_x, eval_y + 8.8, 7)

e_doc = patches.Rectangle((eval_x - 3.4, eval_y - 3.2), 5.0, 7.0, facecolor=WHITE, edgecolor="#adb5bd", linewidth=1.2, zorder=4)
ax.add_patch(e_doc)
for i in range(3):
    ax.plot([eval_x - 2.5, eval_x + 0.6], [eval_y + 2.2 - i*1.3, eval_y + 2.2 - i*1.3], color="#ced4da", lw=2, zorder=5)
e_badge = patches.Circle((eval_x + 2.2, eval_y - 2.0), 1.8, facecolor=WHITE, edgecolor="#adb5bd", linewidth=1.2, zorder=5)
ax.add_patch(e_badge)
e_tick = patches.Polygon([[eval_x + 1.3, eval_y - 2.0], [eval_x + 1.9, eval_y - 2.6], [eval_x + 3.1, eval_y - 1.4]],
                         closed=False, fill=False, edgecolor="#495057", linewidth=2.4, zorder=6)
ax.add_patch(e_tick)

# Label placed cleanly below
ax.text(eval_x, eval_y - 10.6, "Evaluate\nPerformance &\nLearning\nOutcome", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ----------------------------------------------------------------------
# 8. Update Student Score (Bottom-Left)
# ----------------------------------------------------------------------
score_x, score_y = 8, 21
draw_card(ax, score_x, score_y, 11, 12, bg_color=LIGHT_GRAY, border_color=BORDER_GRAY)
draw_badge(ax, score_x, score_y + 8.8, 8)

sc_circle = patches.Circle((score_x, score_y), 3.8, facecolor=WHITE, edgecolor="#ced4da", linewidth=1.6, zorder=4)
ax.add_patch(sc_circle)
sc_tick = patches.Polygon([[score_x - 2.0, score_y - 0.2], [score_x - 0.6, score_y - 2.2], [score_x + 2.4, score_y + 1.8]],
                          closed=False, fill=False, edgecolor="#adb5bd", linewidth=4.0, zorder=5)
ax.add_patch(sc_tick)

ax.text(score_x, score_y - 9.8, "Update Student\nScore", fontsize=12, fontweight='bold',
        ha='center', va='center', color=DARK_CHARCOAL, fontfamily=FONT_FAMILY, linespacing=1.2)

# ==============================================================================
# CONNECTING ARROWS & EXACT ROUTED PATHS (Matching Reference Perfectly)
# ==============================================================================
arrow_style = dict(arrowstyle="-|>", mutation_scale=16, color=ARROW_COLOR, lw=1.8, zorder=2)

def draw_arrow(ax, x1, y1, x2, y2):
    arr = patches.FancyArrowPatch((x1, y1), (x2, y2), **arrow_style)
    ax.add_patch(arr)

def draw_corner_arrow(ax, points):
    path = Path(points)
    arr = patches.FancyArrowPatch(path=path, **arrow_style)
    ax.add_patch(arr)

def draw_curve_arrow(ax, p1, p2, rad=0.2):
    arr = patches.FancyArrowPatch(p1, p2, connectionstyle=f"arc3,rad={rad}", **arrow_style)
    ax.add_patch(arr)

# 1. USER -> (2) Basic info
draw_arrow(ax, user_x + 5.8, user_y, binfo_x - 5.5, binfo_y)

# 2. USER -> User Interface
draw_corner_arrow(ax, [(user_x + 5.6, user_y - 1.8), (28, user_y - 1.8), (28, ui_y + 1.5), (ui_x - 5.8, ui_y + 1.5)])

# 3. (2) Basic info -> Student Data Repository (Leaves left of card to avoid text)
draw_corner_arrow(ax, [(binfo_x - 5.5, binfo_y - 3.0), (33, binfo_y - 3.0), (33, 79), (repo_x, 79), (repo_x, repo_y + 6.0)])

# 4. (2) Basic info -> (3) Starting Lesson
draw_arrow(ax, binfo_x + 5.5, binfo_y, start_x - 5.5, start_y)

# 5. (3) Starting Lesson -> User Interface
draw_corner_arrow(ax, [(start_x + 5.5, start_y), (87, start_y), (87, 76), (ui_x + 5.5, 76), (ui_x + 2.5, ui_y + 5.2)])

# 6. User Interface <-> Project ROAR (Bi-directional curved arrows)
draw_curve_arrow(ax, (ui_x - 5.2, ui_y - 1.8), (agent_x - 4.8, agent_y + 3.0), rad=0.48)
draw_curve_arrow(ax, (agent_x + 4.8, agent_y + 3.0), (ui_x + 5.2, ui_y - 1.8), rad=0.48)

# 7. Student Data Repository -> Project ROAR
draw_curve_arrow(ax, (repo_x + 5.5, repo_y), (agent_x - 5.2, agent_y + 4.2), rad=-0.28)

# 8. Project ROAR -> Generative AI
draw_corner_arrow(ax, [(agent_x - 5.5, agent_y - 2.0), (gen_x - 6.5, agent_y - 2.0), (gen_x - 6.5, gen_y + 2.2), (gen_x - 4.2, gen_y + 2.2)])

# 9. Project ROAR -> (4) Adapting Learning and Pace
draw_corner_arrow(ax, [(agent_x + 6.4, agent_y - 1.5), (adapt_x, agent_y - 1.5), (adapt_x, adapt_y + 5.8)])

# 10. Generative AI -> (6) Content Generation
draw_corner_arrow(ax, [(gen_x + 4.2, gen_y - 1.8), (gen_x + 6.8, gen_y - 1.8), (gen_x + 6.8, cg_y + 8.5), (cg_x, cg_y + 8.5), (cg_x, cg_y + 6.0)])

# 11. (4) Adapting Learning and Pace -> (5) Continuous Feedback
draw_corner_arrow(ax, [(adapt_x - 5.8, adapt_y), (fb_x + 9.5, adapt_y), (fb_x + 9.5, fb_y + 2.0), (fb_x + 5.5, fb_y + 2.0)])

# 12. (5) Continuous Feedback -> (6) Content Generation
draw_corner_arrow(ax, [(fb_x - 5.5, fb_y), (cg_x + 13.0, fb_y), (cg_x + 13.0, cg_y), (cg_x + 5.5, cg_y)])

# 13. (6) Content Generation -> (7) Evaluate Performance
draw_corner_arrow(ax, [(cg_x - 5.5, cg_y + 2.5), (38, cg_y + 2.5), (38, eval_y + 2.0), (eval_x + 5.5, eval_y + 2.0)])

# 14. (7) Evaluate Performance -> (8) Update Student Score
draw_arrow(ax, eval_x - 5.5, eval_y, score_x + 5.5, score_y)

# 15. (7) Evaluate Performance -> (5) Continuous Feedback (Adaptive Hinting Loop)
# Starts below the text of (7) at y = 5.0, goes down to y = 1.0, right across to x = 65.0, up into card (5) at bottom-left
draw_corner_arrow(ax, [(eval_x, 5.0), (eval_x, 1.0), (65.0, 1.0), (65.0, fb_y - 6.0)])

# 16. (8) Update Student Score -> Student Data Repository (Mastery Loop)
draw_corner_arrow(ax, [(score_x - 5.5, score_y), (1.5, score_y), (1.5, repo_y), (repo_x - 5.5, repo_y)])

# Output paths
os.makedirs("/Users/a/thesis-prompt-tutor/assets/screenshots", exist_ok=True)
os.makedirs("/Users/a/thesis-prompt-tutor/evaluation/plots", exist_ok=True)

out1 = "/Users/a/thesis-prompt-tutor/assets/screenshots/methodology_flow_diagram.png"
out2 = "/Users/a/thesis-prompt-tutor/evaluation/plots/figure_methodology_flow_diagram.png"

plt.tight_layout()
plt.savefig(out1, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.savefig(out2, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print(f"Generated successfully: {out1} and {out2}")
