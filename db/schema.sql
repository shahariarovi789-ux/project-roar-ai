-- db/schema.sql
-- Relational Schema for Multi-Agent Adaptive Prompt Engineering Tutor

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

-- 1. Accounts
CREATE TABLE IF NOT EXISTS accounts (
    user_id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_login TEXT
);

-- 2. Learner Profiles (Onboarding Metadata)
CREATE TABLE IF NOT EXISTS learner_profiles (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    prior_experience TEXT DEFAULT 'beginner',
    prefers_examples INTEGER DEFAULT 1,
    prefers_steps INTEGER DEFAULT 1,
    prefers_detailed INTEGER DEFAULT 1,
    preferred_quiz_style TEXT DEFAULT 'mixed',
    session_time_budget INTEGER DEFAULT 30,
    onboarding_done INTEGER DEFAULT 0,
    profile_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id) ON DELETE CASCADE
);

-- 3. Mastery Map (Per Node)
CREATE TABLE IF NOT EXISTS mastery_map (
    user_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    mastery_score REAL DEFAULT 0.0,
    pass_count INTEGER DEFAULT 0,
    fail_count INTEGER DEFAULT 0,
    last_attempted TEXT,
    last_passed TEXT,
    PRIMARY KEY (user_id, node_id),
    FOREIGN KEY (user_id) REFERENCES accounts(user_id) ON DELETE CASCADE
);

-- 4. Node Attempts (Full Telemetry for Evaluation & Research)
CREATE TABLE IF NOT EXISTS node_attempts (
    attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    quiz_type TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    semantic_score REAL,
    rule_score REAL,
    final_score REAL,
    required_score REAL,
    passed INTEGER NOT NULL,
    hints_used INTEGER DEFAULT 0,
    time_elapsed_s REAL,
    fail_streak_before INTEGER DEFAULT 0,
    llm_rationale TEXT,
    attempted_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id) ON DELETE CASCADE
);

-- 5. Sessions
CREATE TABLE IF NOT EXISTS sessions (
    user_id TEXT PRIMARY KEY,
    current_node_id TEXT DEFAULT 'node_01',
    current_phase TEXT DEFAULT 'ONBOARDING',
    nodes_completed TEXT DEFAULT '[]',
    llm_backend TEXT DEFAULT 'ollama',
    llm_model TEXT DEFAULT 'qwen2.5:7b',
    state_json TEXT,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id) ON DELETE CASCADE
);

-- 6. Final Exam Results
CREATE TABLE IF NOT EXISTS final_exam_results (
    user_id TEXT PRIMARY KEY,
    section_a_score REAL,
    section_b_score REAL,
    section_c_score REAL,
    overall_score REAL,
    passed INTEGER,
    answers_json TEXT,
    completed_at TEXT,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id) ON DELETE CASCADE
);

-- 7. Analytics Events
CREATE TABLE IF NOT EXISTS analytics_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id) ON DELETE CASCADE
);

-- 8. Research Metrics (Latency, LLM comparison)
CREATE TABLE IF NOT EXISTS research_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    llm_backend TEXT NOT NULL,
    llm_model TEXT NOT NULL,
    node_id TEXT NOT NULL,
    latency_ms REAL,
    tokens_used INTEGER,
    quality_score REAL,
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id) ON DELETE CASCADE
);
