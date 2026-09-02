# db/models.py
"""
SQLAlchemy ORM Models and Pydantic Schemas for Database Operations.
"""

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

Base = declarative_base()


class AccountORM(Base):
    __tablename__ = "accounts"

    user_id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    last_login = Column(String, nullable=True)

    profile = relationship("LearnerProfileORM", back_populates="account", uselist=False, cascade="all, delete-orphan")
    session = relationship("SessionORM", back_populates="account", uselist=False, cascade="all, delete-orphan")


class LearnerProfileORM(Base):
    __tablename__ = "learner_profiles"

    user_id = Column(String, ForeignKey("accounts.user_id", ondelete="CASCADE"), primary_key=True)
    name = Column(String, nullable=True)
    prior_experience = Column(String, default="beginner")
    prefers_examples = Column(Integer, default=1)
    prefers_steps = Column(Integer, default=1)
    prefers_detailed = Column(Integer, default=1)
    preferred_quiz_style = Column(String, default="mixed")
    session_time_budget = Column(Integer, default=30)
    onboarding_done = Column(Integer, default=0)
    profile_json = Column(Text, nullable=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    account = relationship("AccountORM", back_populates="profile")


class MasteryMapORM(Base):
    __tablename__ = "mastery_map"

    user_id = Column(String, ForeignKey("accounts.user_id", ondelete="CASCADE"), primary_key=True)
    node_id = Column(String, primary_key=True)
    mastery_score = Column(Float, default=0.0)
    pass_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)
    last_attempted = Column(String, nullable=True)
    last_passed = Column(String, nullable=True)


class NodeAttemptORM(Base):
    __tablename__ = "node_attempts"

    attempt_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("accounts.user_id", ondelete="CASCADE"), nullable=False)
    node_id = Column(String, nullable=False)
    quiz_type = Column(String, nullable=False)
    answer_text = Column(Text, nullable=False)
    semantic_score = Column(Float, nullable=True)
    rule_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=True)
    required_score = Column(Float, nullable=True)
    passed = Column(Integer, nullable=False)
    hints_used = Column(Integer, default=0)
    time_elapsed_s = Column(Float, nullable=True)
    fail_streak_before = Column(Integer, default=0)
    llm_rationale = Column(Text, nullable=True)
    attempted_at = Column(String, nullable=False)


class SessionORM(Base):
    __tablename__ = "sessions"

    user_id = Column(String, ForeignKey("accounts.user_id", ondelete="CASCADE"), primary_key=True)
    current_node_id = Column(String, default="node_01")
    current_phase = Column(String, default="ONBOARDING")
    nodes_completed = Column(Text, default="[]")
    llm_backend = Column(String, default="ollama")
    llm_model = Column(String, default="qwen2.5:7b")
    state_json = Column(Text, nullable=True)
    updated_at = Column(String, nullable=False)

    account = relationship("AccountORM", back_populates="session")


class FinalExamResultORM(Base):
    __tablename__ = "final_exam_results"

    user_id = Column(String, ForeignKey("accounts.user_id", ondelete="CASCADE"), primary_key=True)
    section_a_score = Column(Float, nullable=True)
    section_b_score = Column(Float, nullable=True)
    section_c_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    passed = Column(Integer, nullable=True)
    answers_json = Column(Text, nullable=True)
    completed_at = Column(String, nullable=True)


class AnalyticsEventORM(Base):
    __tablename__ = "analytics_events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("accounts.user_id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String, nullable=False)
    payload_json = Column(Text, nullable=True)
    created_at = Column(String, nullable=False)


class ResearchMetricORM(Base):
    __tablename__ = "research_metrics"

    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("accounts.user_id", ondelete="CASCADE"), nullable=False)
    llm_backend = Column(String, nullable=False)
    llm_model = Column(String, nullable=False)
    node_id = Column(String, nullable=False)
    latency_ms = Column(Float, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    quality_score = Column(Float, nullable=True)
    recorded_at = Column(String, nullable=False)


# --- Pydantic Schemas for API Validation ---
class UserRegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class UserLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str


class OnboardingAnswerRequest(BaseModel):
    name: Optional[str] = None
    prior_experience: Optional[str] = "beginner"
    prefers_examples: Optional[bool] = True
    prefers_steps: Optional[bool] = True
    prefers_detailed: Optional[bool] = True
    preferred_quiz_style: Optional[str] = "mixed"
    session_time_budget: Optional[int] = 30


class QuizSubmitRequest(BaseModel):
    answer: Optional[str] = None
    answers: Optional[Dict[str, str]] = None


class QuizHintRequest(BaseModel):
    node_id: Optional[str] = None
    question_idx: Optional[int] = 1
    current_hints_used: Optional[int] = None



class ModelSwitchRequest(BaseModel):
    backend: str = "ollama"  # "ollama", "groq", "openai", "openrouter", "deepseek", "custom_api"
    model: str = "qwen2.5-coder:7b"
    api_key: Optional[str] = None
    ollama_host: Optional[str] = None
    base_url: Optional[str] = None


