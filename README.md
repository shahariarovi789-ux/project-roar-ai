# Project ROAR: Grounded Multi-Agent Orchestration and Model Context Protocol for Adaptive Intelligent Tutoring in Prompt Engineering

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20%26%20Cloud-black.svg?logo=ollama&logoColor=white)](https://ollama.com/)
[![ChromaDB](https://img.shields.io/badge/Vector%20Store-ChromaDB-purple.svg)](https://www.trychroma.com/)
[![VRAM Footprint](https://img.shields.io/badge/VRAM%20Footprint-Sub--6GB%20%284.8GB%29-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Personalized Learning with Large Language Models: Addressing Uniformity and Enhancing Student-Centric Educational Responses**

*An open-source, air-gapped, research-grade Intelligent Tutoring System (ITS) designed to eliminate scaffolding collapse and deliver personalized education in prompt engineering.*

[Evaluation Report](evaluation/Project_ROAR_Evaluation_Report.pdf) • [Installation Guide](#installation-and-setup-guide) • [Architecture](#system-architecture) • [Research Benchmarks](#empirical-evaluation-and-research-benchmarks)

</div>

---

## 1. System Interface Preview

<div align="center">

### 1.1 Interactive Study Interface (RAG-Grounded Concept Guide & 36-Node DAG)
*Dynamic prerequisite gating with Bloom taxonomy alignment, live engine telemetry, and comparative before/after prompt demonstrations.*

![Interactive Study Interface](assets/screenshots/lesson_view.png)

---

### 1.2 Timed Assessment Sandbox (Multi-Modal Quiz & 3-Tier Scaffolding)
*Authentic prompt construction sandboxes paired with on-demand Socratic hint triggers that guide learners without spoiling solutions.*

![Timed Assessment Interface](assets/screenshots/quiz_view.png)

---

### 1.3 Automated Evaluator Feedback (Decomposed Formula & Remediation)
*Transparent multi-variable scoring model displaying semantic relevance, syntactic structure, time/streak penalties, and targeted remediation.*

![Evaluator Feedback Interface](assets/screenshots/evaluator_view.png)

</div>

---

## 2. Key System Capabilities

1. **Anti-Scaffolding Collapse (3-Tier Progressive Hints):** Generic conversational LLMs spoil direct answers, inducing passive cognitive offloading. Project ROAR enforces progressive cognitive scaffolding ($L1\text{ Socratic Analogy} \rightarrow L2\text{ Structural Rubric} \rightarrow L3\text{ Constrained Template}$).
2. **36-Node Dynamic Knowledge DAG:** Replaces response uniformity with topological prerequisite skill trees calibrated across 4 Bloom taxonomy cognitive tiers.
3. **Retrieval-Augmented Semantic Grounding:** ChromaDB vector integration reduces technical prompt syntax hallucinations by **$4.1\times$** ($1.2\%$ vs $24.8\%$).
4. **Sub-6GB Edge Optimization:** Operates 100% offline within a strict **$4,820\text{ MB}$ peak VRAM footprint** on consumer hardware (NVIDIA RTX 3060/4060 or Apple Silicon) at zero recurring cloud API cost.
5. **Human-Grade Grading Alignment:** Dual-stage Evaluator Agent achieves **Cohen's Kappa $\kappa = 0.8963$** and an **$F_1$-score of $95.8\%$** against human instructor grading.

---

## 3. System Architecture

```mermaid
graph TD
    subgraph Client["Interactive User Workspace (localhost:8000)"]
        UI["SPA Desktop Interface\n(Tailwind CSS + ES6 Modules + WebSockets)"]
    end

    subgraph Gateway["FastAPI Orchestration Gateway (/api/v1)"]
        AUTH["JWT Authentication & Security Middleware"]
        ORCH["5-Agent Asynchronous State Machine"]
    end

    subgraph Agents["Multi-Agent Pipeline"]
        OA["1. Onboarding Agent\nLearner Persona & Diagnostic Intake"]
        LA["2. Lesson Agent\nCalibrated Study Guide + Grounding"]
        QA["3. Quiz Agent\nScenario MCQs + Applied Prompt Sandboxes"]
        EA["4. Evaluator Agent\nSemantic Match + Structural Rule Check"]
        RA["5. RAG Agent\nChromaDB Semantic Vector Retrieval"]
    end

    subgraph Inference["Inference Backends"]
        OLL["Local Ollama Engine\n(gpt-oss:20b / gemma4:31b / qwen2.5)"]
        CLOUD["Ollama Cloud / Groq / OpenAI Fallback"]
    end

    subgraph Storage["Persistence & Graph Knowledge"]
        DB[(SQLite WAL Database\n8 Relational Tables)]
        VDB[(ChromaDB Vector Store\n1,899 Grounded QA Chunks)]
        DAG["curriculum_tree.json\n36 Topological Skill Nodes"]
    end

    UI -->|REST & WebSockets| AUTH
    AUTH --> ORCH
    ORCH --> OA & LA & QA & EA
    LA & QA & EA --> RA
    RA --> VDB
    OA & LA & QA & EA --> DB
    LA & QA & EA -->|Local Inference| OLL
    OLL -.->|API Fallback| CLOUD
    ORCH --> DAG
```

---

## 4. Research Methodology

The research methodology of Project ROAR is structured around six core scientific and engineering pillars:

<div align="center">
  <img src="assets/screenshots/methodology_flow_diagram.png" width="800" alt="Project ROAR Methodology Workflow Diagram"/>
  <p><i>Figure 4.1: Project ROAR 8-Step Adaptive Methodology & Agent-Student Feedback Loop.</i></p>
</div>

```
+---------------------------------------------------------------------------------------------------------+
|                                    PROJECT ROAR RESEARCH METHODOLOGY                                    |
+------------------------------------+-----------------------------------+--------------------------------+
| 1. Hierarchical Multi-Agent System | 2. Model Context Protocol (MCP)   | 3. Curriculum Knowledge Graph  |
| • Deterministic State Supervisor   | • Canonical `roar://` Resources   | • 36-Node Topological DAG      |
| • 7 Decoupled Cognitive Agents     | • Standardized JSON-RPC Tools     | • Bloom's Taxonomy Alignment   |
| • Anti-Answer-Leakage Isolation    | • 0% Context Drift Guarantee      | • Prerequisite Gate Validation |
+------------------------------------+-----------------------------------+--------------------------------+
| 4. Retrieval-Augmented Grounding   | 5. Adaptive Socratic Scaffolding  | 6. Dual-Stage Adaptive Scoring |
| • ChromaDB Vector Embedding Store  | • 3-Tier Progressive Hint Decay   | • Semantic Judge + Regex Rule  |
| • 1,899 Vetted Technical Chunks    | • Fail-Streak Remediation Trigger | • 5-Variable Mathematical Grade|
| • 4.1x Hallucination Reduction     | • Zero Direct Solution Spoilage   | • Cohen's Kappa κ = 0.8963     |
+------------------------------------+-----------------------------------+--------------------------------+
```

### 4.1 Hierarchical Multi-Agent Orchestration (HMAS)
Rather than relying on an unconstrained monolithic prompt—which suffers from severe instruction drift and answer leakage—Project ROAR employs a **Hierarchical Multi-Agent System (HMAS)**. Cognitive labor is strictly partitioned across 7 specialized agents:
1. **`TutorOrchestrator`:** Operates as the deterministic supervisory finite-state machine governing valid state transitions:
   $$\mathcal{T}: (\mathcal{S}_{\text{current}} \times \mathcal{E}_{\text{event}}) \longrightarrow \mathcal{S}_{\text{next}}$$
   Valid phases: $\text{ONBOARDING} \to \text{LESSON} \to \text{QUIZ} \to \text{EVALUATING} \to \text{NODE\_PASSED} \mid \text{NODE\_FAILED} \to \text{FINAL\_EXAM}$.
2. **`LessonAgent`:** Synthesizes pedagogical study guides calibrated to learner experience and prior fail streaks.
3. **`QuizAgent`:** Generates 3-tier challenge assessments (MCQs + prompt construction sandboxes) and progressive hints without solution leakage.
4. **`EvaluatorAgent`:** Grades submissions by decoupling deterministic rubric checks from semantic LLM-as-a-judge evaluation.
5. **`RAGAgent`:** Interfaces with ChromaDB vector store for factual retrieval.
6. **`HardwareScout`:** Scans host GPU/VRAM telemetry (macOS Metal / NVIDIA CUDA) to select optimal local model tiers.
7. **`OnboardingAgent`:** Conducts diagnostic intake questionnaires to initialize the learner profile.

### 4.2 Model Context Protocol (MCP 2.x) Integration
To eliminate in-memory state drift and tight cross-module coupling, Project ROAR integrates Anthropic's **Model Context Protocol (MCP)**:
* **Canonical Resources (`roar://...`):** Exposes live learner state (`roar://learner/{id}/profile`, `roar://learner/{id}/session`), topological curriculum structure (`roar://curriculum/dag`), and hardware telemetry (`roar://hardware/profile`). All agents read from a single canonical source of truth.
* **Standardized Tools:** All educational operations (`retrieve_grounding_context`, `verify_node_unlocked`, `compute_socratic_hint`, `grade_prompt_submission`, `update_learner_progress`) are exposed via strict Pydantic JSON Schemas, intercepting 100% of malformed parameters before reaching core logic.
* **Modularity:** Reduces direct cross-agent dependencies by **83.3%** while adding $<0.75\text{ ms}$ protocol overhead.

### 4.3 Curriculum Knowledge Graph & Topological Prerequisite Enforcement
The prompt engineering domain is formalized as a Directed Acyclic Graph (DAG) $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, where $|\mathcal{V}| = 36$ curriculum nodes.
* **Prerequisite Enforcement:** A target node $v$ is unlocked if and only if all parent dependencies are satisfied:
  $$\text{Unlocked}(v, \mathcal{C}) \iff \forall u \in \text{Parents}(v),\; u \in \mathcal{C}$$
  where $\mathcal{C}$ denotes the set of completed nodes with verified passing scores.
* **Cognitive Stratification:** Nodes are weighted continuously from $w \in [1.0, 4.0]$ and mapped to Bloom's Revised Taxonomy (Remember, Understand, Apply, Analyze, Evaluate, Create).

### 4.4 Retrieval-Augmented Generation (RAG) Grounding
To eliminate technical hallucinations on niche syntax (e.g. delimiter escaping, indirect prompt injection defenses, ReAct loops), ROAR integrates a persistent ChromaDB vector store indexing **1,899 vetted QA chunks and prompt engineering documentation**.
* Query embeddings retrieve the top-$k$ most relevant technical chunks using cosine similarity.
* Empirical ablation shows that RAG grounding reduces prompt engineering hallucinations from **24.8% down to 1.2%** ($4.1\times$ reduction).

### 4.5 Adaptive Socratic Scaffolding Engine
To prevent **scaffolding collapse** (where students passively copy AI solutions), the tutor never gives away the answer. Instead, it provides a 3-tier progressive hint sequence:
* **Level 1 (Socratic Concept):** High-level conceptual question or analogy directing attention to first principles.
* **Level 2 (Structural Rubric):** Explicit reminder of missing structural markers, delimiters, or output constraints.
* **Level 3 (Constrained Template):** Partial skeleton or template demonstrating format without providing semantic solutions.

### 4.6 Dual-Stage Evaluation & 5-Variable Adaptive Scoring
Submissions are evaluated through a two-stage decoupled grading pipeline:
1. **Stage 1 (Deterministic Rule Match):** Regex pattern extraction checks mandatory structural markers, negative constraints, and length thresholds to produce $S_{\text{rule}} \in [0, 1]$.
2. **Stage 2 (Semantic LLM-as-a-Judge):** An independent judge LLM evaluates conceptual correctness, reasoning depth, and edge-case handling to produce $S_{\text{semantic}} \in [0, 1]$.
3. **Composite Scoring:** Combined via the calibrated 5-variable adaptive formula:
   $$S_{\text{final}} = \max\left(0,\; \alpha S_{\text{sem}} + \beta S_{\text{rule}} - \gamma H - \delta T_{\text{penalty}} - \varepsilon R_{\text{fail}}\right)$$
   where $\alpha = 0.50$, $\beta = 0.50$, $\gamma = 0.05$, $\delta = 0.05$, and $\varepsilon = 0.01$.

---

## 5. Installation and Setup Guide

### 5.1 macOS (Apple Silicon & Intel)

```bash
# 1. Install prerequisites via Homebrew (if not already installed)
brew install python@3.11 git ollama

# 2. Clone the repository
git clone https://github.com/shahariarovi789-ux/project-roar-ai.git
cd project-roar-ai

# 3. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Configure environment variables
cp .env.example .env

# 6. (Optional: Local LLM) Pull model and start Ollama
ollama pull gpt-oss:20b
ollama serve

# 7. Start the PromptTutor server
python main.py
```
> Open **`http://localhost:8000`** in your browser.

---

### 5.2 Windows (Native PowerShell or WSL2)

#### Using Native PowerShell:
```powershell
# 1. Clone the repository
git clone https://github.com/shahariarovi789-ux/project-roar-ai.git
cd project-roar-ai

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Copy environment configuration
copy .env.example .env

# 5. Launch the application
python main.py
```

#### Using WSL2 (Ubuntu on Windows — Recommended for CUDA Acceleration):
```bash
# In WSL2 terminal:
sudo apt update && sudo apt install -y python3-pip python3-venv git
git clone https://github.com/shahariarovi789-ux/project-roar-ai.git
cd project-roar-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

### 5.3 Linux (Ubuntu / Debian / Fedora / Arch)

```bash
# 1. Install system dependencies (Debian/Ubuntu)
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl

# For Arch Linux: sudo pacman -S python python-pip git

# 2. Clone and enter repository
git clone https://github.com/shahariarovi789-ux/project-roar-ai.git
cd project-roar-ai

# 3. Setup virtual environment & dependencies
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Initialize configuration
cp .env.example .env

# 5. Run application
python main.py
```

---

### 5.4 Docker Containerization (Any Platform)

```bash
# Build and start containerized Project ROAR
docker build -t project-roar-ai .
docker run -d -p 8000:8000 --name prompt-tutor project-roar-ai

# Access at http://localhost:8000
```

---

## 6. Empirical Evaluation and Research Benchmarks

The system was evaluated using a rigorous 4-category benchmark suite:

| Evaluation Category | Benchmark Metric | Standard Baseline | Project ROAR | Scientific Impact |
| :--- | :--- | :---: | :---: | :--- |
| **1. Pedagogical Efficacy** | **Normalized Learning Gain ($g$)** | $g = 0.292$ *(Unscaffolded)* | **$g = 0.727$** | **$2.49\times$ higher retention** (+43.36% absolute mastery jump). |
| **1. Pedagogical Efficacy** | **Scaffolding Decay (36 Nodes)** | Constant High Reliance | **$-82.9\%$ Decay** | $2.53 \rightarrow 0.43\text{ hints/task}$; proves student autonomy. |
| **2. Architectural Ablations** | **No-RAG vs Full ROAR** | $24.8\%$ Hallucinations | **$1.2\%$ Hallucinations** | **$4.1\times$ reduction** in domain syntax errors via ChromaDB. |
| **2. Architectural Ablations** | **Monolithic vs 5-Agent Pipeline** | $42.0\%$ Answer Leakage | **$0.0\%$ Answer Leakage** | Eliminates prompt instruction drift and early answer spoiling. |
| **3. State Machine & Grading** | **Cohen's Kappa ($\kappa$) vs Human** | Ground Truth ($N=100$) | **$\kappa = 0.8963$ ($F_1 = 95.8\%$)** | Near-perfect statistical grading alignment with instructors. |
| **3. State Machine & Grading** | **Illegal DAG Traversal Rejection** | Free Navigation Spikes | **$100\%$ Out-of-Order Rejection** | Strictly gates prerequisite mastery before unlocking tiers. |
| **4. Edge Hardware Feasibility** | **Peak VRAM Footprint** | $6,144\text{ MB}$ Ceiling | **$4,820\text{ MB}$ ($1,324\text{ MB}$ Headroom)** | Verified sub-6GB compliance on consumer hardware. |

### Evaluation Visualizations:
<div align="center">
<table>
  <tr>
    <td align="center"><b>Normalized Learning Gain ($g$)</b></td>
    <td align="center"><b>Scaffolding Decay Curve</b></td>
  </tr>
  <tr>
    <td><img src="assets/screenshots/cat1_learning_gain.png" width="380"/></td>
    <td><img src="assets/screenshots/cat1_scaffolding_decay.png" width="380"/></td>
  </tr>
  <tr>
    <td align="center"><b>Architectural Ablation Comparison</b></td>
    <td align="center"><b>Peak VRAM Hardware Profile</b></td>
  </tr>
  <tr>
    <td><img src="assets/screenshots/cat2_ablation.png" width="380"/></td>
    <td><img src="assets/screenshots/cat4_vram.png" width="380"/></td>
  </tr>
</table>
</div>

---

## 7. Curriculum Knowledge Graph (36 Nodes)

The curriculum is structured as a Directed Acyclic Graph (DAG) across 4 Bloom taxonomy tiers:

```
Tier 1: Foundations & Syntax (11 Nodes, Weight: 1.0 - 1.5, Pass Threshold >= 50%)
├── 1. Introduction to Prompt Engineering
├── 2. Output Configuration (Temperature, Top-K, Top-P)
└── 3. Role & Delimiter Syntax

Tier 2: Prompt Engineering Techniques (15 Nodes, Weight: 1.8 - 2.8, Pass Threshold >= 60%)
├── 4. Zero-Shot & Few-Shot In-Context Learning
├── 5. System Prompting & Behavioral Conditioning
├── 6. Chain-of-Thought (CoT) & Step-Back Prompting
└── 7. Code Prompting (Generation, Debugging, Refactoring)

Tier 3: Advanced Reasoning & Autonomous Workflows (6 Nodes, Weight: 3.0 - 3.5, Pass Threshold >= 70%)
├── 8. Self-Consistency & Tree of Thoughts (ToT)
├── 9. ReAct (Reason + Act) Agentic Workflows
└── 10. Automated Prompt Optimization (APO)

Tier 4: Security, Robustness & Evaluation (4 Nodes, Weight: 3.8 - 4.0, Pass Threshold >= 75%)
├── 11. Jailbreak Defenses & Prompt Injection Mitigations
├── 12. Hallucination Reduction Strategies
└── 13. Capstone Summative Examination
```

---

## 8. Adaptive Multi-Variable Scoring Equation

Student prompt submissions are dynamically graded using a 5-variable mathematical model:

$$\boxed{S_{\text{final}} = \max\!\left(0,\; \alpha \cdot S_{\text{sem}} + \beta \cdot S_{\text{rule}} - \gamma \cdot H - \delta \cdot T_{\text{penalty}} - \varepsilon \cdot R_{\text{fail}}\right)}$$

* **$S_{\text{sem}}$ ($\alpha = 0.50$):** Semantic alignment evaluated via LLM-as-a-Judge with JSON schema enforcement.
* **$S_{\text{rule}}$ ($\beta = 0.50$):** Rule compliance matching structural constraint rubrics.
* **$H$ ($\gamma = 0.05$):** Progressive hint deduction ($0.05$ to $0.15$ for up to 3 requested hints).
* **$T_{\text{penalty}}$ ($\delta = 0.05$):** Time elapsed deduction beyond dynamic node budget ($T_{\text{budget}} = 60 + 20 \times W_{\text{node}}\text{ s}$).
* **$R_{\text{fail}}$ ($\varepsilon = 0.01$):** Consequent retry penalty ($\min(0.01 \times \text{streak},\; 0.05)$).

---

## 9. API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register new student profile |
| `POST` | `/api/v1/auth/login` | Authenticate and obtain JWT bearer token |
| `GET` | `/api/v1/lesson/{node_id}` | Fetch RAG-grounded lesson content for DAG node |
| `GET` | `/api/v1/quiz/{node_id}` | Generate adaptive scenario challenge and MCQs |
| `POST` | `/api/v1/quiz/submit` | Evaluate submission using 5-variable scoring engine |
| `POST` | `/api/v1/quiz/hint` | Request progressive Level 1/2/3 scaffolding hint |
| `GET` | `/api/v1/progress` | Fetch student mastery progress and unlocked DAG nodes |
| `GET` | `/api/v1/model/status` | Real-time hardware telemetry, active engine, and VRAM |
| `WS` | `/ws/{session_id}` | WebSocket token streaming for low-latency feedback |

> Interactive Swagger documentation available at: **`http://localhost:8000/docs`**

---

## 10. Repository Structure

```
.
├── agents/                       # Specialist Cognitive Agents
│   ├── orchestrator.py           # State machine supervisor agent
│   ├── mcp_adapter.py            # Model Context Protocol adapter
│   ├── lesson_agent.py           # Curriculum lesson generator
│   ├── quiz_agent.py             # Adaptive challenge builder
│   ├── evaluator_agent.py        # Semantic judge & rule scorer
│   ├── rag_agent.py              # ChromaDB vector retrieval
│   ├── hardware_scout.py         # Hardware & VRAM profiling agent
│   └── onboarding_agent.py       # Diagnostic profile intake
├── api/                          # FastAPI Gateway
│   ├── main.py                   # App initialization & lifespan
│   ├── middleware.py             # CORS & Auth middleware
│   └── routes/                   # REST route handlers
├── assets/screenshots/           # High-resolution UI & evaluation plots
├── backend/                      # Inference & Prompt Management
│   ├── model_manager.py          # Multi-backend LLM driver (Ollama/Cloud)
│   └── prompt_templates.py       # Sandboxed agent prompt templates
├── core/                         # Pedagogical Logic
│   ├── curriculum.py             # 36-node DAG graph traversal
│   ├── scoring.py                # 5-variable adaptive grading formula
│   └── state_machine.py          # State definitions & transition rules
├── data/                         # Data Stores & Ontologies
│   ├── curriculum_tree.json      # DAG node definitions & weights
│   ├── benchmark_testset.json    # Evaluation benchmark questions
│   └── rag_docs/                 # Domain documentation for ChromaDB
├── evaluation/                   # Empirical Evaluation Suite
│   ├── comprehensive_evaluation_suite.py  # Master 4-category runner
│   ├── mcp_comparative_benchmark.py       # With-MCP vs Without-MCP benchmark
│   ├── plot_mcp_comparison.py             # Radar & latency plot generator
│   ├── comprehensive_thesis_evaluation.ipynb # Interactive notebook
│   └── Project_ROAR_Evaluation_Report.pdf # 9-page formal report
├── mcp_server/                   # Model Context Protocol (MCP 2.x) Package
│   ├── server.py                 # FastMCP server with resources & tools
│   └── client.py                 # In-memory & protocol-compliant client
├── ui/static/                    # Odysseus-style SPA Frontend
│   ├── index.html                # Main workspace interface
│   ├── css/                      # Custom dark-mode styles
│   └── js/                       # Modular ES6 view controllers
├── Dockerfile                    # Production Docker container
├── render.yaml                   # Cloud deployment blueprint
├── requirements.txt              # Production Python dependencies
└── main.py                       # Application launcher
```

---

## 11. License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
<b>Department of Computer Science & Engineering</b><br/>
University of Liberal Arts Bangladesh (ULAB)
</div>
