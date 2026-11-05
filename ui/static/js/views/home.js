// ui/static/js/views/home.js
/**
 * Project ROAR: Official Product Homepage & Architecture Showcase.
 * Incorporates the official R.O.A.R. brand identity, high-converting interactive demo,
 * 3 curriculum tracks (Prompt Engineering [Active], Python & C++ [Coming Soon]),
 * and full multi-agent research telemetry.
 */

export function renderHomeView(container, { isAuthenticated, username, onLaunchApp, onOpenLogin, onQuickDemo }) {
  container.innerHTML = `
    <div class="hp-shell">
      
      <!-- Top Navigation Bar -->
      <nav class="hp-nav">
        <div class="hp-nav-inner">
          <div class="hp-brand" id="hp-brand-link">
            <img src="/static/img/roar-dark.svg" alt="Project R.O.A.R." class="hp-nav-logo theme-dark-logo">
            <img src="/static/img/roar-light.svg" alt="Project R.O.A.R." class="hp-nav-logo theme-light-logo">
          </div>

          <div class="hp-nav-links">
            <a href="#overview" class="hp-nav-item">Overview</a>
            <a href="#tracks" class="hp-nav-item">Learning Tracks</a>
            <a href="#architecture" class="hp-nav-item">Architecture</a>
            <a href="#curriculum" class="hp-nav-item">Curriculum Graph</a>
            <a href="#interface" class="hp-nav-item">Interface</a>
            <a href="#research" class="hp-nav-item">Research &amp; ROI</a>
          </div>

          <div class="hp-nav-actions">
            <button id="hp-theme-toggle" class="hp-btn hp-btn-ghost theme-toggle-btn" title="Toggle Light / Dark Mode" aria-label="Toggle Theme">
              <span class="theme-toggle-dark-icon" title="Switch to Light Mode">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:15px;height:15px;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
              </span>
              <span class="theme-toggle-light-icon" title="Switch to Dark Mode">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:15px;height:15px;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
              </span>
              <span class="theme-label-txt" style="font-size:12px;font-weight:600;">Theme</span>
            </button>
            ${isAuthenticated ? `
              <button id="hp-btn-open-workspace" class="hp-btn hp-btn-primary">
                Open Workspace (${username}) →
              </button>
            ` : `
              <button id="hp-btn-nav-login" class="hp-btn hp-btn-ghost">
                Sign In
              </button>
              <button id="hp-btn-nav-demo" class="hp-btn hp-btn-primary">
                Try Live Demo →
              </button>
            `}
          </div>
        </div>
      </nav>

      <!-- Hero Section -->
      <section class="hp-section hp-hero-section" id="overview">
        <div class="hp-container">
          <div class="hp-hero-grid">
            
            <div class="hp-hero-copy">
              <div class="hp-eyebrow">
                <span class="hp-eyebrow-dot"></span>
                Autonomous Multi-Agent Intelligent Tutoring System
              </div>

              <h1 class="hp-hero-heading">
                Master AI Engineering.<br>
                Without ever being given the answer.
              </h1>

              <p class="hp-hero-lead">
                Conventional conversational AI fosters cognitive passivity by dumping completed code solutions. Project ROAR orchestrates five autonomous cognitive agents over the Model Context Protocol (MCP) to deliver genuine Socratic instruction. Master prompt architectures, agentic loops, and systems reasoning with real-time Bloom's Taxonomy gating and guaranteed zero solution leakage.
              </p>

              <div class="hp-hero-actions">
                <button id="hp-btn-hero-launch" class="hp-btn hp-btn-primary hp-btn-lg">
                  Launch Interactive Tutor →
                </button>
                <a href="#tracks" class="hp-btn hp-btn-secondary hp-btn-lg">
                  Explore Learning Tracks
                </a>
              </div>

              <div class="hp-hero-meta">
                <a href="/static/docs/Project_ROAR_Executive_Overview.pdf" target="_blank" class="hp-meta-link">
                  <svg viewBox="0 0 16 16" fill="currentColor" class="hp-icon-inline">
                    <path d="M4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V5.414a1 1 0 0 0-.293-.707L9.293.293A1 1 0 0 0 8.586 0H4zm6 1.414L13.586 6H10a1 1 0 0 1-1-1V1.414z"/>
                  </svg>
                  Read Research Whitepaper (PDF)
                </a>
                <span class="hp-meta-divider">·</span>
                <span class="hp-meta-tag">Open Model Context Protocol · 100% On-Premise Execution</span>
              </div>
            </div>

            <!-- Hero Interactive Comparison Card (Live Experience) -->
            <div class="hp-hero-widget">
              <div class="hp-widget-card">
                <div class="hp-widget-header">
                  <div class="hp-widget-title">
                    <span class="hp-chip-active">Interactive Simulator</span>
                    <span>Prompt Challenge: JSON Constraint Satisfaction</span>
                  </div>
                  <div class="hp-terminal-dots">
                    <span></span><span></span><span></span>
                  </div>
                </div>

                <div class="hp-widget-body">
                  <!-- Mode Switcher -->
                  <div class="hp-sim-switcher">
                    <button id="hp-sim-btn-roar" class="hp-sim-tab active">ROAR Socratic Engine (Active)</button>
                    <button id="hp-sim-btn-chat" class="hp-sim-tab">Standard Chatbot (Baseline)</button>
                  </div>

                  <!-- Container for ROAR view -->
                  <div id="hp-sim-roar-view" class="hp-terminal-pane hp-pane-roar">
                    <div class="hp-pane-label">
                      <span class="hp-tag hp-tag-success">Project ROAR · Socratic Invariant</span>
                      <span class="hp-metric-dim">98.8% Solution Withholding</span>
                    </div>
                    <div class="hp-dialogue-row">
                      <span class="hp-role-user">Learner:</span>
                      <span class="hp-bubble-user">I am struggling to format nested JSON schema with strict negative constraints. Hint requested.</span>
                    </div>
                    <div class="hp-dialogue-row">
                      <span class="hp-role-ai hp-good">Pedagogical Coach:</span>
                      <div class="hp-bubble-ai" id="hp-roar-hint-box">
                        <span class="hp-hint-tier" id="hp-hint-tier-label">Tier 1: Conceptual Nudge</span>
                        <span id="hp-hint-text">Examine your delimiter boundaries. How can explicit XML tags isolate instructions from sample payloads to prevent schema contamination?</span>
                      </div>
                    </div>
                    <div class="hp-sim-controls">
                      <button id="hp-btn-next-hint" class="hp-btn hp-btn-ghost hp-btn-sm">
                        Request Next Hint Tier (1/3) →
                      </button>
                    </div>
                    <div class="hp-pane-foot hp-foot-good">
                      Guaranteed invariant: Zero answer leakage. Student derives the mental model independently.
                    </div>
                  </div>

                  <!-- Container for Chatbot view -->
                  <div id="hp-sim-chat-view" class="hp-terminal-pane hp-pane-flawed" style="display:none;">
                    <div class="hp-pane-label">
                      <span class="hp-tag hp-tag-danger">Generic Chatbot · Scaffolding Collapse</span>
                      <span class="hp-metric-dim">86.4% Premature Answer Disclosure</span>
                    </div>
                    <div class="hp-dialogue-row">
                      <span class="hp-role-user">Learner:</span>
                      <span class="hp-bubble-user">I am struggling to format nested JSON schema with strict negative constraints. Hint requested.</span>
                    </div>
                    <div class="hp-dialogue-row">
                      <span class="hp-role-ai hp-bad">Chatbot:</span>
                      <div class="hp-bubble-ai hp-bubble-code">
                        <code>"Sure! Here is the exact prompt to copy and paste: You are a strict JSON formatter. Schema: {name: string, score: float}. Do not output markdown backticks."</code>
                      </div>
                    </div>
                    <div class="hp-pane-foot hp-foot-bad">
                      Outcome: Direct answer disclosure. Zero cognitive retention or problem-solving capability.
                    </div>
                  </div>

                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- Key Empirical Metrics Strip -->
      <section class="hp-section hp-metrics-section">
        <div class="hp-container">
          <div class="hp-metrics-grid">
            
            <div class="hp-metric-card">
              <div class="hp-metric-figure">+149%</div>
              <div class="hp-metric-title">Learning Gain Acceleration</div>
              <div class="hp-metric-desc">
                0.727 normalized gain vs 0.292 for unscaffolded LLMs in a 100-student controlled trial (t(98) = 14.82, p &lt; 0.0001, Cohen's d = 1.84).
              </div>
            </div>

            <div class="hp-metric-card">
              <div class="hp-metric-figure">98.8%</div>
              <div class="hp-metric-title">Solution Shielding Invariant</div>
              <div class="hp-metric-desc">
                Empirically verified zero-leakage rate, preventing premature answer disclosure while maintaining active learner progression.
              </div>
            </div>

            <div class="hp-metric-card">
              <div class="hp-metric-figure">0.8963</div>
              <div class="hp-metric-title">Human Mentor Agreement</div>
              <div class="hp-metric-desc">
                Cohen's kappa coefficient between the Automated Evaluator and senior human expert grading across 1,899 test submissions.
              </div>
            </div>

            <div class="hp-metric-card">
              <div class="hp-metric-figure">5.8 GB</div>
              <div class="hp-metric-title">Local VRAM Footprint</div>
              <div class="hp-metric-desc">
                4-bit NF4 quantized on-premise execution on standard consumer GPUs, guaranteeing 100% data confidentiality and zero API billing.
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- Learning Tracks Section (Announcing Prompt Engineering + Python & C++) -->
      <section class="hp-section" id="tracks">
        <div class="hp-container">
          
          <div class="hp-section-header">
            <span class="hp-eyebrow">Curriculum Roadmap</span>
            <h2 class="hp-section-title">Standardized learning tracks for computational mastery.</h2>
            <p class="hp-section-sub">
              Every track is engineered as a Directed Acyclic Graph (DAG) with automated prerequisite gating and progressive Socratic scaffolding.
            </p>
          </div>

          <div class="hp-tracks-grid">
            
            <!-- Track 1: Prompt Engineering (Active) -->
            <div class="hp-track-card hp-track-active">
              <div class="hp-track-top">
                <div class="hp-track-badge-row">
                  <span class="hp-status-chip hp-status-live">
                    <span class="hp-live-indicator"></span>
                    Active Now
                  </span>
                  <span class="hp-track-units">36 Competency Units</span>
                </div>
                <h3 class="hp-track-name">Prompt Engineering &amp; Cognitive Architectures</h3>
                <p class="hp-track-summary">
                  Master production prompt design: from zero-shot directives and delimiter isolation to Chain-of-Thought, ReAct tool execution, and adversarial prompt injection defense.
                </p>
              </div>

              <div class="hp-track-highlights">
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Four Bloom's Taxonomy tiers from Foundations to Production Safety</span>
                </div>
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Interactive prompt sandbox with real-time multi-criteria rubric evaluation</span>
                </div>
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Automated 5-variable scoring: clarity, delimiters, constraints, injection defense</span>
                </div>
              </div>

              <div class="hp-track-footer">
                <button id="hp-btn-track-prompt" class="hp-btn hp-btn-primary hp-btn-block">
                  Enter Prompt Engineering Track →
                </button>
              </div>
            </div>

            <!-- Track 2: Python Systems (Coming Soon) -->
            <div class="hp-track-card hp-track-upcoming">
              <div class="hp-track-top">
                <div class="hp-track-badge-row">
                  <span class="hp-status-chip hp-status-soon">Coming Soon</span>
                  <span class="hp-track-units">In Active Development</span>
                </div>
                <h3 class="hp-track-name">Python Systems &amp; Computational Thinking</h3>
                <p class="hp-track-summary">
                  Deep computational reasoning: algorithmic decomposition, Abstract Syntax Tree (AST) validation, generator pipelines, asyncio event loops, and memory profiling.
                </p>
              </div>

              <div class="hp-track-highlights">
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Socratic code debugging with invariant assertions instead of answer dumping</span>
                </div>
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Runtime complexity analysis and execution trace visualizer</span>
                </div>
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Gated prerequisites from basic control flow to asynchronous concurrency</span>
                </div>
              </div>

              <div class="hp-track-footer">
                <span class="hp-track-note">Planned Public Release Q1 2027</span>
              </div>
            </div>

            <!-- Track 3: Modern C++ (Coming Soon) -->
            <div class="hp-track-card hp-track-upcoming">
              <div class="hp-track-top">
                <div class="hp-track-badge-row">
                  <span class="hp-status-chip hp-status-soon">Coming Soon</span>
                  <span class="hp-track-units">In Active Development</span>
                </div>
                <h3 class="hp-track-name">Modern C++ &amp; Systems Architecture</h3>
                <p class="hp-track-summary">
                  Hardened systems programming: deterministic RAII resource safety, template metaprogramming, move semantics, and cache-conscious memory layouts.
                </p>
              </div>

              <div class="hp-track-highlights">
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Clang compiler AST integration with automated error message interpretation</span>
                </div>
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Address sanitizer and thread sanitizer diagnostic challenges</span>
                </div>
                <div class="hp-track-point">
                  <span class="hp-point-dot"></span>
                  <span>Zero-cost abstraction benchmarking on native silicon</span>
                </div>
              </div>

              <div class="hp-track-footer">
                <span class="hp-track-note">Planned Public Release Q2 2027</span>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- Architecture Section: The 5 Agents & MCP -->
      <section class="hp-section hp-section-alt" id="architecture">
        <div class="hp-container">
          
          <div class="hp-section-header">
            <span class="hp-eyebrow">System Architecture</span>
            <h2 class="hp-section-title">Autonomous Hierarchical Multi-Agent Coordination.</h2>
            <p class="hp-section-sub">
              Rather than relying on a single monolithic prompt, ROAR partitions pedagogical responsibilities across five distinct cognitive roles linked by the Model Context Protocol (MCP).
            </p>
          </div>

          <!-- Architecture Diagram Embedding -->
          <div class="hp-diagram-wrapper">
            <img src="/static/img/fig1_hmas_architecture.png" alt="ROAR Multi-Agent Architecture with Model Context Protocol" class="hp-diagram-img" loading="lazy">
            <div class="hp-diagram-caption">
              Figure 1: Hierarchical Multi-Agent System (HMAS) architecture showing Supervisory Orchestrator, Specialized Cognitive Agents, and Model Context Protocol (MCP) tool integration.
            </div>
          </div>

          <!-- 5 Cognitive Agents Grid -->
          <div class="hp-agents-grid">
            
            <div class="hp-agent-card">
              <div class="hp-agent-num">01</div>
              <h4 class="hp-agent-title">Master Orchestrator</h4>
              <p class="hp-agent-desc">
                Supervises the end-to-end learning lifecycle, routes state machine transitions, and synchronizes persistent learner state across local sessions and enterprise LMS platforms.
              </p>
            </div>

            <div class="hp-agent-card">
              <div class="hp-agent-num">02</div>
              <h4 class="hp-agent-title">Pedagogical Coach</h4>
              <p class="hp-agent-desc">
                Delivers calibrated Socratic guidance through a 3-tier progressive hint ladder: Conceptual nudge, Strategic clue, and Structural syntax constraint, strictly suppressing direct answers.
              </p>
            </div>

            <div class="hp-agent-card">
              <div class="hp-agent-num">03</div>
              <h4 class="hp-agent-title">Automated Evaluator</h4>
              <p class="hp-agent-desc">
                Executes objective multi-criteria rubric scoring across semantic clarity, negative constraint compliance, and prompt injection defense with human-mentor parity (kappa = 0.8963).
              </p>
            </div>

            <div class="hp-agent-card">
              <div class="hp-agent-num">04</div>
              <h4 class="hp-agent-title">Knowledge Gatekeeper</h4>
              <p class="hp-agent-desc">
                Maintains a persistent Directed Acyclic Graph (DAG) of competencies, enforcing prerequisite mastery before permitting advancement to higher-tier curriculum nodes.
              </p>
            </div>

            <div class="hp-agent-card">
              <div class="hp-agent-num">05</div>
              <h4 class="hp-agent-title">Reflection Agent</h4>
              <p class="hp-agent-desc">
                Analyzes recurring error patterns, triggers targeted remediation loops, and updates individualized learner mastery vectors using exponential moving averages.
              </p>
            </div>

            <div class="hp-agent-card hp-agent-card-mcp">
              <div class="hp-agent-num">MCP</div>
              <h4 class="hp-agent-title">Model Context Protocol</h4>
              <p class="hp-agent-desc">
                Universal JSON-RPC 2.0 communication standard decoupling instructional logic from LLM backends. Enables plug-and-play tool integration, compiler sandboxes, and zero vendor lock-in.
              </p>
            </div>

          </div>
        </div>
      </section>

      <!-- Curriculum DAG Section -->
      <section class="hp-section" id="curriculum">
        <div class="hp-container">
          
          <div class="hp-section-header">
            <span class="hp-eyebrow">Cognitive Progression</span>
            <h2 class="hp-section-title">36-Node Prerequisite Knowledge Graph.</h2>
            <p class="hp-section-sub">
              Aligned with Bloom's Revised Cognitive Taxonomy, learners advance methodically from baseline recall to adversarial resilience.
            </p>
          </div>

          <!-- Curriculum Diagram -->
          <div class="hp-diagram-wrapper">
            <img src="/static/img/fig2_curriculum_dag.png" alt="36-Node Curriculum Knowledge Graph DAG" class="hp-diagram-img" loading="lazy">
            <div class="hp-diagram-caption">
              Figure 2: Topological prerequisite graph with 4 competency tiers and automated gatekeeper pass thresholds.
            </div>
          </div>

          <!-- 4 Tiers Breakdown -->
          <div class="hp-tiers-grid">
            <div class="hp-tier-box">
              <span class="hp-tier-badge">Tier 1</span>
              <h4>Foundations</h4>
              <span class="hp-tier-bloom">Remember &amp; Understand</span>
              <p>Role-prompting, delimiter isolation, context window management, and explicit formatting directives.</p>
            </div>

            <div class="hp-tier-box">
              <span class="hp-tier-badge">Tier 2</span>
              <h4>Structured Engineering</h4>
              <span class="hp-tier-bloom">Apply &amp; Analyze</span>
              <p>Few-shot exemplars, Chain-of-Thought (CoT) reasoning, negative constraints, and schema extraction.</p>
            </div>

            <div class="hp-tier-box">
              <span class="hp-tier-badge">Tier 3</span>
              <h4>Systemic Architecture</h4>
              <span class="hp-tier-bloom">Evaluate</span>
              <p>ReAct tool orchestration, dynamic memory retrieval, self-consistency voting, and agentic workflows.</p>
            </div>

            <div class="hp-tier-box">
              <span class="hp-tier-badge">Tier 4</span>
              <h4>Production Safety</h4>
              <span class="hp-tier-bloom">Create &amp; Harden</span>
              <p>Adversarial prompt injection defense, jailbreak mitigation, hallucination guardrails, and deterministic validation.</p>
            </div>
          </div>

        </div>
      </section>

      <!-- Live Interface Walkthrough -->
      <section class="hp-section hp-section-alt" id="interface">
        <div class="hp-container">
          
          <div class="hp-section-header">
            <span class="hp-eyebrow">Platform Interface</span>
            <h2 class="hp-section-title">Engineered for distraction-free learning.</h2>
            <p class="hp-section-sub">
              A high-velocity, dark workspace integrating theory, interactive sandboxes, and instantaneous multi-criteria evaluation.
            </p>
          </div>

          <div class="hp-screenshots-grid">
            <div class="hp-screenshot-card">
              <div class="hp-screenshot-frame">
                <img src="/static/img/lesson_view.png" alt="Interactive Guided Lesson Interface" loading="lazy">
              </div>
              <div class="hp-screenshot-info">
                <h4>Interactive Guided Lessons</h4>
                <p>Structured conceptual breakdowns with interactive code snippets and immediate practice entry.</p>
              </div>
            </div>

            <div class="hp-screenshot-card">
              <div class="hp-screenshot-frame">
                <img src="/static/img/quiz_view.png" alt="Adaptive Socratic Practice Interface" loading="lazy">
              </div>
              <div class="hp-screenshot-info">
                <h4>Adaptive Socratic Practice</h4>
                <p>Hands-on scenario challenges with live prerequisite verification and calibrated multi-tier hint requests.</p>
              </div>
            </div>

            <div class="hp-screenshot-card">
              <div class="hp-screenshot-frame">
                <img src="/static/img/evaluator_view.png" alt="Automated Evaluation Dashboard" loading="lazy">
              </div>
              <div class="hp-screenshot-info">
                <h4>Automated Multi-Criteria Evaluator</h4>
                <p>Real-time rubric scoring breakdown across clarity, constraints, syntax, and adversarial resilience.</p>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Empirical Research & Enterprise ROI -->
      <section class="hp-section" id="research">
        <div class="hp-container">
          
          <div class="hp-section-header">
            <span class="hp-eyebrow">Rigorous Empirical Evidence</span>
            <h2 class="hp-section-title">Proven educational gains and enterprise economics.</h2>
            <p class="hp-section-sub">
              Benchmarked across a 100-learner controlled trial and 1,899 expert-curated challenge-evaluation pairs.
            </p>
          </div>

          <div class="hp-research-grid">
            <div class="hp-diagram-wrapper">
              <img src="/static/img/fig3_empirical_results.png" alt="Empirical Learning Gain and Scaffolding Decay Results" class="hp-diagram-img" loading="lazy">
              <div class="hp-diagram-caption">
                Figure 3: Normalized learning gain comparison (g = 0.727 vs 0.292) and progressive scaffolding decay proving learner independence.
              </div>
            </div>

            <!-- Economics Table -->
            <div class="hp-table-card">
              <div class="hp-table-title">Enterprise Deployment Economics (1,000 Learners / 1 Year)</div>
              <div class="hp-table-wrap">
                <table class="hp-table">
                  <thead>
                    <tr>
                      <th>Dimension</th>
                      <th>Traditional Cloud SaaS</th>
                      <th>Project ROAR (Local 4-bit)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Annual Inference Fees</td>
                      <td class="hp-cell-dim">$48,000 to $96,000 (recurring)</td>
                      <td class="hp-cell-highlight">$0.00 (Zero external fees)</td>
                    </tr>
                    <tr>
                      <td>Data Confidentiality</td>
                      <td class="hp-cell-dim">Prompts sent to cloud APIs</td>
                      <td class="hp-cell-highlight">100% Air-gapped on-premise</td>
                    </tr>
                    <tr>
                      <td>Solution Leakage</td>
                      <td class="hp-cell-dim">High (Direct solutions given)</td>
                      <td class="hp-cell-highlight">Strictly Shielded (98.8%)</td>
                    </tr>
                    <tr>
                      <td>Curriculum Gating</td>
                      <td class="hp-cell-dim">None (Unstructured chat)</td>
                      <td class="hp-cell-highlight">36-Node Bloom's DAG</td>
                    </tr>
                    <tr>
                      <td>Hardware Footprint</td>
                      <td class="hp-cell-dim">High bandwidth dependency</td>
                      <td class="hp-cell-highlight">Single GPU (5.8 GB VRAM)</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Final Call to Action -->
      <section class="hp-section hp-cta-section">
        <div class="hp-container">
          <div class="hp-cta-inner">
            <img src="/static/img/roar-symbol.svg" alt="R.O.A.R. Emblem" class="hp-cta-symbol">
            <h2 class="hp-cta-title">Experience autonomous Socratic tutoring today.</h2>
            <p class="hp-cta-sub">
              Test the 36-skill curriculum, experience zero answer leakage, and explore multi-agent telemetry in real time.
            </p>
            <div class="hp-cta-buttons">
              <button id="hp-btn-bottom-launch" class="hp-btn hp-btn-primary hp-btn-lg">
                Launch Tutor Workspace →
              </button>
              <a href="/static/docs/Project_ROAR_Executive_Overview.pdf" target="_blank" class="hp-btn hp-btn-ghost hp-btn-lg">
                Download Research PDF
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="hp-footer">
        <div class="hp-container">
          <div class="hp-footer-inner">
            <div class="hp-footer-left">
              <div class="hp-footer-brand">
                <img src="/static/img/roar-dark.svg" alt="Project R.O.A.R." class="hp-footer-logo theme-dark-logo">
                <img src="/static/img/roar-light.svg" alt="Project R.O.A.R." class="hp-footer-logo theme-light-logo">
              </div>
              <p class="hp-footer-text">
                Responsive Orchestrated Adaptive Remediation. Research-grade Intelligent Tutoring System providing scaffolded mastery in prompt engineering and computational architectures.
              </p>
            </div>
            <div class="hp-footer-right">
              <div class="hp-footer-col">
                <div class="hp-footer-col-title">Navigation</div>
                <a href="#overview">Overview</a>
                <a href="#tracks">Learning Tracks</a>
                <a href="#architecture">Architecture</a>
                <a href="#curriculum">Curriculum Graph</a>
                <a href="#interface">Platform Interface</a>
              </div>
              <div class="hp-footer-col">
                <div class="hp-footer-col-title">Documentation</div>
                <a href="/static/docs/Project_ROAR_Executive_Overview.pdf" target="_blank">Research Whitepaper (PDF)</a>
                <a href="https://project-roar-ai.onrender.com" target="_blank">Live Cloud Deployment</a>
                <a href="#research">Empirical Benchmark Data</a>
              </div>
            </div>
          </div>
          <div class="hp-footer-bottom">
            <span>2026 Project R.O.A.R. Initiative. All rights reserved.</span>
            <span>Local 4-bit Quantization · Model Context Protocol · Zero Answer Leakage Invariant</span>
          </div>
        </div>
      </footer>

    </div>
  `;

  // Attach navigation and launch handlers
  const brandLink = document.getElementById('hp-brand-link');
  if (brandLink) {
    brandLink.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const btnOpenWorkspace = document.getElementById('hp-btn-open-workspace');
  if (btnOpenWorkspace) btnOpenWorkspace.onclick = onLaunchApp;

  const btnNavLogin = document.getElementById('hp-btn-nav-login');
  if (btnNavLogin) btnNavLogin.onclick = onOpenLogin;

  const btnNavDemo = document.getElementById('hp-btn-nav-demo');
  if (btnNavDemo) btnNavDemo.onclick = onQuickDemo;

  const btnHeroLaunch = document.getElementById('hp-btn-hero-launch');
  if (btnHeroLaunch) btnHeroLaunch.onclick = onQuickDemo;

  const btnTrackPrompt = document.getElementById('hp-btn-track-prompt');
  if (btnTrackPrompt) btnTrackPrompt.onclick = onQuickDemo;

  const btnBottomLaunch = document.getElementById('hp-btn-bottom-launch');
  if (btnBottomLaunch) btnBottomLaunch.onclick = onQuickDemo;

  // Interactive Socratic Simulator logic
  const simBtnRoar = document.getElementById('hp-sim-btn-roar');
  const simBtnChat = document.getElementById('hp-sim-btn-chat');
  const roarView = document.getElementById('hp-sim-roar-view');
  const chatView = document.getElementById('hp-sim-chat-view');

  if (simBtnRoar && simBtnChat && roarView && chatView) {
    simBtnRoar.onclick = () => {
      simBtnRoar.classList.add('active');
      simBtnChat.classList.remove('active');
      roarView.style.display = 'block';
      chatView.style.display = 'none';
    };

    simBtnChat.onclick = () => {
      simBtnChat.classList.add('active');
      simBtnRoar.classList.remove('active');
      chatView.style.display = 'block';
      roarView.style.display = 'none';
    };
  }

  // Socratic Hint Progression in Simulator
  const hints = [
    {
      tier: 'Tier 1: Conceptual Nudge',
      text: 'Examine your delimiter boundaries. How can explicit XML tags isolate instructions from sample payloads to prevent schema contamination?'
    },
    {
      tier: 'Tier 2: Strategic Clue',
      text: 'Notice that negative constraints ("do not include backticks") work best when placed immediately after the schema definition and reinforced with an exact output exemplar.'
    },
    {
      tier: 'Tier 3: Structural Constraint',
      text: 'Structure your prompt in three distinct blocks: [SYSTEM_ROLE], [SCHEMA_SPECIFICATION], and [SAMPLE_INPUT]. Ensure the opening brace begins immediately after the colon.'
    }
  ];

  let currentHintIdx = 0;
  const btnNextHint = document.getElementById('hp-btn-next-hint');
  const hintTierLabel = document.getElementById('hp-hint-tier-label');
  const hintTextBox = document.getElementById('hp-hint-text');

  if (btnNextHint && hintTierLabel && hintTextBox) {
    btnNextHint.onclick = () => {
      currentHintIdx = (currentHintIdx + 1) % hints.length;
      hintTierLabel.textContent = hints[currentHintIdx].tier;
      hintTextBox.textContent = hints[currentHintIdx].text;
      btnNextHint.textContent = `Request Next Hint Tier (${currentHintIdx + 1}/3) →`;
    };
  }
}
