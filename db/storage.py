# db/storage.py
"""
Storage and Persistence Layer for SQLite WAL Database.
Provides async and sync helpers for CRUD operations across all tables.
"""

import os
import json
import sqlite3
import aiosqlite
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from core.learner_profile import LearnerProfile
from core.state_machine import TutorState, TutorPhase

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "db" / "tutor.db"
SCHEMA_FILE = Path(__file__).resolve().parent / "schema.sql"


def get_db_path() -> str:
    path = os.getenv("DB_PATH", str(DB_PATH))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    return path


def init_database_sync():
    """Initializes schema synchronously."""
    path = get_db_path()
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    con = sqlite3.connect(path)
    con.executescript(schema_sql)
    con.commit()
    con.close()
    print(f"[DB] Initialized database at: {path}")


async def get_db_connection() -> aiosqlite.Connection:
    path = get_db_path()
    db = await aiosqlite.connect(path)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode = WAL;")
    await db.execute("PRAGMA synchronous = NORMAL;")
    await db.execute("PRAGMA foreign_keys = ON;")
    return db


# ============================================================
# Account & Auth Operations
# ============================================================

async def create_account(user_id: str, username: str, password_hash: str, email: Optional[str] = None) -> bool:
    db = await get_db_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        await db.execute(
            """
            INSERT INTO accounts (user_id, username, email, password_hash, created_at, last_login)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, username, email, password_hash, now, now)
        )
        # Create initial profile and session entries
        init_profile = LearnerProfile(user_id=user_id)
        await db.execute(
            """
            INSERT INTO learner_profiles (user_id, name, created_at, updated_at, profile_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, username, now, now, json.dumps(init_profile.to_dict()))
        )
        init_state = TutorState(user_id=user_id)
        await db.execute(
            """
            INSERT INTO sessions (user_id, current_node_id, current_phase, nodes_completed, state_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, "node_01", "ONBOARDING", "[]", json.dumps(init_state.to_dict()), now)
        )
        await db.commit()
        return True
    except Exception as e:
        print(f"[DB Error] create_account: {e}")
        return False
    finally:
        await db.close()


async def get_account_by_username(username: str) -> Optional[Dict[str, Any]]:
    db = await get_db_connection()
    try:
        cursor = await db.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


async def get_account_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    db = await get_db_connection()
    try:
        cursor = await db.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None
    finally:
        await db.close()


# ============================================================
# Learner Profile Operations
# ============================================================

async def get_learner_profile(user_id: str) -> Optional[LearnerProfile]:
    db = await get_db_connection()
    try:
        cursor = await db.execute("SELECT profile_json FROM learner_profiles WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row and row["profile_json"]:
            return LearnerProfile.from_dict(json.loads(row["profile_json"]))
        return None
    finally:
        await db.close()


async def save_learner_profile(profile: LearnerProfile) -> bool:
    db = await get_db_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        profile.updated_at = now
        p_dict = profile.to_dict()
        p_json = json.dumps(p_dict)
        await db.execute(
            """
            INSERT INTO learner_profiles (
                user_id, name, prior_experience, prefers_examples, prefers_steps,
                prefers_detailed, preferred_quiz_style, session_time_budget,
                onboarding_done, profile_json, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                prior_experience = excluded.prior_experience,
                prefers_examples = excluded.prefers_examples,
                prefers_steps = excluded.prefers_steps,
                prefers_detailed = excluded.prefers_detailed,
                preferred_quiz_style = excluded.preferred_quiz_style,
                session_time_budget = excluded.session_time_budget,
                onboarding_done = excluded.onboarding_done,
                profile_json = excluded.profile_json,
                updated_at = excluded.updated_at
            """,
            (
                profile.user_id, profile.name, profile.prior_experience,
                int(profile.prefers_examples), int(profile.prefers_steps),
                int(profile.prefers_detailed), profile.preferred_quiz_style,
                profile.session_time_budget, int(profile.onboarding_done),
                p_json, profile.created_at, now
            )
        )
        await db.commit()
        return True
    finally:
        await db.close()


# ============================================================
# Session Operations
# ============================================================

async def get_tutor_state(user_id: str) -> Optional[TutorState]:
    db = await get_db_connection()
    try:
        cursor = await db.execute("SELECT state_json FROM sessions WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row and row["state_json"]:
            return TutorState.from_dict(json.loads(row["state_json"]))
        return None
    finally:
        await db.close()


async def save_tutor_state(user_id: str, state: TutorState, completed_nodes: List[str]) -> bool:
    db = await get_db_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        state_json = json.dumps(state.to_dict())
        nodes_json = json.dumps(completed_nodes)
        await db.execute(
            """
            INSERT INTO sessions (user_id, current_node_id, current_phase, nodes_completed, state_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                current_node_id = excluded.current_node_id,
                current_phase = excluded.current_phase,
                nodes_completed = excluded.nodes_completed,
                state_json = excluded.state_json,
                updated_at = excluded.updated_at
            """,
            (user_id, state.current_node_id, state.phase.value, nodes_json, state_json, now)
        )
        await db.commit()
        return True
    finally:
        await db.close()


# ============================================================
# Quiz Attempts & Mastery
# ============================================================

async def record_quiz_attempt(
    user_id: str,
    node_id: str,
    quiz_type: str,
    answer_text: str,
    semantic_score: float,
    rule_score: float,
    final_score: float,
    required_score: float,
    passed: bool,
    hints_used: int,
    time_elapsed_s: float,
    fail_streak_before: int,
    llm_rationale: str
) -> int:
    db = await get_db_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        cursor = await db.execute(
            """
            INSERT INTO node_attempts (
                user_id, node_id, quiz_type, answer_text, semantic_score,
                rule_score, final_score, required_score, passed, hints_used,
                time_elapsed_s, fail_streak_before, llm_rationale, attempted_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, node_id, quiz_type, answer_text, semantic_score,
                rule_score, final_score, required_score, int(passed), hints_used,
                time_elapsed_s, fail_streak_before, llm_rationale, now
            )
        )
        
        # Update Mastery Map
        if passed:
            await db.execute(
                """
                INSERT INTO mastery_map (user_id, node_id, mastery_score, pass_count, fail_count, last_attempted, last_passed)
                VALUES (?, ?, ?, 1, 0, ?, ?)
                ON CONFLICT(user_id, node_id) DO UPDATE SET
                    mastery_score = MAX(mastery_score, excluded.mastery_score),
                    pass_count = pass_count + 1,
                    last_attempted = excluded.last_attempted,
                    last_passed = excluded.last_passed
                """,
                (user_id, node_id, final_score, now, now)
            )
        else:
            await db.execute(
                """
                INSERT INTO mastery_map (user_id, node_id, mastery_score, pass_count, fail_count, last_attempted, last_passed)
                VALUES (?, ?, ?, 0, 1, ?, NULL)
                ON CONFLICT(user_id, node_id) DO UPDATE SET
                    fail_count = fail_count + 1,
                    last_attempted = excluded.last_attempted
                """,
                (user_id, node_id, final_score, now)
            )

        await db.commit()
        return cursor.lastrowid or 0
    finally:
        await db.close()


async def get_all_mastery_scores(user_id: str) -> Dict[str, Dict[str, Any]]:
    db = await get_db_connection()
    try:
        cursor = await db.execute("SELECT * FROM mastery_map WHERE user_id = ?", (user_id,))
        rows = await cursor.fetchall()
        return {row["node_id"]: dict(row) for row in rows}
    finally:
        await db.close()


# ============================================================
# Research & Analytics Logging
# ============================================================

async def log_research_metric(
    user_id: str,
    llm_backend: str,
    llm_model: str,
    node_id: str,
    latency_ms: float,
    tokens_used: int,
    quality_score: float
):
    db = await get_db_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        await db.execute(
            """
            INSERT INTO research_metrics (
                user_id, llm_backend, llm_model, node_id, latency_ms, tokens_used, quality_score, recorded_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, llm_backend, llm_model, node_id, latency_ms, tokens_used, quality_score, now)
        )
        await db.commit()
    finally:
        await db.close()


async def log_analytics_event(user_id: str, event_type: str, payload: Optional[Dict[str, Any]] = None):
    db = await get_db_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        payload_json = json.dumps(payload) if payload else None
        await db.execute(
            """
            INSERT INTO analytics_events (user_id, event_type, payload_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, event_type, payload_json, now)
        )
        await db.commit()
    finally:
        await db.close()
