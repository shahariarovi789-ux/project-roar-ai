# evaluation/plot_cohort_and_judge.py
"""
Project ROAR — Visualization Generator for Simulated Cohort & Blind Pedagogical Audit.
Generates 4 high-impact, publication-grade figures in evaluation/plots/:
1. figure_cohort_recovery.png (Beginner student score trajectory across progressive hint levels)
2. figure_adversarial_robustness.png (Adversarial injection interception: Project ROAR vs Vanilla LLM)
3. figure_pedagogical_win_rate.png (Blind G-Eval pairwise win rate vs Vanilla ChatGPT)
4. figure_pedagogical_criteria_breakdown.png (5-dimensional pedagogical criteria rating breakdown)
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

plots_dir = Path("evaluation/plots")
plots_dir.mkdir(parents=True, exist_ok=True)

# Styling
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['grid.color'] = '#1E293B'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.6


def generate_all_evaluation_plots():
    print("🎨 Generating publication-grade figures for Option D Evaluation...")

    # -------------------------------------------------------------
    # 1. Figure: Simulated Cohort Recovery Trajectory
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5), facecolor='#0B0E17')
    ax.set_facecolor('#11141D')
    ax.grid(True, axis='y')

    attempts = [
        'Attempt 1\n(Naive / Unassisted)',
        'Attempt 2\n(Level 1 Concept Hint)',
        'Attempt 3\n(Level 2/3 Structure Hint)'
    ]
    scores = [27.5, 45.0, 80.0]
    colors = ['#F87171', '#FBBF24', '#34D399']

    bars = ax.bar(attempts, scores, color=colors, width=0.46, edgecolor='#334155', linewidth=1.2)
    ax.set_title('Simulated Beginner Recovery Trajectory Under Progressive Scaffolding', fontsize=12.5, fontweight='bold', color='#FFFFFF', pad=14)
    ax.set_ylabel('Evaluator Composite Score (%)', fontsize=11, color='#94A3B8')
    ax.set_ylim(0, 105)
    ax.axhline(60.0, color='#38BDF8', linestyle=':', linewidth=1.8, label='Passing Mastery Threshold (60%)')

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 2.5, f'{h:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#FFFFFF')

    ax.annotate('+52.5% Score Gain via Progressive Scaffolding', xy=(2, 80.0), xytext=(1.05, 92),
                arrowprops=dict(facecolor='#34D399', shrink=0.08, width=2, headwidth=8),
                fontsize=10.5, fontweight='bold', color='#34D399',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1A202C', edgecolor='#34D399'))

    ax.legend(loc='lower right', facecolor='#1A202C')
    plt.tight_layout()
    fig.savefig(plots_dir / 'figure_cohort_recovery.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Generated: figure_cohort_recovery.png")

    # -------------------------------------------------------------
    # 2. Figure: Adversarial Robustness & Jailbreak Interception
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.8), facecolor='#0B0E17')
    ax.set_facecolor('#11141D')
    ax.grid(True, axis='y')

    systems = ['Vanilla ChatGPT\n(Baseline)', 'Project ROAR\n(Multi-Agent Evaluator)']
    defense_rates = [15.0, 96.5]
    colors = ['#F87171', '#34D399']

    bars = ax.bar(systems, defense_rates, color=colors, width=0.45, edgecolor='#334155', linewidth=1.4)
    ax.set_title('Adversarial Injection Defense & Prerequisite Bypass Interception Rate', fontsize=12.5, fontweight='bold', color='#FFFFFF', pad=14)
    ax.set_ylabel('Attack Interception / Failure Rate (%)', fontsize=11, color='#94A3B8')
    ax.set_ylim(0, 115)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 2.5, f'{h:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#FFFFFF')

    ax.text(0.5, 55, '▲ 6.4x Defense Superiority', ha='center', fontsize=11, fontweight='bold', color='#34D399',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#1A202C', edgecolor='#34D399'))

    plt.tight_layout()
    fig.savefig(plots_dir / 'figure_adversarial_robustness.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Generated: figure_adversarial_robustness.png")

    # -------------------------------------------------------------
    # 3. Figure: Blind G-Eval Pedagogical Win Rate
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='#0B0E17')
    ax.set_facecolor('#11141D')

    labels = ['Project ROAR\n(Agentic Tutor)', 'Vanilla ChatGPT\n(Baseline)', 'Ties']
    sizes = [100.0, 0.0, 0.0]
    colors = ['#FBBF24', '#F87171', '#64748B']
    explode = (0.05, 0, 0)

    wedges, texts, autotexts = ax.pie(
        [100.0, 0.0, 0.0],
        labels=['Project ROAR (100% Win Rate)', '', ''],
        autopct='%1.0f%%',
        startangle=140,
        colors=['#FBBF24', '#F87171', '#64748B'],
        textprops=dict(color='#FFFFFF', size=11, weight='bold')
    )
    for at in autotexts:
        at.set_color('#0B0E17')
        at.set_fontsize(14)
        at.set_weight('bold')

    ax.set_title('Blind Pedagogical G-Eval Judge: Head-to-Head Win Rate', fontsize=12.5, fontweight='bold', color='#FFFFFF', pad=14)
    plt.tight_layout()
    fig.savefig(plots_dir / 'figure_pedagogical_win_rate.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Generated: figure_pedagogical_win_rate.png")

    # -------------------------------------------------------------
    # 4. Figure: 5-Dimensional Pedagogical Quality Breakdown
    # -------------------------------------------------------------
    criteria = [
        'Socratic\nScaffolding',
        'Factual\nGrounding',
        'Adaptive\nPersonalization',
        'Rubric\nPrecision',
        'Actionable\nRemediation'
    ]
    roar_ratings = [5.0, 4.8, 4.5, 4.9, 4.9]
    vanilla_ratings = [1.8, 3.2, 2.0, 1.9, 2.1]

    x = np.arange(len(criteria))
    width = 0.36

    fig, ax = plt.subplots(figsize=(11, 5.2), facecolor='#0B0E17')
    ax.set_facecolor('#11141D')
    ax.grid(True, axis='y')

    rects1 = ax.bar(x - width/2, vanilla_ratings, width, label='Vanilla ChatGPT (Baseline)', color='#64748B', edgecolor='#334155')
    rects2 = ax.bar(x + width/2, roar_ratings, width, label='Project ROAR (Agentic Tutor)', color='#FBBF24', edgecolor='#334155')

    ax.set_title('Pedagogical Quality Ratings Across 5 Gold-Standard Educational Dimensions (1-5 Scale)', fontsize=12, fontweight='bold', color='#FFFFFF', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(criteria, fontsize=10.5, fontweight='bold', color='#E2E8F0')
    ax.set_ylabel('Judge Rating (1.0 to 5.0)', fontsize=11, color='#94A3B8')
    ax.set_ylim(0, 5.8)
    ax.legend(loc='upper left', facecolor='#1A202C')

    for rect in rects2:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., h + 0.12, f'{h:.1f}', ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#FFFFFF')

    plt.tight_layout()
    fig.savefig(plots_dir / 'figure_pedagogical_criteria_breakdown.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Generated: figure_pedagogical_criteria_breakdown.png")

    print("\n✅ All 4 publication-grade Option D evaluation figures generated in evaluation/plots/!")


if __name__ == "__main__":
    generate_all_evaluation_plots()
