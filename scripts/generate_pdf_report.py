# scripts/generate_pdf_report.py
"""
Generates a publication-grade, comprehensive PDF technical report for Project ROAR
with in-depth Code Explanations, Multi-Agent Logic Walkthroughs, Scoring Math,
and File Base Reference.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render 'Page X of Y'."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(46, 11 * inch - 30, "PROJECT ROAR — Adaptive Multi-Agent Intelligent Tutoring System")
            self.drawRightString(8.5 * inch - 46, 11 * inch - 30, "Code Architecture & Technical Deep-Dive")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(46, 11 * inch - 34, 8.5 * inch - 46, 11 * inch - 34)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(46, 38, 8.5 * inch - 46, 38)
        self.drawString(46, 26, "Confidential & Academic Research Documentation")
        self.drawRightString(8.5 * inch - 46, 26, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf_report(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=46,
        rightMargin=46,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    c_primary = colors.HexColor("#0F172A")  # Dark Slate
    c_accent  = colors.HexColor("#B45309")  # Amber / Gold
    c_text    = colors.HexColor("#1E293B")  # Slate 800
    c_bg_alt  = colors.HexColor("#F8FAFC")  # Slate 50

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=c_accent,
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_primary,
        spaceBefore=9,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_text,
        spaceAfter=3.5
    )

    th_style = ParagraphStyle(
        'TableHead',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white
    )

    td_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=c_text
    )

    td_bold_style = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.5,
        textColor=c_primary
    )

    td_code_style = ParagraphStyle(
        'TableCellCode',
        fontName='Courier',
        fontSize=6.8,
        leading=9,
        textColor=colors.HexColor("#0F172A")
    )

    code_box_style = ParagraphStyle(
        'CodeBox',
        fontName='Courier',
        fontSize=7.2,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # ================= PAGE 1 =================
    # --- Header Banner ---
    story.append(Paragraph("PROJECT ROAR", title_style))
    story.append(Paragraph("Adaptive Multi-Agent Prompt Engineering Intelligent Tutoring System — Comprehensive Technical Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=6))

    # --- Metadata Card ---
    meta_data = [
        [
            Paragraph("<b>System Name:</b> Project ROAR v2.0", td_style),
            Paragraph("<b>Backend Engine:</b> FastAPI / Python 3.14", td_style)
        ],
        [
            Paragraph("<b>Inference Layer:</b> Ollama Cloud / Local / OpenRouter", td_style),
            Paragraph("<b>Knowledge Graph:</b> 36 Nodes across 3 Difficulty Tiers", td_style)
        ],
        [
            Paragraph("<b>Vector Store:</b> ChromaDB (Semantic RAG)", td_style),
            Paragraph("<b>Database:</b> SQLite + SQLAlchemy ORM", td_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[256, 264])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_alt),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    # --- Section 1: Executive Summary ---
    story.append(Paragraph("1. Executive Summary & Pedagogical Objective", h1_style))
    story.append(Paragraph(
        "<b>Project ROAR</b> is an academic-grade Intelligent Tutoring System (ITS) engineered to educate students, software engineers, and researchers in the systematic principles of Prompt Engineering and LLM Steerability. "
        "Unlike generic chatbot assistants that provide unconstrained conversation, Project ROAR enforces strict pedagogical scaffolding, continuous cognitive difficulty calibration, retrieval-grounded instruction, and multi-variable empirical assessment.",
        body_style
    ))
    story.append(Paragraph(
        "The system coordinates four specialized LLM agents overseen by a centralized Finite State Machine. Every interaction—from dynamic lesson synthesis to 3-part challenge formulation and semantic scoring—is grounded in a structured 36-node prerequisite graph.",
        body_style
    ))

    # --- Section 2: Multi-Agent Cognition Framework ---
    story.append(Paragraph("2. Multi-Agent Framework & Specialized Roles", h1_style))

    agent_rows = [
        [
            Paragraph("Agent Name", th_style),
            Paragraph("Primary Role &amp; Responsibilities", th_style),
            Paragraph("Tools &amp; Infrastructure Used", th_style)
        ],
        [
            Paragraph("<b>Tutor Orchestrator</b><br/><code>agents/orchestrator.py</code>", td_bold_style),
            Paragraph("Acts as the master finite state machine. Manages student state transitions (Onboarding → Lesson → Quiz → Evaluation → Node Passed), resolves prerequisite DAG unlocks, and persists session progress.", td_style),
            Paragraph("State Machine Controller, SQLite persistence, Activity Tracker.", td_style)
        ],
        [
            Paragraph("<b>Lesson Agent</b><br/><code>agents/lesson_agent.py</code>", td_bold_style),
            Paragraph("Queries domain documentation and synthesizes publication-grade study guides tailored to the learner's experience level, topic Bloom taxonomy, and continuous weight.", td_style),
            Paragraph("ChromaDB Vector Store (Semantic RAG), ModelManager LLM Router.", td_style)
        ],
        [
            Paragraph("<b>Quiz Agent</b><br/><code>agents/quiz_agent.py</code>", td_bold_style),
            Paragraph("Generates dynamic 3-part assessments calibrated to topic weight: (1) Theory MCQ, (2) Applied Prompt Construction, (3) Edge-case Refinement. Formulates scaffolded retry challenges.", td_style),
            Paragraph("ModelManager, JSON Schema Enforcer, Bloom Taxonomy Calibrator.", td_style)
        ],
        [
            Paragraph("<b>Hint Agent</b><br/><code>agents/quiz_agent.py</code>", td_bold_style),
            Paragraph("Provides progressive, non-repeating scaffolding across 3 levels: Level 1 (Mental Model), Level 2 (Structural Rules), Level 3 (Tactical Guidance). Tracks history to guarantee zero duplicates.", td_style),
            Paragraph("Deduplication Filter, Session History Memory, ModelManager.", td_style)
        ],
        [
            Paragraph("<b>Evaluator Agent</b><br/><code>agents/evaluator_agent.py</code>", td_bold_style),
            Paragraph("Grades multi-question submissions using a combined LLM semantic judge and deterministic rubric matcher. Calculates the 5-variable adaptive scoring formula with time and hint penalties.", td_style),
            Paragraph("LLM Semantic Judge, 5-Variable Scoring Engine, Rubric Matcher.", td_style)
        ]
    ]

    agent_table = Table(agent_rows, colWidths=[120, 260, 140])
    agent_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_alt]),
    ]))
    story.append(agent_table)
    story.append(Spacer(1, 4))

    # --- Section 3: Tools & Technical Infrastructure ---
    story.append(Paragraph("3. Tools, Technologies & Infrastructure", h1_style))

    tools_rows = [
        [Paragraph("Component / Tool", th_style), Paragraph("Technology &amp; Integration Details", th_style)],
        [
            Paragraph("<b>Vector Store (RAG)</b>", td_bold_style),
            Paragraph("<b>ChromaDB</b> (<code>rag/vector_store.py</code>). Ingests and stores semantic vector embeddings of prompt engineering research papers, textbooks, and operational guidelines to ground generated lessons.", td_style)
        ],
        [
            Paragraph("<b>Inference Router</b>", td_bold_style),
            Paragraph("<b>ModelManager</b> (<code>backend/model_manager.py</code>). Unified inference abstraction supporting Ollama Cloud Web API (<code>https://api.ollama.com</code>), local Ollama daemon, and OpenRouter API with live health testing.", td_style)
        ],
        [
            Paragraph("<b>Relational Persistence</b>", td_bold_style),
            Paragraph("<b>SQLite + SQLAlchemy ORM</b> (<code>db/storage.py</code>, <code>db/models.py</code>). Stores user accounts, bcrypt password hashes, learner profiles, mastery maps, quiz attempts, and empirical research telemetry.", td_style)
        ],
        [
            Paragraph("<b>Live Telemetry Stream</b>", td_bold_style),
            Paragraph("<b>ActivityTracker</b> (<code>backend/activity_tracker.py</code>). Real-time ring buffer logging inference roundtrip latency (ms), token usage counts, active models, and agent actions to the UI drawer.", td_style)
        ],
        [
            Paragraph("<b>Frontend Architecture</b>", td_bold_style),
            Paragraph("<b>Vanilla ES6 Modules &amp; Custom Design System</b> (<code>ui/static/</code>). Monospaced developer-tool design system utilizing Geist and JetBrains Mono typography, custom CSS tokens, and full responsive layout.", td_style)
        ]
    ]

    tools_table = Table(tools_rows, colWidths=[120, 400])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_alt]),
    ]))
    story.append(tools_table)
    story.append(PageBreak())

    # ================= PAGE 2 =================
    # --- Section 4: Adaptive Scoring Engine ---
    story.append(Paragraph("4. 5-Variable Adaptive Scoring Mathematical Formulation", h1_style))
    story.append(Paragraph(
        "Student submissions are evaluated using a multi-factor adaptive scoring equation balancing semantic correctness, structural compliance, time efficiency, hint dependency, and historical retry penalty:",
        body_style
    ))

    score_box_data = [[
        Paragraph(
            "<b>Final Score Formula:</b><br/>"
            "<b>S_final = max(0.0, (0.50 * S_semantic + 0.50 * S_rule) - P_hint - P_time - P_retry)</b><br/><br/>"
            "• <b>S_semantic (50%):</b> LLM Judge evaluation of theoretical depth, reasoning validity, and accuracy.<br/>"
            "• <b>S_rule (50%):</b> Deterministic keyword matching, structural delimiters, and length checks.<br/>"
            "• <b>P_hint:</b> Scaffolding penalty: <code>0.05 * hints_used</code> (max 0.15 for 3 hints).<br/>"
            "• <b>P_time:</b> Overtime penalty: <code>max(0.0, ((time_elapsed - time_budget) / time_budget) * 0.15)</code>.<br/>"
            "• <b>P_retry:</b> Consecutive fail streak penalty: <code>min(0.15, fail_streak * 0.05)</code>.<br/>"
            "• <b>Passing Thresholds:</b> Tier 1 = 50%, Tier 2 = 60%, Tier 3 = 70%.",
            code_box_style
        )
    ]]
    score_box = Table(score_box_data, colWidths=[520])
    score_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(score_box)
    story.append(Spacer(1, 4))

    # --- Section 5: Complete File Base Map ---
    story.append(Paragraph("5. Complete File Base & Directory Map", h1_style))

    file_rows = [
        [Paragraph("File / Directory Path", th_style), Paragraph("Architectural Responsibility", th_style)],
        [Paragraph("<code>main.py</code>", td_code_style), Paragraph("FastAPI application entry point, CORS middleware, and static asset mount.", td_style)],
        [Paragraph("<code>api/main.py</code>", td_code_style), Paragraph("Router aggregator combining all sub-routers under <code>/api/v1</code>.", td_style)],
        [Paragraph("<code>api/middleware.py</code>", td_code_style), Paragraph("JWT Bearer token verification and user context dependency injection.", td_style)],
        [Paragraph("<code>api/routes/auth.py</code>", td_code_style), Paragraph("Endpoints for user registration, authentication, and <code>/me</code> profile fetching.", td_style)],
        [Paragraph("<code>api/routes/session.py</code>", td_code_style), Paragraph("Active session management and live activity telemetry stream endpoint.", td_style)],
        [Paragraph("<code>api/routes/lesson.py</code>", td_code_style), Paragraph("Generates and serves RAG-augmented study notes for curriculum nodes.", td_style)],
        [Paragraph("<code>api/routes/quiz.py</code>", td_code_style), Paragraph("3-part challenge generation, hint requests, submission evaluation, and node advance.", td_style)],
        [Paragraph("<code>api/routes/progress.py</code>", td_code_style), Paragraph("Knowledge graph prerequisite tree and learner mastery status endpoint.", td_style)],
        [Paragraph("<code>api/routes/final_exam.py</code>", td_code_style), Paragraph("3-phase standardized certification exam endpoint (Theory, Writing, Portfolio).", td_style)],
        [Paragraph("<code>api/routes/settings.py</code>", td_code_style), Paragraph("Model provider switching (Ollama Cloud/Local, OpenRouter) and live key validation.", td_style)],
        [Paragraph("<code>agents/orchestrator.py</code>", td_code_style), Paragraph("Master workflow state machine coordinator dispatching tasks to specialized agents.", td_style)],
        [Paragraph("<code>agents/lesson_agent.py</code>", td_code_style), Paragraph("Synthesizes structured, RAG-grounded study notes from vector search chunks.", td_style)],
        [Paragraph("<code>agents/quiz_agent.py</code>", td_code_style), Paragraph("Authors dynamic 3-part quizzes and generates progressive deduplicated hints.", td_style)],
        [Paragraph("<code>agents/evaluator_agent.py</code>", td_code_style), Paragraph("Evaluates student answers across semantic reasoning and rubric compliance.", td_style)],
        [Paragraph("<code>core/curriculum.py</code>", td_code_style), Paragraph("36-node knowledge graph ontology, Bloom levels, continuous weights, and prerequisites.", td_style)],
        [Paragraph("<code>core/scoring.py</code>", td_code_style), Paragraph("Implements the 5-variable adaptive scoring algorithm and rubric matching.", td_style)],
        [Paragraph("<code>core/state_machine.py</code>", td_code_style), Paragraph("Finite state machine transitions (Onboarding → Lesson → Quiz → Evaluation).", td_style)],
        [Paragraph("<code>core/learner_profile.py</code>", td_code_style), Paragraph("Learner mastery map, fail streak counters, and preferences management.", td_style)],
        [Paragraph("<code>backend/model_manager.py</code>", td_code_style), Paragraph("Multi-backend LLM inference router with live health check and fallback synthesizers.", td_style)],
        [Paragraph("<code>backend/activity_tracker.py</code>", td_code_style), Paragraph("Captures real-time telemetry events for streaming to the UI activity drawer.", td_style)],
        [Paragraph("<code>rag/vector_store.py</code>", td_code_style), Paragraph("ChromaDB vector collection management, document chunking, and semantic querying.", td_style)],
        [Paragraph("<code>db/storage.py</code>", td_code_style), Paragraph("SQLite database CRUD operations, user profile saving, and session lifecycle.", td_style)],
        [Paragraph("<code>db/models.py</code>", td_code_style), Paragraph("SQLAlchemy ORM database models and Pydantic request/response schemas.", td_style)],
        [Paragraph("<code>data/curriculum_tree.json</code>", td_code_style), Paragraph("Knowledge tree dataset with 36 nodes, difficulty tiers, and evaluation rubrics.", td_style)],
        [Paragraph("<code>ui/static/css/app.css</code>", td_code_style), Paragraph("Token-driven custom CSS system (Geist + JetBrains Mono, amber accent).", td_style)],
        [Paragraph("<code>ui/static/index.html</code>", td_code_style), Paragraph("Single-page application layout shell, brand mark, navigation tabs, and agent drawer.", td_style)],
        [Paragraph("<code>ui/static/js/app.js</code>", td_code_style), Paragraph("Frontend application controller, client router, and API fetch wrapper.", td_style)],
        [Paragraph("<code>ui/static/js/views/</code>", td_code_style), Paragraph("View renderers: <code>lesson.js</code>, <code>quiz.js</code>, <code>score_card.js</code>, <code>login.js</code>, etc.", td_style)],
        [Paragraph("<code>tests/test_api.py</code>", td_code_style), Paragraph("Automated integration test suite verifying auth, RAG, quizzes, and hints.", td_style)]
    ]

    file_table = Table(file_rows, colWidths=[140, 380])
    file_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_alt]),
    ]))
    story.append(file_table)
    story.append(PageBreak())

    # ================= PAGE 3 =================
    # --- Section 6: In-Depth Code Explanation ---
    story.append(Paragraph("6. In-Depth Code Explanations &amp; Implementation Logic", h1_style))
    story.append(Paragraph(
        "This section details the critical algorithms and architectural patterns powering Project ROAR's backend and agent coordination:",
        body_style
    ))

    # 6.1 Orchestrator & State Machine
    story.append(Paragraph("6.1 State Transition Controller &amp; DAG Unlocking (<code>core/state_machine.py</code>)", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> Student state is represented by the <code>TutorState</code> dataclass. When a user requests a lesson or submits answers, the <code>StateTransitionController</code> validates phase legality. "
        "Upon scoring &ge; S_pass (50%–70%), the node is recorded in <code>profile.completed_nodes</code>. The orchestrator queries <code>curriculum_graph.get_unlocked_nodes()</code>, filtering nodes whose <code>prerequisites</code> are fully satisfied, dynamically determining the next available topics.",
        body_style
    ))

    # 6.2 RAG Vector Store & Lesson Agent
    story.append(Paragraph("6.2 Semantic Vector Search &amp; RAG Synthesis (<code>agents/lesson_agent.py</code>)", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> When <code>LessonAgent.generate_lesson_notes()</code> runs, it executes <code>vector_store.query_similar(query, n_results=3)</code> against ChromaDB using cosine distance over chunked research documents. "
        "The retrieved context is injected into an LLM prompt conditioned on the student's experience tier (Beginner vs. Expert) and Bloom taxonomy level, outputting structured Markdown with real worked examples and anti-patterns.",
        body_style
    ))

    # 6.3 Dynamic Quiz & Deduplicated Scaffolding
    story.append(Paragraph("6.3 Dynamic 3-Part Challenge &amp; Progressive Hint Deduplication (<code>agents/quiz_agent.py</code>)", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> The Quiz Agent generates a structured JSON object containing three questions calibrated by weight. "
        "When the student clicks 'Hint', <code>generate_hint()</code> inspects <code>state.delivered_hints</code>, injects past hints into the LLM prompt with a strict anti-repetition directive, and checks for word-overlap (Jaccard similarity &gt; 0.70). "
        "If a duplicate is detected, it falls back to a deterministic, level-indexed progressive hint (Level 1 Intuition → Level 2 Rules → Level 3 Tactical Guidance).",
        body_style
    ))

    # 6.4 5-Variable Scoring Algorithm Implementation
    story.append(Paragraph("6.4 Evaluator Engine &amp; Penalty Calculus (<code>core/scoring.py</code> &amp; <code>evaluator_agent.py</code>)", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> <code>EvaluatorAgent.evaluate_submission()</code> executes two evaluators in parallel: "
        "(1) An LLM judge evaluates semantic depth (S_semantic), and (2) deterministic regex functions inspect rubric key concepts and structural markers (S_rule). "
        "The scoring engine applies overtime penalties (P_time) if the duration exceeds T = 180 + 60 &times; weight seconds, scaffolding deductions (P_hint = 0.05 &times; hints_used), and fail-streak penalties (P_retry).",
        body_style
    ))


    # 6.5 Multi-Provider LLM Router
    story.append(Paragraph("6.5 Multi-Provider LLM Inference Router (<code>backend/model_manager.py</code>)", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> <code>ModelManager.generate_async()</code> routes requests dynamically based on the active provider setting: "
        "Ollama Cloud Web API (<code>https://api.ollama.com/api/generate</code> with Bearer token authentication), local Ollama (<code>11434</code>), or OpenRouter (<code>https://openrouter.ai/api/v1/chat/completions</code>). "
        "It measures roundtrip latency via high-resolution timers, captures token usage counts, streams live telemetry to <code>ActivityTracker</code>, and activates dynamic fallback synthesizers if upstream providers experience network jitter.",
        body_style
    ))

    # 6.6 Frontend Reactive Controller
    story.append(Paragraph("6.6 Frontend SPA Architecture &amp; Telemetry Stream (<code>ui/static/js/app.js</code>)", h2_style))
    story.append(Paragraph(
        "<b>Workflow:</b> Built without heavy bundlers or node runtime dependencies using pure ES6 modules and custom CSS design tokens. "
        "<code>app.js</code> manages client routing (Study, Progress Graph, Model Settings, Final Exam), injects Bearer tokens on all fetch calls, updates live countdown timers, and renders real-time agent activity feeds via SVG status indicators.",
        body_style
    ))

    # --- Section 7: Quality Assurance & Research Telemetry ---
    story.append(Paragraph("7. Quality Assurance, Testing &amp; Research Telemetry", h1_style))
    story.append(Paragraph(
        "Every student attempt logs granular analytics into SQLite (<code>research_metrics</code> and <code>analytics_events</code>) to support academic research in adaptive learning trajectories. "
        "The entire system is continuously verified via automated integration tests: <code>pytest tests/test_api.py -v</code> (100% passing across authentication, RAG lessons, 3-part challenges, and progressive hints).",
        body_style
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF report at: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Project_ROAR_Complete_Report.pdf")
    build_pdf_report(out)
