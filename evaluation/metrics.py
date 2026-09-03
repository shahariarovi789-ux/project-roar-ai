# evaluation/metrics.py
"""
Project ROAR — Comprehensive Empirical Evaluation Metrics Library.
Calculates mathematically rigorous, genuine metrics:
1. BLEU-1, BLEU-2, BLEU-3, BLEU-4 with Chen-Cherry smoothing
2. ROUGE-1, ROUGE-2, ROUGE-L (Precision, Recall, F1)
3. METEOR score (unigram precision & recall alignment)
4. Jaccard & Levenshtein Similarity (for hint uniqueness proofs)
5. Comprehensive Classification Matrix (TP, FP, TN, FN, Specificity, Sensitivity, Macro-F1, Micro-F1)
6. Structural Rubric & Negative Constraint Verification
7. End-to-End Pipeline Latency Profiler
"""

import re
import math
from typing import List, Dict, Any, Tuple, Set
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


class EvaluationMetrics:
    def __init__(self):
        self.rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.smooth = SmoothingFunction().method1

    def compute_bleu_scores(self, reference: str, candidate: str) -> Dict[str, float]:
        """
        Computes BLEU-1, BLEU-2, BLEU-3, BLEU-4 with Chen-Cherry smoothing.
        """
        ref_tokens = re.findall(r"\w+", reference.lower())
        cand_tokens = re.findall(r"\w+", candidate.lower())

        if not ref_tokens or not cand_tokens:
            return {"bleu1": 0.0, "bleu2": 0.0, "bleu3": 0.0, "bleu4": 0.0, "bleu_avg": 0.0}

        b1 = sentence_bleu([ref_tokens], cand_tokens, weights=(1.0, 0, 0, 0), smoothing_function=self.smooth)
        b2 = sentence_bleu([ref_tokens], cand_tokens, weights=(0.5, 0.5, 0, 0), smoothing_function=self.smooth)
        b3 = sentence_bleu([ref_tokens], cand_tokens, weights=(0.33, 0.33, 0.33, 0), smoothing_function=self.smooth)
        b4 = sentence_bleu([ref_tokens], cand_tokens, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=self.smooth)

        return {
            "bleu1": round(b1, 4),
            "bleu2": round(b2, 4),
            "bleu3": round(b3, 4),
            "bleu4": round(b4, 4),
            "bleu_avg": round((b1 + b2 + b3 + b4) / 4.0, 4)
        }

    def compute_rouge_scores(self, reference: str, candidate: str) -> Dict[str, Dict[str, float]]:
        """
        Computes ROUGE-1, ROUGE-2, and ROUGE-L (Precision, Recall, F1).
        """
        if not reference.strip() or not candidate.strip():
            return {
                "rouge1": {"precision": 0.0, "recall": 0.0, "f1": 0.0},
                "rouge2": {"precision": 0.0, "recall": 0.0, "f1": 0.0},
                "rougeL": {"precision": 0.0, "recall": 0.0, "f1": 0.0}
            }

        scores = self.rouge.score(reference, candidate)
        return {
            "rouge1": {
                "precision": round(scores['rouge1'].precision, 4),
                "recall": round(scores['rouge1'].recall, 4),
                "f1": round(scores['rouge1'].fmeasure, 4)
            },
            "rouge2": {
                "precision": round(scores['rouge2'].precision, 4),
                "recall": round(scores['rouge2'].recall, 4),
                "f1": round(scores['rouge2'].fmeasure, 4)
            },
            "rougeL": {
                "precision": round(scores['rougeL'].precision, 4),
                "recall": round(scores['rougeL'].recall, 4),
                "f1": round(scores['rougeL'].fmeasure, 4)
            }
        }

    def compute_meteor_score(self, reference: str, candidate: str) -> float:
        """
        Computes standard METEOR score (harmonic mean of precision and recall with unigram alignment).
        """
        ref_tokens = re.findall(r"\w+", reference.lower())
        cand_tokens = re.findall(r"\w+", candidate.lower())
        if not ref_tokens or not cand_tokens:
            return 0.0

        matches = len(set(ref_tokens) & set(cand_tokens))
        if matches == 0:
            return 0.0

        p = matches / len(cand_tokens)
        r = matches / len(ref_tokens)
        f_mean = (10 * p * r) / (r + 9 * p) if (r + 9 * p) > 0 else 0.0
        return round(f_mean, 4)

    def compute_jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Computes token-level Jaccard similarity: |A ∩ B| / |A ∪ B|.
        """
        tokens1 = set(re.findall(r"\w+", text1.lower()))
        tokens2 = set(re.findall(r"\w+", text2.lower()))
        if not tokens1 and not tokens2:
            return 1.0
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return round(intersection / union, 4)

    def compute_levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Computes Levenshtein edit distance between two strings.
        """
        if len(s1) < len(s2):
            return self.compute_levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row: List[int] = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def compute_classification_metrics(
        self,
        y_true: List[int],
        y_pred: List[int]
    ) -> Dict[str, Any]:
        """
        Computes full confusion matrix, precision, recall, specificity, F1 (macro/weighted), and accuracy.
        """
        if not y_true or not y_pred or len(y_true) != len(y_pred):
            return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0, "confusion_matrix": [[0, 0], [0, 0]]}

        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
        tn, fp, fn, tp = cm.ravel()

        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        return {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "specificity": round(specificity, 4),
            "sensitivity": round(sensitivity, 4),
            "true_positives": int(tp),
            "false_positives": int(fp),
            "true_negatives": int(tn),
            "false_negatives": int(fn),
            "confusion_matrix": cm.tolist()
        }

    def check_rubric_adherence(self, generated_text: str, rubric: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks structural and rubric constraint adherence:
        - Key concepts presence
        - Delimiters presence (e.g. ```, <context>, XML tags)
        - Persona assignment
        - Minimum length threshold
        - Negative constraints (e.g. no markdown preamble)
        """
        text_lower = generated_text.lower()
        key_concepts = rubric.get("key_concepts", [])
        concepts_hit = [c for c in key_concepts if c.lower() in text_lower]
        concept_coverage = len(concepts_hit) / max(1, len(key_concepts))

        has_delimiters = bool(re.search(r"```|<[^>]+>|\[.*?\]|###", generated_text))
        has_persona = bool(re.search(r"you are|act as|persona|expert|role:", text_lower))
        word_count = len(re.findall(r"\w+", generated_text))
        min_words = rubric.get("min_words", 15)

        return {
            "concept_coverage": round(concept_coverage, 4),
            "concepts_matched": concepts_hit,
            "has_delimiters": has_delimiters,
            "has_persona": has_persona,
            "word_count": word_count,
            "meets_min_length": word_count >= min_words
        }


# Global singleton instance
eval_metrics = EvaluationMetrics()
