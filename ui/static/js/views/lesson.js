// ui/static/js/views/lesson.js
/**
 * Project ROAR: Accredited Educational Study Canvas.
 * Inspired by world-class learning platforms (Brilliant, Coursera, Stripe Docs).
 * Replaces generic AI bento boxes with high-impact pedagogical components:
 * - Unified 2-column educational workspace (eliminates all wasted screen space)
 * - Structured Learning Objectives banner
 * - Interactive Before/After Prompt Transformation with simulated model output
 * - 3 Actionable Golden Rules concept cards
 * - Socratic Knowledge Check (active self-reflection before quiz)
 * - Sticky Study Companion Rail (Table of Contents, quick actions, assessment target)
 */

export function renderLessonView(container, { lessonData, onStartQuiz, onSkipToQuiz, onRegenerateLesson, isExpert }) {
  const isPassed = Boolean(lessonData.is_passed);
  const rawMarkdown = lessonData.lesson_markdown || '';
  const wordCount = rawMarkdown.split(/\s+/).filter(Boolean).length;
  const readMinutes = Math.max(1, Math.round(wordCount / 180));

  const bloomColorMap = {
    'Remember':   { hex: '#818CF8', label: 'Foundational Recall' },
    'Understand': { hex: '#38BDF8', label: 'Conceptual Comprehension' },
    'Apply':      { hex: '#34D399', label: 'Hands-on Application' },
    'Analyze':    { hex: '#FB923C', label: 'Critical Deconstruction' },
    'Evaluate':   { hex: '#F472B6', label: 'Strategic Evaluation' },
    'Create':     { hex: '#FBBF24', label: 'Autonomous Synthesis' },
  };

  const bloom = bloomColorMap[lessonData.bloom_level] || { hex: 'var(--c-accent)', label: 'Conceptual Comprehension' };

  // Parse structured pedagogical components from markdown
  const parsed = parseLessonMarkdown(rawMarkdown, lessonData);

  container.innerHTML = `
    <div class="edu-study-layout">

      <!-- ======================================================== -->
      <!-- PRIMARY LEARNING COLUMN                                   -->
      <!-- ======================================================== -->
      <div class="edu-learning-main">

        <!-- Course / Module Context Banner -->
        <header class="edu-module-header">
          <div class="edu-module-breadcrumb">
            <span class="edu-module-badge">${lessonData.category || 'Foundations'}</span>
            <span class="edu-breadcrumb-sep">›</span>
            <span class="edu-lesson-track">Tier ${lessonData.difficulty_tier || 1} Topic</span>
            ${isPassed
              ? `<span class="edu-status-pill mastered">
                   <svg class="pill-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
                   Mastered
                 </span>`
              : `<span class="edu-status-pill in-progress">
                   <span class="edu-pulse-dot"></span>
                   In Progress
                 </span>`
            }
          </div>

          <h1 class="edu-lesson-title">${lessonData.topic_title}</h1>

          <p class="edu-lesson-subtitle">
            ${parsed.subtitle}
          </p>

          <div class="edu-lesson-meta-bar">
            <div class="edu-meta-item">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/><path stroke-linecap="round" stroke-width="2" d="M12 6v6l4 2"/></svg>
              <span>${readMinutes} min read (${wordCount} words)</span>
            </div>
            <div class="edu-meta-item">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
              <span style="color:${bloom.hex};font-weight:600;">${bloom.label}</span>
            </div>
            <div class="edu-meta-item">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
              <span>RAG Verified Corpus</span>
            </div>
          </div>
        </header>

        <!-- Learning Objectives Card -->
        <section class="edu-objectives-card">
          <div class="edu-objectives-header">
            <div class="edu-obj-icon-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <div>
              <div class="edu-obj-title">Learning Objectives</div>
              <div class="edu-obj-subtitle">What you will master in this lesson</div>
            </div>
          </div>
          <ul class="edu-obj-list">
            ${parsed.objectives.map(obj => `<li>${obj}</li>`).join('')}
          </ul>
        </section>

        <!-- Main Section 1: The Core Mental Model -->
        <section class="edu-section" id="sec-mental-model">
          <div class="edu-section-head">
            <span class="edu-section-badge">Part 1</span>
            <h2 class="edu-section-title">Core Mental Model</h2>
          </div>
          <div class="edu-prose">
            ${parsed.mentalModelHtml}
            <div class="edu-callout tip">
              <div class="edu-callout-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </div>
              <div class="edu-callout-content">
                <strong>Socratic Insight:</strong> Autoregressive language models do not reason with innate intent—they compute conditional probability distributions over next-token vectors. Every token you place in a prompt acts as a mathematical constraint filter over the response space.
              </div>
            </div>
          </div>
          <div class="edu-section-nav-footer">
            <button type="button" class="edu-btn-section-next" data-target="sec-worked-example">
              <span>Continue to Part 2: Worked Example</span>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
          </div>
        </section>

        <!-- Main Section 2: Interactive Prompt Transformation (Before vs After) -->
        <section class="edu-section" id="sec-worked-example">
          <div class="edu-section-head">
            <span class="edu-section-badge">Part 2</span>
            <h2 class="edu-section-title">Worked Example: Prompt Transformation</h2>
          </div>
          <p class="edu-section-desc">
            Observe the dramatic difference in generative reliability when transitioning from an ambiguous query to a fortified, production-grade prompt.
          </p>

          <div class="edu-comparison-container">
            <!-- Flawed Prompt Card -->
            <div class="edu-comparison-card flawed">
              <div class="edu-comp-header">
                <div class="edu-comp-label">
                  <span class="edu-comp-icon bad">✕</span>
                  <span class="edu-comp-title">Flawed (Vague Prompt)</span>
                </div>
                <span class="edu-comp-tag bad">High Variance &amp; Hallucination Risk</span>
              </div>
              <div class="edu-comp-code-box">
                <pre><code>${escapeHtml(parsed.flawedPrompt)}</code></pre>
              </div>
              <div class="edu-comp-critique bad">
                <strong>Why it fails:</strong> Lacks domain persona, output length limits, and negative boundaries. The model defaults to unpredictable length and conversational preamble.
              </div>
            </div>

            <!-- Fortified Prompt Card -->
            <div class="edu-comparison-card fortified">
              <div class="edu-comp-header">
                <div class="edu-comp-label">
                  <span class="edu-comp-icon good">✓</span>
                  <span class="edu-comp-title">Fortified (Engineered Prompt)</span>
                </div>
                <span class="edu-comp-tag good">Deterministic Production Output</span>
              </div>
              <div class="edu-comp-code-box">
                <pre><code>${escapeHtml(parsed.fortifiedPrompt)}</code></pre>
              </div>
              <div class="edu-comp-critique good">
                <strong>Why it succeeds:</strong> ${escapeHtml(parsed.whyItWorks)}
              </div>
            </div>
          </div>

          <!-- Interactive Simulated Output Comparison Drawer -->
          <div class="edu-sim-drawer">
            <button type="button" class="edu-btn-sim-toggle" id="btn-toggle-sim">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
              <span id="sim-toggle-label">Compare Simulated Model Responses</span>
              <svg class="sim-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
            <div class="edu-sim-content" id="sim-content-box" style="display:none;">
              <div class="edu-sim-grid">
                <div class="edu-sim-card bad">
                  <div class="edu-sim-head">Response to Vague Prompt</div>
                  <div class="edu-sim-body">
                    <em>"Certainly! Here is some information about that topic. There are many important aspects to keep in mind when studying this. First of all, researchers have noted several key factors over time..."</em>
                    <div class="edu-sim-verdict bad">❌ 180 tokens wasted on conversational fluff; zero structured data.</div>
                  </div>
                </div>
                <div class="edu-sim-card good">
                  <div class="edu-sim-head">Response to Fortified Prompt</div>
                  <div class="edu-sim-body">
                    • <strong>Primary Driver:</strong> 34% reduction in downstream hallucination via strict boundary conditioning.<br>
                    • <strong>Format Compliance:</strong> 100% adherence to 3-bullet constraint with zero preamble.<br>
                    • <strong>Recommendation:</strong> Integrate input delimiters across all automated API pipelines.
                    <div class="edu-sim-verdict good">✓ 42 tokens total; clean bullet structure ready for downstream parser.</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="edu-section-nav-footer">
            <button type="button" class="edu-btn-section-next" data-target="sec-golden-rules">
              <span>Continue to Part 3: 3 Actionable Golden Rules</span>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
          </div>
        </section>

        <!-- Main Section 3: The 3 Actionable Golden Rules -->
        <section class="edu-section" id="sec-golden-rules">
          <div class="edu-section-head">
            <span class="edu-section-badge">Part 3</span>
            <h2 class="edu-section-title">The 3 Actionable Golden Rules</h2>
          </div>
          <p class="edu-section-desc">
            Apply these three core heuristics whenever constructing prompts for automated systems:
          </p>

          <div class="edu-rules-grid">
            ${parsed.rules.map((rule, idx) => `
              <div class="edu-rule-card">
                <div class="edu-rule-top">
                  <span class="edu-rule-number">0${idx + 1}</span>
                  <span class="edu-rule-tag">${rule.tag || 'Rule'}</span>
                </div>
                <h3 class="edu-rule-title">${rule.title}</h3>
                <p class="edu-rule-body">${rule.desc}</p>
              </div>
            `).join('')}
          </div>
          <div class="edu-section-nav-footer">
            <button type="button" class="edu-btn-section-next" data-target="sec-self-check">
              <span>Continue to Part 4: Socratic Self-Check</span>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
          </div>
        </section>

        <!-- Main Section 4: Socratic Self-Check -->
        <section class="edu-section" id="sec-self-check">
          <div class="edu-section-head">
            <span class="edu-section-badge">Part 4</span>
            <h2 class="edu-section-title">Socratic Knowledge Check</h2>
          </div>

          <div class="edu-self-check-card">
            <div class="edu-check-header">
              <span class="edu-check-badge">Self-Reflection Exercise</span>
              <span class="edu-check-meta">Check your conceptual understanding before the quiz</span>
            </div>
            <h3 class="edu-check-question">
              ${parsed.checkQuestion}
            </h3>
            <div class="edu-check-action-row">
              <button type="button" class="edu-btn-reveal" id="btn-reveal-reflection">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                <span>Reveal Socratic Analysis</span>
              </button>
            </div>
            <div class="edu-check-explanation" id="check-explanation-box" style="display:none;">
              <div class="edu-check-expl-body">
                <strong>Socratic Analysis:</strong> ${parsed.checkAnswer}
              </div>
            </div>
          </div>
          <div class="edu-section-nav-footer">
            <button type="button" class="edu-btn-section-next" data-target="sec-milestone">
              <span>Proceed to Assessment Quiz</span>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
          </div>
        </section>

        <!-- Lesson Milestone & Launch Assessment Card -->
        <footer class="edu-milestone-card" id="sec-milestone">
          <div class="edu-milestone-left">
            <div class="edu-milestone-flag">Lesson Milestone Complete</div>
            <h3 class="edu-milestone-title">Ready to verify your understanding?</h3>
            <p class="edu-milestone-desc">
              Test your mastery with 3 calibrated Socratic questions. Progressive hints and live reasoning feedback will be active.
            </p>
          </div>
          <button id="btn-bottom-quiz" class="edu-btn-primary lg">
            <span>${isPassed ? 'Retake Practice Quiz' : 'Start Practice Quiz (3 Questions)'}</span>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </footer>

      </div>


      <!-- ======================================================== -->
      <!-- STICKY STUDY COMPANION RAIL (RIGHT)                      -->
      <!-- ======================================================== -->
      <aside class="edu-companion-rail">
        
        <!-- Assessment Target Card -->
        <div class="edu-rail-card assessment-cta-card">
          <div class="rail-card-top">
            <span class="rail-card-badge">Assessment Ready</span>
            <span class="rail-tier-badge">Tier ${lessonData.difficulty_tier || 1}</span>
          </div>
          <div class="rail-target-title">${lessonData.topic_title}</div>
          <div class="rail-target-desc">
            ${isPassed
              ? 'Topic Mastered! You can retake the practice quiz anytime to sharpen your skills.'
              : 'Pass the 3-question evaluation to unlock subsequent curriculum nodes in this track.'
            }
          </div>
          <button id="btn-proceed-quiz" class="edu-btn-primary full-w">
            <span>${isPassed ? 'Retake Practice Quiz' : 'Start Practice Quiz →'}</span>
          </button>
          <div class="rail-meta-row">
            <span>Pass Threshold: <strong>60%</strong></span>
            <span>Est. Time: <strong>4 min</strong></span>
          </div>
        </div>

        <!-- Table of Contents ("In This Lesson") -->
        <div class="edu-rail-card">
          <div class="rail-card-title">In This Lesson</div>
          <nav class="edu-toc-nav">
            <a href="#sec-mental-model" class="edu-toc-link active">
              <span class="toc-step">01</span>
              <span class="toc-label">Core Mental Model</span>
            </a>
            <a href="#sec-worked-example" class="edu-toc-link">
              <span class="toc-step">02</span>
              <span class="toc-label">Worked Example</span>
            </a>
            <a href="#sec-golden-rules" class="edu-toc-link">
              <span class="toc-step">03</span>
              <span class="toc-label">3 Actionable Golden Rules</span>
            </a>
            <a href="#sec-self-check" class="edu-toc-link">
              <span class="toc-step">04</span>
              <span class="toc-label">Socratic Self-Check</span>
            </a>
          </nav>
        </div>

        <!-- Study Toolkit Card -->
        <div class="edu-rail-card">
          <div class="rail-card-title">Study Toolkit</div>
          <div class="edu-toolkit-group">
            <button id="btn-copy-notes" class="edu-toolkit-btn" title="Copy markdown to clipboard">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
              <span>Copy Lesson Notes</span>
            </button>
            <button id="btn-download-notes" class="edu-toolkit-btn" title="Export markdown guide">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
              <span>Download Guide (.md)</span>
            </button>
            <button id="btn-regen-lesson" class="edu-toolkit-btn" title="Synthesize alternative explanation">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              <span>Alternative Explanation</span>
            </button>
            ${isExpert && !isPassed
              ? `<button id="btn-expert-skip" class="edu-toolkit-btn skip" title="Skip to assessment">Skip to Assessment →</button>`
              : ''
            }
          </div>
        </div>

        <!-- Academic Telemetry & Model Details (Discreet Collapsible) -->
        <details class="edu-rail-card edu-telemetry-details">
          <summary class="rail-card-title summary-toggle">
            <span>Model &amp; System Telemetry</span>
            <svg class="summary-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </summary>
          <div class="telemetry-info-body">
            <div class="telemetry-item">
              <span class="telemetry-k">Inference Agent:</span>
              <span class="telemetry-v">${lessonData.model_used || 'gpt-oss:20b'}</span>
            </div>
            <div class="telemetry-item">
              <span class="telemetry-k">Cognitive Domain:</span>
              <span class="telemetry-v" style="color:${bloom.hex};">${bloom.label}</span>
            </div>
            <div class="telemetry-item">
              <span class="telemetry-k">Taxonomy Weight:</span>
              <span class="telemetry-v">${lessonData.weight != null ? lessonData.weight : '1.0'}</span>
            </div>
            <div class="telemetry-item">
              <span class="telemetry-k">Round-trip Latency:</span>
              <span class="telemetry-v">${Math.round(lessonData.latency_ms || 0)}ms</span>
            </div>
            <div class="telemetry-item">
              <span class="telemetry-k">RAG Grounding:</span>
              <span class="telemetry-v" style="color:var(--c-success);">Verified Active</span>
            </div>
          </div>
        </details>

      </aside>

    </div>
  `;

  // Bind interactive elements
  const proceedBtn = document.getElementById('btn-proceed-quiz');
  if (proceedBtn) proceedBtn.onclick = onStartQuiz;

  const bottomBtn = document.getElementById('btn-bottom-quiz');
  if (bottomBtn) bottomBtn.onclick = onStartQuiz;

  const skipBtn = document.getElementById('btn-expert-skip');
  if (skipBtn) skipBtn.onclick = onSkipToQuiz;

  // Toggle simulated outputs
  const simToggleBtn = document.getElementById('btn-toggle-sim');
  const simContentBox = document.getElementById('sim-content-box');
  const simToggleLabel = document.getElementById('sim-toggle-label');
  if (simToggleBtn && simContentBox) {
    simToggleBtn.onclick = () => {
      const isHidden = simContentBox.style.display === 'none';
      simContentBox.style.display = isHidden ? 'block' : 'none';
      simToggleBtn.classList.toggle('active', isHidden);
      if (simToggleLabel) {
        simToggleLabel.textContent = isHidden ? 'Hide Simulated Output Comparison' : 'Compare Simulated Model Responses';
      }
    };
  }

  // Socratic self-check reveal
  const revealBtn = document.getElementById('btn-reveal-reflection');
  const explBox = document.getElementById('check-explanation-box');
  if (revealBtn && explBox) {
    revealBtn.onclick = () => {
      const isHidden = explBox.style.display === 'none';
      explBox.style.display = isHidden ? 'block' : 'none';
      revealBtn.innerHTML = isHidden
        ? `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg><span>Explanation Revealed</span>`
        : `<span>Reveal Socratic Analysis</span>`;
      revealBtn.classList.toggle('revealed', isHidden);
    };
  }

  // Copy notes
  const copyBtn = document.getElementById('btn-copy-notes');
  if (copyBtn) {
    copyBtn.onclick = async () => {
      try {
        await navigator.clipboard.writeText(rawMarkdown);
        copyBtn.innerHTML = `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color:var(--c-success);"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg><span style="color:var(--c-success);">Notes Copied!</span>`;
        setTimeout(() => {
          copyBtn.innerHTML = `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2"/></svg><span>Copy Lesson Notes</span>`;
        }, 2200);
      } catch (err) {
        alert('Could not copy notes to clipboard.');
      }
    };
  }

  // Download notes
  const downloadBtn = document.getElementById('btn-download-notes');
  if (downloadBtn) {
    downloadBtn.onclick = () => {
      const blob = new Blob([rawMarkdown], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${(lessonData.topic_title || 'study_notes').replace(/[^a-zA-Z0-9_-]/g, '_')}.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    };
  }

  // Regenerate
  const regenBtn = document.getElementById('btn-regen-lesson');
  if (regenBtn) {
    regenBtn.onclick = () => {
      regenBtn.disabled = true;
      regenBtn.innerHTML = `<span class="spinner-sm"></span> <span>Synthesizing…</span>`;
      onRegenerateLesson();
    };
  }

  // Smooth in-container scrolling to target section
  const viewScrollEl = document.getElementById('view-container');
  const scrollToTarget = (targetId) => {
    const targetEl = document.getElementById(targetId);
    if (!targetEl) return;

    if (viewScrollEl) {
      const targetRect = targetEl.getBoundingClientRect();
      const containerRect = viewScrollEl.getBoundingClientRect();
      const relativeTop = targetRect.top - containerRect.top + viewScrollEl.scrollTop - 24;
      viewScrollEl.scrollTo({ top: Math.max(0, relativeTop), behavior: 'smooth' });
    }

    // Secondary fallback to ensure scroll happens across all browser rendering modes
    try {
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (err) {}
  };

  // Wire Table of Contents links
  const tocLinks = container.querySelectorAll('.edu-toc-link');
  tocLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        const targetId = href.substring(1);
        scrollToTarget(targetId);
        tocLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
      }
    });
  });

  // Wire Next Section transition buttons
  const nextBtns = container.querySelectorAll('.edu-btn-section-next');
  nextBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = btn.getAttribute('data-target');
      if (targetId) {
        scrollToTarget(targetId);
      }
    });
  });

  // Scrollspy for table of contents
  const sections = ['sec-mental-model', 'sec-worked-example', 'sec-golden-rules', 'sec-self-check', 'sec-milestone']
    .map(id => document.getElementById(id))
    .filter(Boolean);

  const updateToc = () => {
    if (!viewScrollEl) return;
    let currentId = '';
    const scrollPos = viewScrollEl.scrollTop + 140;

    sections.forEach(sec => {
      const targetRect = sec.getBoundingClientRect();
      const containerRect = viewScrollEl.getBoundingClientRect();
      const relativeTop = targetRect.top - containerRect.top + viewScrollEl.scrollTop;
      if (relativeTop <= scrollPos) {
        currentId = sec.id;
      }
    });

    tocLinks.forEach(link => {
      const href = link.getAttribute('href');
      link.classList.toggle('active', href === `#${currentId}`);
    });
  };

  if (viewScrollEl) {
    viewScrollEl.addEventListener('scroll', updateToc, { passive: true });
    // Always start at top of new lesson
    viewScrollEl.scrollTop = 0;
  }
}

/**
 * Robust parser to extract educational sections from the lesson markdown.
 */
function parseLessonMarkdown(text, lessonData) {
  const clean = text.replace(/^#\s+[^\n]+\n+/, '');

  // Subtitle
  const subtitle = `Comprehensive study guide covering foundational mechanics, constraint conditioning, and production best practices for ${lessonData.topic_title.toLowerCase()}.`;

  // Learning Objectives
  const objectives = [
    `Understand ${lessonData.topic_title} as deterministic programming instructions rather than casual queries.`,
    `Identify key failure modes of vague prompts and how structural constraint conditioning prevents hallucination.`,
    `Apply the 3 core golden rules (Persona framing, concrete output limits, and input delimitation) in production.`
  ];

  // Part 1: Mental model
  let mentalModelHtml = '';
  const mmMatch = clean.match(/##\s*1\.[^\n]*\n([\s\S]*?)(?=\n##\s*2\.|\Z)/);
  if (mmMatch && window.marked) {
    mentalModelHtml = window.marked.parse(mmMatch[1].trim());
  } else {
    mentalModelHtml = `<p>A prompt is not just a search query—it is a structured program of natural language instructions that steers the probability distribution of an autoregressive language model toward accurate, deterministic outputs.</p>`;
  }

  // Part 2: Worked example
  let flawedPrompt = 'Explain science.';
  let fortifiedPrompt = 'You are a friendly science teacher. Explain the greenhouse effect in exactly 2 simple sentences using a glass greenhouse analogy. Do not include conversational preamble.';
  let whyItWorks = 'Defines a clear role, sets numeric constraints (2 sentences), and includes an explicit negative boundary.';

  const weMatch = clean.match(/##\s*2\.[^\n]*\n([\s\S]*?)(?=\n##\s*3\.|\Z)/);
  if (weMatch) {
    const weBlock = weMatch[1];
    const flawedM = weBlock.match(/#\s*(?:❌|Flawed|Before)[^\n]*\n([\s\S]*?)(?=#\s*(?:✅|Fortified|After)|```|\Z)/);
    if (flawedM && flawedM[1].trim()) {
      flawedPrompt = flawedM[1].trim().replace(/^["'`]+|["'`]+$/g, '');
    }

    const fortifiedM = weBlock.match(/#\s*(?:✅|Fortified|After)[^\n]*\n([\s\S]*?)(?=```|\Z)/);
    if (fortifiedM && fortifiedM[1].trim()) {
      fortifiedPrompt = fortifiedM[1].trim().replace(/^["'`]+|["'`]+$/g, '');
    }

    const whyM = weBlock.match(/[-*]\s*\*\*Why [iI]t [wW]orks\*\*:\s*([^\n]+)/);
    if (whyM && whyM[1].trim()) {
      whyItWorks = whyM[1].trim();
    }
  }

  // Part 3: Golden rules
  const rules = [
    {
      title: 'Assign a Specific Role',
      tag: 'Persona Conditioning',
      desc: 'Frame the model persona (e.g. Senior Systems Architect) to activate latent domain-specific vocabulary and analytical rigor.'
    },
    {
      title: 'Enforce Concrete Constraints',
      tag: 'Format & Length Bounds',
      desc: 'Explicitly specify output format (e.g. 3 bullets, strict JSON) and negative bounds (e.g. "Do not include conversational filler").'
    },
    {
      title: 'Isolate Variable Inputs',
      tag: 'Context Delimitation',
      desc: 'Wrap dynamic user input inside triple quotes or XML tags (e.g. &lt;context&gt;...&lt;/context&gt;) to cleanly separate instructions from variable user data.'
    }
  ];

  const grMatch = clean.match(/##\s*3\.[^\n]*\n([\s\S]*?)(?=\n##|\Z)/);
  if (grMatch) {
    const extracted = [];
    const ruleRegex = /\d+\.\s*\*\*([^*]+)\*\*[:\-]?\s*([^\n]+)/g;
    let match;
    while ((match = ruleRegex.exec(grMatch[1])) !== null) {
      extracted.push({
        title: escapeHtml(match[1].trim()),
        tag: `Rule ${extracted.length + 1}`,
        desc: escapeHtml(match[2].trim())
      });
    }
    if (extracted.length >= 2) {
      rules.splice(0, extracted.length, ...extracted);
    }
  }

  // Part 4: Self-check
  const checkQuestion = `Why is an explicit negative boundary (e.g. "Do not include conversational preamble") essential when incorporating an LLM into an automated software pipeline?`;
  const checkAnswer = `Instruction-tuned models have heavy conversational priors that default to pleasantries ("Certainly! I'd be happy to help with that"). In automated software pipelines, unconstrained pleasantries break downstream JSON/CSV parsers and unnecessarily waste latency and generation tokens.`;

  return {
    subtitle,
    objectives,
    mentalModelHtml,
    flawedPrompt,
    fortifiedPrompt,
    whyItWorks,
    rules,
    checkQuestion,
    checkAnswer
  };
}

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
