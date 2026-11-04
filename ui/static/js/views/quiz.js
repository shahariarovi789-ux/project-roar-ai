// ui/static/js/views/quiz.js
/**
 * Project ROAR: Posh & Sophisticated Multi-Question Socratic Quiz View.
 * Editorial luxury meets high-stakes assessment and progressive scaffolding.
 */

export function renderQuizView(container, { quizData, onSubmitAnswer, onRequestHint, onRegenerateQuiz }) {
  let timerInterval = null;
  let secondsElapsed = 0;
  const timeBudget = quizData.time_budget_seconds || 240;
  let hintsUsed = 0;

  const questions = quizData.questions || [
    {
      id: 'q1',
      type: 'mcq',
      title: 'Question 1: Scenario & Core Concept',
      question: `How does ${quizData.topic_title} guide model behavior?`,
      options: [
        'A) Token sampling control',
        'B) Clear instructions & constraint conditioning',
        'C) Permanent weight modification',
        'D) Bypassing model safety filters'
      ],
    },
    {
      id: 'q2',
      type: 'writing',
      title: 'Question 2: Applied Prompt Construction',
      question: `Write a structured prompt demonstrating ${quizData.topic_title}.`
    },
    {
      id: 'q3',
      type: 'writing',
      title: 'Question 3: Failure Diagnosis & Repair',
      question: `Diagnose a vague prompt for ${quizData.topic_title}, then write your corrected version.`
    },
  ];

  const qTypeLabel = (q) => (q.type === 'mcq' || q.options) ? 'Multiple Choice' : 'Prompt Synthesis';

  container.innerHTML = `
    <div class="quiz-view-wrapper">

      <!-- Quiz Header Card -->
      <header class="quiz-hero-card">
        <div class="quiz-hero-breadcrumb-row">
          <div class="lesson-breadcrumb">
            <span class="lesson-cat-badge">Assessment</span>
            <span class="lesson-breadcrumb-sep">/</span>
            <span class="lesson-path-label">${quizData.topic_title}</span>
            <span class="meta-pill tier-pill">Tier ${quizData.difficulty_tier || 1}</span>
          </div>

          <!-- Telemetry: Timer & Hint Budget -->
          <div class="quiz-telemetry-cluster">
            <div class="quiz-timer-pill" id="quiz-timer-pill" title="Time elapsed">
              <span class="quiz-timer-dot" id="quiz-timer-dot"></span>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/><path stroke-linecap="round" stroke-width="2" d="M12 6v6l4 2"/></svg>
              <span id="quiz-timer" class="quiz-timer-val">00:00</span>
              <span class="quiz-timer-limit">/ ${Math.round(timeBudget)}s</span>
            </div>

            <div class="quiz-hints-pill" title="Available Socratic hints">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
              <span>Hints:</span>
              <span id="hint-counter" class="quiz-hint-val">0/3</span>
            </div>
          </div>
        </div>

        <div class="quiz-hero-body">
          <div class="lesson-title-area">
            <h1 class="lesson-heading">${quizData.topic_title}</h1>
            <div class="lesson-sub-meta">
              <span class="meta-pill">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                ${questions.length} Socratic Questions
              </span>
              <span class="meta-pill">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                Pass Threshold: ${Math.round((quizData.passing_threshold || 0.60) * 100)}%
              </span>
            </div>
          </div>
        </div>
      </header>

      <!-- Guided mode callout -->
      ${quizData.guided_mode_active ? `
        <div class="quiz-guided-banner">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg>
          <div>
            <strong>Guided Scaffolding Active.</strong> The Socratic agent has prepared adaptive hints. Click the hint button on any question if you need conceptual clues.
          </div>
        </div>
      ` : ''}

      <!-- Questions Form -->
      <form id="multi-quiz-form" class="quiz-form">

        ${questions.map((q, idx) => `
          <div class="quiz-question-card" data-card-idx="${idx + 1}">
            
            <!-- Left Accent Indicator -->
            <div class="quiz-card-accent-bar ${idx === 0 ? 'accent-gold' : 'accent-muted'}"></div>

            <!-- Card Header: Index, Title, Type, and Dedicated Hint Trigger -->
            <div class="quiz-card-header">
              <div class="quiz-card-header-left">
                <span class="quiz-q-chip">Q${idx + 1}</span>
                <span class="quiz-q-title">${q.title || `Question ${idx + 1}`}</span>
              </div>
              <div class="quiz-card-header-right">
                <button type="button" class="btn-q-hint btn-posh-ghost" data-qidx="${idx + 1}" title="Request Socratic clue for Question ${idx + 1}">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
                  <span>Hint for Q${idx + 1}</span>
                </button>
                <span class="quiz-type-badge ${q.type === 'mcq' || q.options ? 'type-mcq' : 'type-writing'}">
                  ${qTypeLabel(q)}
                </span>
              </div>
            </div>

            <!-- Question Prompt Body -->
            <div class="quiz-prompt-body">
              <p>${q.question}</p>
            </div>

            <!-- Input area -->
            ${(q.type === 'mcq' || q.options) && q.options?.length
              ? `<div class="quiz-options-group">
                  ${q.options.map((opt, oi) => `
                    <label class="option-card">
                      <input type="radio" name="q_${q.id || idx}" value="${opt.charAt(0)}" required class="option-radio-input">
                      <div class="option-radio">
                        <div class="option-radio-dot"></div>
                      </div>
                      <div class="option-title">${opt}</div>
                    </label>
                  `).join('')}
                </div>`
              : `<div class="quiz-textarea-wrapper">
                  <textarea
                    name="q_${q.id || idx}"
                    rows="5"
                    required
                    class="quiz-field-textarea"
                    placeholder="Formulate your structured engineered prompt response here…"
                  ></textarea>
                  <div class="quiz-textarea-footer">
                    <span>Markdown supported · Focus on clear constraints & context</span>
                  </div>
                </div>`
            }

            <!-- Dedicated Per-Question Hints Accordion -->
            <div id="q-hints-${idx + 1}" class="quiz-hints-accordion"></div>
          </div>
        `).join('')}

        <!-- Bottom Action Bar -->
        <footer class="quiz-action-bar">
          <button type="button" id="btn-regen-quiz" class="btn-posh-ghost" title="Formulate fresh question set">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            <span>Regenerate Challenge</span>
          </button>
          <button type="submit" id="btn-submit-quiz" class="btn-posh-primary lg">
            <span>Submit for Socratic Evaluation</span>
            <svg class="arrow-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </footer>
      </form>

    </div>
  `;

  // Focus tracking & selection interaction
  const quizForm = document.getElementById('multi-quiz-form');
  quizForm.addEventListener('change', (e) => {
    if (e.target.type === 'radio') {
      const group = e.target.closest('.quiz-options-group');
      if (group) {
        group.querySelectorAll('.option-card').forEach(card => card.classList.remove('selected'));
      }
      e.target.closest('.option-card')?.classList.add('selected');
    }
  });

  quizForm.addEventListener('focusin', (e) => {
    const card = e.target.closest('.quiz-question-card');
    if (card) {
      document.querySelectorAll('.quiz-card-accent-bar').forEach(bar => {
        bar.classList.remove('active-focus');
      });
      const bar = card.querySelector('.quiz-card-accent-bar');
      if (bar) bar.classList.add('active-focus');
    }
  });

  // Timer
  const timerEl = document.getElementById('quiz-timer');
  const timerDot = document.getElementById('quiz-timer-dot');
  timerInterval = setInterval(() => {
    secondsElapsed++;
    const mm = String(Math.floor(secondsElapsed / 60)).padStart(2, '0');
    const ss = String(secondsElapsed % 60).padStart(2, '0');
    if (timerEl) {
      timerEl.textContent = `${mm}:${ss}`;
      if (secondsElapsed > timeBudget) {
        timerEl.style.color = 'var(--c-danger)';
        if (timerDot) timerDot.style.background = 'var(--c-danger)';
      } else if (secondsElapsed > timeBudget * 0.75) {
        timerEl.style.color = 'var(--c-accent)';
        if (timerDot) timerDot.style.background = 'var(--c-accent)';
      }
    }
  }, 1000);

  // Update hint buttons state
  const updateAllHintButtons = () => {
    const isMax = (hintsUsed >= 3);
    document.querySelectorAll('.btn-q-hint').forEach(b => {
      if (isMax) {
        b.disabled = true;
        b.querySelector('span').textContent = 'Hints Exhausted (3/3)';
        b.classList.add('disabled');
      }
    });
    const counter = document.getElementById('hint-counter');
    if (counter) {
      counter.textContent = `${hintsUsed}/3`;
      if (hintsUsed >= 3) counter.style.color = 'var(--c-danger)';
      else if (hintsUsed >= 2) counter.style.color = 'var(--c-accent)';
    }
  };

  const fetchAndRenderHint = async (qIdx, targetContainer) => {
    if (hintsUsed >= 3) return;

    // Show loading stub
    const loadingEl = document.createElement('div');
    loadingEl.className = 'quiz-hint-card hint-card-enter loading';
    loadingEl.innerHTML = `
      <span class="spinner-sm"></span>
      <span style="color:var(--c-text-2);font-size:13px;font-family:var(--font-mono);">Synthesizing progressive Socratic hint for Q${qIdx}…</span>
    `;
    targetContainer.appendChild(loadingEl);

    try {
      const res = await onRequestHint(qIdx);
      loadingEl.remove();
      if (res?.hint) {
        hintsUsed = res.hints_used;
        const cleanHint = (res.hint || '')
          .replace(/^(?:Hint\s*#?\d*[:\-]\s*|\*\*Hint\s*#?\d*[:\-]?\*\*\s*|💡\s*)/i, '')
          .trim();
        const el = document.createElement('div');
        el.className = 'quiz-hint-card hint-card-enter';
        el.innerHTML = `
          <div class="hint-header-row">
            <span class="quiz-hint-badge">Hint #${hintsUsed} · Q${qIdx}</span>
            <span class="hint-scaffold-tag">Cognitive Scaffolding</span>
          </div>
          <div class="hint-content-body">${cleanHint}</div>
        `;
        targetContainer.appendChild(el);
        updateAllHintButtons();
      }
    } catch (err) {
      loadingEl.remove();
      alert('Failed to retrieve hint: ' + err.message);
    }
  };

  // Bind dedicated per-question hint buttons
  document.querySelectorAll('.btn-q-hint').forEach(btn => {
    btn.onclick = (e) => {
      e.preventDefault();
      const qIdx = Number(btn.getAttribute('data-qidx')) || 1;
      const targetContainer = document.getElementById(`q-hints-${qIdx}`);
      if (targetContainer) {
        fetchAndRenderHint(qIdx, targetContainer);
      }
    };
  });

  // Regen quiz
  const regenQuizBtn = document.getElementById('btn-regen-quiz');
  if (regenQuizBtn) {
    regenQuizBtn.onclick = () => {
      clearInterval(timerInterval);
      regenQuizBtn.disabled = true;
      regenQuizBtn.innerHTML = `<span class="spinner-sm"></span> <span>Synthesizing new challenge…</span>`;
      onRegenerateQuiz();
    };
  }

  // Submit quiz
  quizForm.onsubmit = async (e) => {
    e.preventDefault();
    clearInterval(timerInterval);
    const submitBtn = document.getElementById('btn-submit-quiz');
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner-sm"></span> <span>Evaluating Socratic Responses…</span>`;
    const fd = new FormData(e.target);
    const answersMap = {};
    questions.forEach((q, idx) => {
      answersMap[q.id || `q${idx + 1}`] = (fd.get(`q_${q.id || idx}`) || '').trim();
    });
    try {
      await onSubmitAnswer(answersMap, { timeElapsed: secondsElapsed, hintsUsed });
    } catch (err) {
      alert('Evaluation failed: ' + err.message);
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<span>Submit for Socratic Evaluation</span><svg class="arrow-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>`;
    }
  };
}
