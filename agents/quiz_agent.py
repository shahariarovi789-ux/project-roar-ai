# agents/quiz_agent.py
"""
Quiz Agent.
Generates 3 dynamic, non-static challenge questions strictly calibrated to node weight and Bloom taxonomy:
- Tier 1 (Weight 1.0 - 1.5, Remember/Understand): Accessible, beginner-friendly, scenario-based MCQs & prompt writing.
- Tier 2 (Weight 1.8 - 2.8, Apply/Analyze): Applied workflow, delimiters, few-shot formatting, drift diagnosis.
- Tier 3 (Weight 3.0 - 4.0, Evaluate/Create): Advanced reasoning chains, JSON schema contracts, adversarial defense.
"""

import json
import re
import random
from typing import Dict, Any, List, Optional
from core.curriculum import CurriculumNode
from core.learner_profile import LearnerProfile
from backend.model_manager import model_manager
from backend.activity_tracker import activity_tracker


class QuizAgent:
    @staticmethod
    async def generate_quiz_challenge(
        node: CurriculumNode,
        profile: LearnerProfile,
        fail_streak: int = 0,
        force_regen: bool = False
    ) -> Dict[str, Any]:
        """
        Dynamically generates 3 non-static challenge questions calibrated to difficulty weight.
        Guaranteed to never embed hints inside the question text.
        Supports force_regen for on-demand synthesis of fresh alternative question sets.
        """
        tier = node.difficulty_tier
        weight = node.weight
        regen_tag = " (Fresh Question Set)" if force_regen else ""
        activity_tracker.log("Quiz Agent", f"Formulating Tier {tier} quiz for: {node.title}{regen_tag}", f"Weight: {weight} (Bloom: {node.bloom_level})", "running")
        
        key_concepts = ", ".join(node.rubric.get("key_concepts", []))

        # --- TIER 1: FOUNDATIONAL / SCENARIO-DRIVEN (Weight 1.0 - 1.5) ---
        if tier == 1 or weight <= 1.5:
            prompt = f"""You are an expert AI Prompt Engineering Educator.
Create a FRESH, ENGAGING, SCENARIO-BASED 3-question quiz for the foundational topic: '{node.title}'.
Topic Description: {node.description}.
Key Concepts: {key_concepts}.
Difficulty: Tier 1 (Foundational / Beginner, Weight {weight}).

STRICT RULES:
1. Question 1 MUST be a dynamic, realistic scenario Multiple Choice Question (MCQ).
   - Example style: Present a practical situation (e.g. an engineer asking an AI to do task X) and ask which prompt strategy or core concept applies.
   - Do NOT use generic template questions like "What is the primary purpose of...".
   - Provide 4 distinct, plausible options (A, B, C, D) with 1 clearly correct answer.
2. Question 2 MUST be an applied Prompt Writing challenge where the student writes a structured prompt.
3. Question 3 MUST be a Prompt Improvement/Diagnosis challenge where the student fixes a flawed or vague prompt.
4. CRITICAL: NEVER include the word 'Hint', hints, tips, or clues inside the question text. The UI provides a dedicated interactive Hint button for that.

### REQUIRED JSON OUTPUT FORMAT:
Return strictly valid JSON only:
{{
  "questions": [
    {{
      "id": "q1",
      "title": "Question 1: Scenario & Core Mechanics",
      "type": "mcq",
      "question": "<Write a vivid scenario question testing {node.title}>",
      "options": [
        "A) <Option A>",
        "B) <Option B>",
        "C) <Option C>",
        "D) <Option D>"
      ],
      "correct": "B"
    }},
    {{
      "id": "q2",
      "title": "Question 2: Applied Prompt Construction",
      "type": "writing",
      "question": "<Write a specific prompt writing instruction applying {node.title}>"
    }},
    {{
      "id": "q3",
      "title": "Question 3: Prompt Diagnosis & Refinement",
      "type": "writing",
      "question": "<Present a realistic unoptimized prompt and ask the student to diagnose and rewrite it using {node.title}>"
    }}
  ]
}}
"""

        # --- TIER 2: INTERMEDIATE / APPLIED (Weight 1.8 - 2.8) ---
        elif tier == 2 or weight < 3.0:
            prompt = f"""You are a Senior AI Prompt Engineering Instructor.
Create an APPLIED, REAL-WORLD 3-question assessment for: '{node.title}'.
Topic Description: {node.description}.
Key Concepts: {key_concepts}.
Difficulty: Tier 2 (Intermediate, Weight {weight}).

STRICT RULES:
1. Question 1 (MCQ): Test the nuanced mechanics, trade-offs, or attention steering of {node.title} in a realistic production scenario.
2. Question 2 (Writing): Ask the student to construct an end-to-end production prompt using clear delimiters, role constraints, and output formatting.
3. Question 3 (Diagnosis): Present a flawed prompt suffering from drift, ambiguity, or format leakage and ask the student to diagnose the flaw and write the corrected version.
4. CRITICAL: NEVER include words like 'Hint:' or clues inside the question text.

### REQUIRED JSON OUTPUT FORMAT:
Return strictly valid JSON only:
{{
  "questions": [
    {{
      "id": "q1",
      "title": "Question 1: Technique Mechanics & Trade-offs",
      "type": "mcq",
      "question": "<Scenario-based question testing {node.title} mechanics>",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct": "A"
    }},
    {{
      "id": "q2",
      "title": "Question 2: Production Prompt Blueprint",
      "type": "writing",
      "question": "<Actionable prompt authoring task>"
    }},
    {{
      "id": "q3",
      "title": "Question 3: Failure Mode & Guardrails",
      "type": "writing",
      "question": "<Flawed prompt diagnosis and repair task>"
    }}
  ]
}}
"""

        # --- TIER 3: ADVANCED / EXPERT (Weight 3.0 - 4.0) ---
        else:
            prompt = f"""You are a Principal AI Architect.
Create an ADVANCED, ENTERPRISE-GRADE 3-question challenge for: '{node.title}'.
Topic Description: {node.description}.
Key Concepts: {key_concepts}.
Difficulty: Tier 3 (Advanced / Expert, Weight {weight}).

STRICT RULES:
1. Question 1 (MCQ): Deep theoretical mechanics, attention distributions, hallucination mitigation, or adversarial vulnerabilities.
2. Question 2 (Writing): Author a complex enterprise prompt with strict JSON schema contracts, negative constraints, and zero-preamble rules.
3. Question 3 (Writing): Defend an AI agent pipeline against prompt injection, jailbreaks, or cascading reasoning errors.
4. CRITICAL: NEVER include hints or clues inside the question text.

### REQUIRED JSON OUTPUT FORMAT:
Return strictly valid JSON only:
{{
  "questions": [
    {{
      "id": "q1",
      "title": "Question 1: Deep Architectural Mechanics",
      "type": "mcq",
      "question": "<Advanced architectural question>",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct": "C"
    }},
    {{
      "id": "q2",
      "title": "Question 2: Enterprise Specification",
      "type": "writing",
      "question": "<Enterprise prompt construction task>"
    }},
    {{
      "id": "q3",
      "title": "Question 3: Adversarial Robustness & Pipeline Defense",
      "type": "writing",
      "question": "<Adversarial defense and repair task>"
    }}
  ]
}}
"""

        if force_regen:
            prompt += "\n\n### VARIATION REGENERATION DIRECTIVE:\nThe user requested a completely NEW, alternative assessment. Create a fresh scenario question with different practical problem domains, new parameter requirements, and distinct multiple choice distractors."

        # Execute genuine LLM generation
        res = await model_manager.generate_async(
            prompt=prompt,
            system_prompt="You are a calibrated AI assessment engine. Return strictly valid JSON adhering to the requested schema. Never embed hints in questions.",
            temperature=0.85 if force_regen else 0.75,
            max_tokens=1800,
            agent_name="Quiz Agent",
            intent="quiz"
        )

        parsed_questions = QuizAgent._parse_quiz_json(res["text"], node)

        activity_tracker.log(
            "Quiz Agent",
            f"Generated {len(parsed_questions)} questions in {res['latency_ms']}ms",
            f"Difficulty: Tier {tier} (Weight: {weight})",
            "success"
        )

        return {
            "node_id": node.id,
            "topic_title": node.title,
            "topic_path": node.path,
            "difficulty_tier": node.difficulty_tier,
            "weight": node.weight,
            "quiz_type": node.quiz_type,
            "passing_threshold": node.passing_threshold,
            "time_budget_seconds": node.time_budget_seconds,
            "questions": parsed_questions,
            "total_questions": len(parsed_questions),
            "model_used": res["model"]
        }

    @staticmethod
    def _parse_quiz_json(raw_text: str, node: CurriculumNode) -> List[Dict[str, Any]]:
        """Parses, sanitizes, and strips any embedded hints from the quiz JSON."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        def sanitize_question_text(q_text: str) -> str:
            """Strips any accidental 'Hint: ...' or '(Hint: ...)' from the question string."""
            if not q_text:
                return q_text
            # Remove trailing hint statements
            q_clean = re.sub(r"\s*(?:\(?Hint:\s*.*?\)?)$", "", q_text, flags=re.IGNORECASE)
            q_clean = re.sub(r"\s*Hint\s*#?\d*[:\-]\s*.*$", "", q_clean, flags=re.IGNORECASE)
            return q_clean.strip()

        try:
            data = json.loads(cleaned)
            if "questions" in data and isinstance(data["questions"], list) and len(data["questions"]) > 0:
                questions = []
                for idx, q in enumerate(data["questions"]):
                    if not isinstance(q, dict):
                        continue
                    q_id = q.get("id") or f"q{idx+1}"
                    q_type = q.get("type") or ("mcq" if "options" in q else "writing")
                    q_title = q.get("title") or f"Question {idx+1}"
                    q_raw_text = q.get("question") or f"Explain and apply {node.title}."
                    q_text = sanitize_question_text(q_raw_text)

                    question_entry = {
                        "id": q_id,
                        "title": q_title,
                        "type": q_type,
                        "question": q_text,
                    }

                    if q_type == "mcq" and "options" in q and isinstance(q["options"], list):
                        question_entry["options"] = [str(opt) for opt in q["options"]]
                        question_entry["correct"] = str(q.get("correct", "B")).upper()

                    questions.append(question_entry)

                if len(questions) == 3:
                    return questions
        except Exception:
            pass

        # Dynamic topic-aware fallback questions with randomized options
        return QuizAgent._generate_dynamic_fallback_questions(node)

    @staticmethod
    def _generate_dynamic_fallback_questions(node: CurriculumNode) -> List[Dict[str, Any]]:
        """Generates dynamic, non-static fallback questions when LLM response is unparseable."""
        t = node.title
        key_concepts = node.rubric.get("key_concepts", []) if node.rubric else []
        concept_a = key_concepts[0] if key_concepts else "clear instructions"
        concept_b = key_concepts[1] if len(key_concepts) > 1 else "output constraints"

        if node.difficulty_tier == 1:
            mcq_pool = [
                {
                    "question": f"Imagine you want an AI assistant to summarize customer emails into 3 key bullet points. When applying {t}, what is the most effective approach?",
                    "options": [
                        "A) Leave the prompt open-ended so the AI can guess the format",
                        f"B) Explicitly instruct the AI with clear constraints and formatting rules for {concept_a}",
                        "C) Repeat the word 'summarize' multiple times without extra context",
                        "D) Modify the underlying neural network weights directly"
                    ],
                    "correct": "B"
                },
                {
                    "question": f"Why is {t} considered a foundational principle in modern prompt engineering?",
                    "options": [
                        "A) It makes prompts unnecessarily long and expensive to process",
                        "B) It establishes unambiguous guidance that steers the model toward deterministic, high-quality responses",
                        "C) It replaces the need to specify the user's objective",
                        "D) It only works on offline computer vision models"
                    ],
                    "correct": "B"
                }
            ]
            selected_mcq = random.choice(mcq_pool)
            return [
                {
                    "id": "q1",
                    "title": "Question 1: Scenario & Core Concept",
                    "type": "mcq",
                    "question": selected_mcq["question"],
                    "options": selected_mcq["options"],
                    "correct": selected_mcq["correct"]
                },
                {
                    "id": "q2",
                    "title": "Question 2: Practical Prompt Authoring",
                    "type": "writing",
                    "question": f"Write a prompt applying {t} that asks an AI to explain {concept_a} to a high-school student in exactly two bullet points."
                },
                {
                    "id": "q3",
                    "title": "Question 3: Prompt Diagnosis & Repair",
                    "type": "writing",
                    "question": f"Consider this vague prompt: 'Tell me about {t}'. Identify why this prompt lacks precision, and write your fortified replacement."
                }
            ]
        else:
            return [
                {
                    "id": "q1",
                    "title": "Question 1: Architectural Mechanics",
                    "type": "mcq",
                    "question": f"In production LLM systems, how does {t} optimize model token predictions and prevent attention drift?",
                    "options": [
                        "A) By fine-tuning the model weights permanently across training epochs",
                        f"B) By conditioning attention logits via structural boundaries and in-context grounding ({concept_a})",
                        "C) By disabling temperature sampling permanently",
                        "D) By bypassing the context window limit"
                    ],
                    "correct": "B"
                },
                {
                    "id": "q2",
                    "title": "Question 2: Production Prompt Blueprint",
                    "type": "writing",
                    "question": f"Construct a structured prompt incorporating {t} with clear input delimiters, an explicit system persona, and a strict JSON schema contract."
                },
                {
                    "id": "q3",
                    "title": "Question 3: Failure Mode & Edge-Case Defense",
                    "type": "writing",
                    "question": f"Describe a scenario where a prompt lacking {concept_b} fails due to hallucinations or injection, and provide the fortified prompt to prevent it."
                }
            ]

    @staticmethod
    async def generate_hint(
        node: CurriculumNode,
        quiz_question: str,
        hint_number: int,
        previous_hints: Optional[List[str]] = None
    ) -> str:
        """Generates strictly non-repeating progressive hints tailored to difficulty tier and topic."""
        prev_hints = previous_hints or []
        prev_clause = ""
        if prev_hints:
            formatted_prev = "\n".join([f"- {h}" for h in prev_hints])
            prev_clause = f"\nPreviously provided hints (CRITICAL: DO NOT REPEAT OR DUPLICATE ANY OF THESE):\n{formatted_prev}\n"

        if hint_number == 1:
            tier_guidance = f"Level 1 (Core Intuition & Definition): Explain what '{node.title}' means fundamentally in prompt engineering and how it shapes AI outputs."
        elif hint_number == 2:
            tier_guidance = f"Level 2 (Design Rule & Strategy): Provide a practical guideline, parameter tradeoff, or structural tip for using '{node.title}' effectively."
        else:
            tier_guidance = f"Level 3 (Tactical Application & Pitfalls): Provide concrete guidance on what specific elements, delimiters, or constraints to include or avoid for '{node.title}'."

        prompt = (
            f"You are an AI Prompt Engineering Tutor. The student requested Hint #{hint_number}/3 for the topic '{node.title}' (Tier {node.difficulty_tier}, Weight {node.weight}).\n"
            f"Topic Description: {node.description}\n"
            f"Question being answered: {quiz_question}\n"
            f"{prev_clause}\n"
            f"Task: Provide a concise, clear {tier_guidance}.\n"
            f"Rules:\n"
            f"1. You MUST provide a completely NEW and DIFFERENT hint from any previous hints.\n"
            f"2. Keep it under 2 sentences.\n"
            f"3. Do NOT start with 'Hint #1:' or prefix numbers—just provide the hint text directly.\n"
            f"4. Do NOT reveal the exact multiple choice letter or full final prompt solution."
        )

        res = await model_manager.generate_async(
            prompt=prompt,
            system_prompt="You are an expert prompt engineering tutor providing progressive, unique hints.",
            temperature=0.7,
            max_tokens=150,
            agent_name="Hint Agent",
            intent=f"hint_{hint_number}_{node.id}"
        )

        raw_text = res.get("text", "").strip()
        # Clean redundant prefixes like "Hint #1:", "**Hint 2:**", etc.
        cleaned_hint = re.sub(r"^(?:Hint\s*#?\d*[:\-]\s*|\*\*Hint\s*#?\d*[:\-]?\*\*\s*|💡\s*)", "", raw_text, flags=re.IGNORECASE).strip()

        # Check for duplication against previous hints
        is_duplicate = False
        for prev in prev_hints:
            clean_prev = re.sub(r"^(?:Hint\s*#?\d*[:\-]\s*|\*\*Hint\s*#?\d*[:\-]?\*\*\s*|💡\s*)", "", prev, flags=re.IGNORECASE).strip().lower()
            if cleaned_hint.lower() == clean_prev:
                is_duplicate = True
                break
            # Check high word overlap
            words_cand = set(re.findall(r"\w+", cleaned_hint.lower()))
            words_prev = set(re.findall(r"\w+", clean_prev))
            if words_cand and words_prev:
                jaccard = len(words_cand & words_prev) / len(words_cand | words_prev)
                if jaccard > 0.70:
                    is_duplicate = True
                    break

        if not cleaned_hint or is_duplicate:
            cleaned_hint = QuizAgent._get_progressive_fallback_hint(node, hint_number, quiz_question, prev_hints)

        return cleaned_hint

    @staticmethod
    def _get_progressive_fallback_hint(
        node: CurriculumNode,
        hint_number: int,
        quiz_question: str,
        previous_hints: Optional[List[str]] = None
    ) -> str:
        """Deterministic topic-specific progressive hints guaranteed to never repeat across levels 1, 2, 3."""
        key_concepts = node.rubric.get("key_concepts", []) if node.rubric else []
        concept_str = ", ".join(key_concepts[:2]) if key_concepts else node.title.lower()
        title_lower = node.title.lower()

        # Topic-tailored hints for Temperature / Sampling controls
        if "temperature" in title_lower or node.id == "node_04":
            if hint_number == 1:
                return "Temperature scales the token logits in softmax: lower values concentrate probability on the top tokens (deterministic), while higher values flatten the distribution (creative)."
            elif hint_number == 2:
                return "For classification, math, and JSON schema extraction, use a low temperature (0.0 to 0.2). For creative writing and varied brainstorming, use 0.7 to 1.0."
            else:
                return "Setting temperature to 0.0 effectively uses greedy decoding, ensuring the model returns the single highest probability token at every step."

        # Topic-tailored hints for System Prompt / Persona
        if "system" in title_lower or "persona" in title_lower or "role" in title_lower:
            if hint_number == 1:
                return "System prompts establish the overarching behavioral identity, expertise domain, and persistent rules for the entire interaction."
            elif hint_number == 2:
                return "Clearly define the persona's perspective, tone, and what specific tasks they are authorized or forbidden to perform."
            else:
                return "Use explicit role constraints: 'You are an expert X. Always analyze the input using Y framework before responding.'"

        # Topic-tailored hints for Few-Shot / Examples
        if "few-shot" in title_lower or "few shot" in title_lower or "example" in title_lower:
            if hint_number == 1:
                return "Few-shot prompting provides demonstrations of input-output pairs to prime the model's pattern recognition."
            elif hint_number == 2:
                return "Keep the formatting of each example strictly uniform, and ensure negative edge cases are handled in at least one example."
            else:
                return "Always provide diverse examples that represent the breadth of real user queries to avoid overfitting to one template."

        # Topic-tailored hints for Delimiters
        if "delimiter" in title_lower:
            if hint_number == 1:
                return "Delimiters (like ``` or <context>) clearly separate instructions from user-supplied untrusted text."
            elif hint_number == 2:
                return "Explicitly reference the delimiters in your instructions: 'Summarize the text enclosed in <document> tags'."
            else:
                return "Delimiters prevent prompt injection by establishing unambiguous structural boundaries between commands and payload data."

        # Question-type aware dynamic guidance
        q_lower = quiz_question.lower()
        is_writing = "write" in q_lower or "construct" in q_lower or "author" in q_lower or "prompt" in q_lower
        is_diagnosis = "diagnose" in q_lower or "improve" in q_lower or "vague" in q_lower or "flaw" in q_lower or "repair" in q_lower or "refine" in q_lower

        if is_diagnosis:
            if hint_number == 1:
                return f"Identify the core flaw in the prompt related to {node.title}—look for missing delimiters, absent role personas, or undefined output structure."
            elif hint_number == 2:
                return f"Explain the failure mode: without strict constraints for {node.title}, the model suffers from attention drift or hallucinations."
            else:
                return "In your fortified prompt, add explicit affirmative directives, clear input delimiters (e.g. ```), and strict negative output constraints."

        if is_writing:
            if hint_number == 1:
                return f"For this writing task on {node.title}, start by defining an authoritative system persona role and declaring the target task."
            elif hint_number == 2:
                return f"Integrate key parameters for {node.title} (e.g. {concept_str}) and structure the prompt with clear input delimiters."
            else:
                return "Complete your prompt by specifying the exact expected output schema and explicitly forbidding conversational preamble."

        # Generic progressive fallback based on node metadata
        if hint_number == 1:
            desc = node.description.split('.')[0] if node.description else f"the foundational principles of {node.title}"
            return f"Think about {desc}—consider how this mechanism directly impacts the model's output quality."
        elif hint_number == 2:
            return f"In your prompt or answer, consider how key concepts like {concept_str} structure and constrain the AI's reasoning."
        else:
            return f"Ensure your solution clearly specifies boundary constraints, input delimiters, and the exact desired output schema for {node.title}."


# Global singleton instance
quiz_agent = QuizAgent()
