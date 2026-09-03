# backend/prompt_templates.py
"""
Topic-Grounded Prompt Templates for the Adaptive Tutoring System.
Guarantees 100% curriculum alignment, clear pedagogical progression, and calibrated length:
- Tier 1 (Foundational / Beginner, Weight 1.0 - 1.5): Ultra-concise, bite-sized (150-220 words, 1 min read).
- Tier 2 (Intermediate / Applied, Weight 1.8 - 2.8): Structured, practical blueprints (280-380 words, 2-3 min read).
- Tier 3 (Advanced / Expert, Weight 3.0 - 4.0): In-depth architectural analysis & defense (400-500 words, 3-4 min read).
"""

from typing import Dict, Any, List


TOPIC_SPECIFIC_GUIDES = {
    "node_01": {
        "core_topic": "Introduction to Prompt Engineering",
        "pedagogical_focus": "Explain what a prompt is, what prompt engineering is, and how giving clear instructions guides the AI to produce accurate answers instead of generic text.",
        "flawed_example": "Explain science.",
        "fortified_example": "You are a friendly science teacher. Explain the greenhouse effect in exactly 2 simple sentences using a glass greenhouse analogy.",
        "why_it_works": "Assigns a clear persona, an exact length constraint (2 sentences), and an intuitive analogy."
    },
    "node_02": {
        "core_topic": "Foundations of Prompt Engineering",
        "pedagogical_focus": "Explain the 4 core components of an effective prompt: 1) Instruction, 2) Context, 3) Input Data, and 4) Output Format.",
        "flawed_example": "Fix this: 'our sales were 50 units'.",
        "fortified_example": "You are a Communications Specialist. Rewrite the following update into 1 executive bullet point.\n\nInput: 'our sales were 50 units'\nOutput: Professional 1-line bullet point.",
        "why_it_works": "Separates the instruction from input data and defines the exact format."
    },
    "node_03": {
        "core_topic": "LLM Output Length & Token Management",
        "pedagogical_focus": "Explain token limits, max_tokens, and how to enforce exact length constraints (e.g. word or bullet limits).",
        "flawed_example": "Summarize this report briefly.",
        "fortified_example": "Summarize the key findings in strictly under 50 words using exactly 2 bullet points.",
        "why_it_works": "Replaces vague words like 'briefly' with strict quantitative numbers (50 words, 2 bullets)."
    }
}


def get_lesson_prompt(
    node_id: str,
    topic_path: str,
    topic_description: str,
    key_concepts: List[str],
    depth: int,
    difficulty_tier: int,
    rag_context: str,
    prefers_examples: bool,
    prefers_steps: bool,
    prefers_detailed: bool,
    prior_experience: str,
    target_domain: str = "Modern AI Applications",
    fail_streak: int = 0
) -> str:
    concepts_str = ", ".join(key_concepts) if key_concepts else "Core prompt engineering principles"

    # Specific topic override if available
    topic_guide = TOPIC_SPECIFIC_GUIDES.get(node_id)
    topic_focus = topic_guide["pedagogical_focus"] if topic_guide else f"Teach the specific concepts: {topic_description} ({concepts_str})."

    context_block = f"\n### Grounding Knowledge Base (Domain Corpus):\n{rag_context}\n" if rag_context else ""

    scaffolding_block = ""
    if fail_streak > 0:
        scaffolding_block = (
            f"\n> [!NOTE]\n"
            f"> **Scaffolding Active (Retry #{fail_streak})**: The student previously struggled with this topic.\n"
            f"> Simplify the explanation, provide a beginner-friendly breakdown, and highlight the exact mistake to avoid."
        )

    # =========================================================================
    # TIER 1: FOUNDATIONAL & EASY TOPICS (Strictly 150 - 220 words, 1-2 min read)
    # Never overload introductory topics with multi-section enterprise tables!
    # =========================================================================
    if difficulty_tier == 1:
        return f"""You are a friendly, encouraging AI Prompt Engineering Tutor.
Author an **ULTRA-CONCISE, BITE-SIZED Study Note** (Strictly 150–220 words total, fast to read in under 1.5 minutes).

Target Topic: {topic_path}
Topic Focus: {topic_focus}
Core Concepts: {concepts_str}
Learner Level: Beginner / Foundational
{context_block}
{scaffolding_block}

### MANDATORY BITE-SIZED STRUCTURE:

# 📘 Quick Guide: {topic_path}

## 1. 💡 The Core Idea (In 2 Sentences)
- [2 clear, simple sentences explaining what {topic_path} is and why it matters].

## 2. 🔬 Practical Example (Before & After)
```markdown
# ❌ Flawed (Vague Prompt)
{topic_guide['flawed_example'] if topic_guide else '[1-line vague prompt]'}

# ✅ Fortified (Engineered Prompt)
{topic_guide['fortified_example'] if topic_guide else '[2-line structured prompt with role and constraints]'}
```
- **Why it works**: [1 sentence explaining the key prompt improvement].

## 3. ⚡ 3 Golden Rules
1. **Be Specific**: Always state the exact goal and role.
2. **Set Constraints**: Specify format, length, or style.
3. **Provide Context**: Give the model the necessary background data.

CRITICAL: Keep the entire response under 220 words. No long essays, no huge comparison tables. Format in clean GitHub Markdown.
"""

    # =========================================================================
    # TIER 2: INTERMEDIATE & APPLIED (280 - 360 words, 2-3 min read)
    # =========================================================================
    elif difficulty_tier == 2:
        return f"""You are an expert AI Prompt Engineering Instructor.
Author a **Clear, Applied Study Guide** (~280–360 words, 2-3 minute read) for: '{topic_path}'.

Target Topic: {topic_path}
Topic Description: {topic_description}
Key Concepts: {concepts_str}
Pedagogical Objective: {topic_focus}
Difficulty Tier: Tier 2 (Intermediate)
{context_block}
{scaffolding_block}

### MANDATORY STRUCTURE:

# 📘 Study Notes: {topic_path}

## 1. 🎯 Purpose & Mechanics
- [2-3 sentences explaining how {topic_path} steers LLM attention and output quality].
- Core concepts covered: {concepts_str}.

## 2. 📋 Applied Prompt Blueprint
```markdown
# [SYSTEM ROLE & CONTEXT]
...
# [INPUT & DELIMITERS]
...
# [OUTPUT FORMAT]
...
```
- **Key Takeaway**: [2 concise bullets on why this structure prevents drift and hallucinations].

## 3. 🛠️ 3 Practical Implementation Guidelines
1. **Rule 1**: [Practical guideline for {topic_path}]
2. **Rule 2**: [Delimiters or syntax rule]
3. **Rule 3**: [Output schema control]

Keep output strictly under 360 words with crisp GitHub Markdown.
"""

    # =========================================================================
    # TIER 3: ADVANCED & EXPERT (380 - 460 words, 3-4 min read)
    # =========================================================================
    else:
        return f"""You are a Principal AI Architect and Research Engineer.
Author an **Advanced Production Study Guide** (~380–460 words) for: '{topic_path}'.

Target Topic: {topic_path}
Topic Syllabus: {topic_description}
Key Concepts: {concepts_str}
Pedagogical Objective: {topic_focus}
Difficulty Tier: Tier 3 (Advanced / Expert)
{context_block}
{scaffolding_block}

### MANDATORY STRUCTURE:

# 📘 Advanced Architecture: {topic_path}

## 1. 🧠 Theoretical Foundations & Attention Mechanics
- [Substantive explanation of how {topic_path} shapes token prediction logits and reasoning trajectories].

## 2. 🏛️ Production Schema & Guardrail Contract
```markdown
# [ENTERPRISE CONTRACT]
...
# [SECURITY CONSTRAINTS & NEGATIVE DIRECTIVES]
...
```

## 3. 🛡️ Failure Modes & Edge-Case Defense
| Vulnerability / Failure | Mechanism | Fortified Solution |
| :--- | :--- | :--- |
| ... | ... | ... |

Keep output strictly under 460 words with clean GitHub Markdown.
"""


def get_quiz_prompt(
    topic_path: str,
    quiz_type: str,
    difficulty_tier: int,
    rubric: Dict[str, Any],
    fail_streak: int = 0
) -> str:
    return f"""You are a senior assessment specialist.
Create a 3-question dynamic quiz for: '{topic_path}' (Tier {difficulty_tier}/3).
"""


def get_evaluator_prompt() -> str:
    return """You are a rigorous, calibrated LLM-as-a-Judge assessment engine."""
