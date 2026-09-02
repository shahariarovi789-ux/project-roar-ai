// ui/static/js/views/quiz.js
/**
 * Project ROAR — Multi-question dynamic quiz view.
 * Dedicated, prominent per-question hint buttons for Question 1, Question 2, and Question 3.
 */

export function renderQuizView(container, { quizData, onSubmitAnswer, onRequestHint, onRegenerateQuiz }) {
  let timerInterval  = null;
  let secondsElapsed = 0;
  const timeBudget   = quizData.time_budget_seconds || 240;
  let hintsUsed      = 0;

  const questions = quizData.questions || [
    {
      id: 'q1', type: 'mcq', title: 'Question 1: Scenario & Core Concept',
      question: `How does ${quizData.topic_title} guide model behavior?`,
      options: ['A) Token sampling control', 'B) Clear instructions & constraint conditioning', 'C) Permanent weight modification', 'D) Bypassing model safety filters'],
    },
    { id: 'q2', type: 'writing', title: 'Question 2: Applied Prompt Construction', question: `Write a structured prompt demonstrating ${quizData.topic_title}.` },
    { id: 'q3', type: 'writing', title: 'Question 3: Failure Diagnosis & Repair', question: `Diagnose a vague prompt for ${quizData.topic_title}, then write your corrected version.` },
  ];

  const qTypeLabel = (q) => (q.type === 'mcq' || q.options) ? 'Multiple choice' : 'Prompt writing';
  const qTypeColor = (q) => (q.type === 'mcq' || q.options)
    ? 'color:#A5B4FC;background:rgba(165,180,252,0.14);border:1px solid rgba(165,180,252,0.3);'
    : 'color:#FBBF24;background:rgba(251,191,36,0.14);border:1px solid rgba(251,191,36,0.3);';

  container.innerHTML = `
    <div class="animate-in" style="width:100%;max-width:760px;display:flex;flex-direction:column;gap:0;">

      <!-- Header row -->
      <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:24px;flex-wrap:wrap;">
        <div>
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:9px;flex-wrap:wrap;">
            <span class="chip chip-accent">Assessment · ${questions.length} Questions</span>
            <span class="chip chip-muted">Tier ${quizData.difficulty_tier}</span>
            <span style="font-family:var(--font-mono);font-size:11px;font-weight:600;color:var(--c-text-3);">
              Pass ≥ ${Math.round((quizData.passing_threshold || 0.60) * 100)}%
            </span>
          </div>
          <h1 style="font-size:22px;font-weight:800;color:var(--c-text);letter-spacing:-0.025em;margin:0;">${quizData.topic_title}</h1>
        </div>

        <!-- Controls: timer + hints budget badge -->
        <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
          <div style="display:flex;align-items:center;gap:6px;font-family:var(--font-mono);font-size:12px;padding:6px 14px;border:1px solid rgba(255,255,255,0.14);border-radius:var(--r-sm);background:var(--c-surface);box-shadow:0 2px 8px rgba(0,0,0,0.3);">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:13px;height:13px;color:var(--c-text-3);flex-shrink:0;"><circle cx="12" cy="12" r="10" stroke-width="2"/><path stroke-linecap="round" stroke-width="2" d="M12 6v6l4 2"/></svg>
            <span id="quiz-timer" style="font-weight:700;color:var(--c-success);letter-spacing:0.02em;">00:00</span>
            <span style="color:var(--c-text-3);">/ ${Math.round(timeBudget)}s</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;font-family:var(--font-mono);font-size:11px;padding:6px 12px;border:1px solid rgba(251,191,36,0.25);border-radius:var(--r-sm);background:rgba(251,191,36,0.08);color:var(--c-text-2);">
            <span>💡 Hints:</span>
            <span id="hint-counter" style="font-weight:800;color:var(--c-accent);">0/3</span>
          </div>
        </div>
      </div>

      <!-- Guided mode banner -->
      ${quizData.guided_mode_active ? `
        <div style="display:flex;align-items:center;gap:12px;padding:12px 16px;border:1px solid rgba(251,146,60,0.35);border-radius:var(--r-md);background:rgba(251,146,60,0.08);margin-bottom:20px;box-shadow:0 4px 14px rgba(0,0,0,0.3);">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:16px;height:16px;color:var(--c-amber);flex-shrink:0;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg>
          <span style="font-size:13px;color:var(--c-text-2);"><strong style="color:var(--c-amber);">Guided Mode Active.</strong> Click the Hint button on any question if you need scaffolding assistance.</span>
        </div>
      ` : ''}

      <!-- Questions Form -->
      <form id="multi-quiz-form" style="display:flex;flex-direction:column;gap:18px;">

        ${questions.map((q, idx) => `
          <div class="card stagger-item stagger-${Math.min(4, idx + 1)}" style="padding:26px 30px;position:relative;overflow:hidden;">
            
            <!-- Accent left border -->
            <div style="position:absolute;left:0;top:0;bottom:0;width:4px;background:${idx === 0 ? 'var(--c-accent)' : 'rgba(255,255,255,0.12)'};border-radius:var(--r-lg) 0 0 var(--r-lg);"></div>

            <!-- Question Header with Question Number, Title, Type Badge, and Dedicated Hint Button -->
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:10px;">
              <div style="display:flex;align-items:center;gap:12px;">
                <span style="
                  width:28px;height:28px;border-radius:6px;
                  background:linear-gradient(135deg, #FDE047 0%, #F59E0B 100%);
                  display:flex;align-items:center;justify-content:center;
                  font-family:var(--font-mono);font-size:13px;font-weight:800;color:#0B0E17;
                  flex-shrink:0;
                  box-shadow:0 2px 8px rgba(0,0,0,0.4);
                ">Q${idx + 1}</span>
                <span style="font-size:15px;font-weight:700;color:var(--c-text);">${q.title || `Question ${idx + 1}`}</span>
              </div>
              <div style="display:flex;align-items:center;gap:8px;">
                <button type="button" class="btn-q-hint btn btn-ghost" data-qidx="${idx + 1}" style="font-size:12px;padding:5px 12px;height:auto;gap:6px;line-height:1;border-color:rgba(251,191,36,0.3);color:var(--c-text);">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:13px;height:13px;flex-shrink:0;color:var(--c-accent);"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
                  <span>Hint for Q${idx + 1}</span>
                </button>
                <span style="font-family:var(--font-mono);font-size:10.5px;font-weight:600;padding:3px 9px;border-radius:var(--r-xs);${qTypeColor(q)}">${qTypeLabel(q)}</span>
              </div>
            </div>

            <!-- Question Text -->
            <p style="font-size:15px;color:var(--c-text-2);line-height:1.75;margin-bottom:18px;">${q.question}</p>

            <!-- Input area -->
            ${(q.type === 'mcq' || q.options) && q.options?.length
              ? `<div style="display:flex;flex-direction:column;gap:8px;">
                  ${q.options.map((opt, oi) => `
                    <label class="option-card" style="cursor:pointer;">
                      <input type="radio" name="q_${q.id || idx}" value="${opt.charAt(0)}" required style="display:none;">
                      <div class="option-radio"><div class="option-radio-dot"></div></div>
                      <div class="option-title" style="font-size:13.5px;font-weight:500;">${opt}</div>
                    </label>
                  `).join('')}
                </div>`
              : `<textarea
                  name="q_${q.id || idx}"
                  rows="5"
                  required
                  class="field-input"
                  placeholder="Write your structured prompt response here…"
                  style="font-size:13.5px;line-height:1.6;"
                ></textarea>
                <div style="display:flex;justify-content:flex-end;margin-top:6px;">
                  <span style="font-family:var(--font-mono);font-size:10px;color:var(--c-text-3);">Markdown syntax is supported</span>
                </div>`
            }

            <!-- Dedicated Per-Question Hints Accordion -->
            <div id="q-hints-${idx + 1}" style="display:flex;flex-direction:column;gap:10px;margin-top:14px;"></div>
          </div>
        `).join('')}

        <!-- Footer actions -->
        <div style="display:flex;align-items:center;justify-content:space-between;padding-top:8px;margin-top:4px;">
          <button type="button" id="btn-regen-quiz" class="btn btn-ghost" style="font-size:13px;">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:13px;height:13px;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            New Question Set
          </button>
          <button type="submit" id="btn-submit-quiz" class="btn btn-primary" style="padding:11px 28px;font-size:13.5px;">
            Submit for grading →
          </button>
        </div>
      </form>

    </div>
  `;

  // Radio option card selection
  document.getElementById('multi-quiz-form').addEventListener('change', (e) => {
    if (e.target.type === 'radio') {
      const name = e.target.name;
      document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
        r.closest('.option-card')?.classList.remove('selected');
      });
      e.target.closest('.option-card')?.classList.add('selected');
    }
  });

  // Focus tracking
  document.getElementById('multi-quiz-form').addEventListener('focusin', (e) => {
    const card = e.target.closest('.card');
    if (card) {
      const edge = card.querySelector('[style*="position:absolute;left:0"]');
      if (edge) edge.style.background = 'var(--c-accent)';
    }
  });

  // Timer
  const timerEl = document.getElementById('quiz-timer');
  timerInterval = setInterval(() => {
    secondsElapsed++;
    const mm = String(Math.floor(secondsElapsed / 60)).padStart(2, '0');
    const ss = String(secondsElapsed % 60).padStart(2, '0');
    if (timerEl) {
      timerEl.textContent = `${mm}:${ss}`;
      if (secondsElapsed > timeBudget) {
        timerEl.style.color = 'var(--c-danger)';
      } else if (secondsElapsed > timeBudget * 0.75) {
        timerEl.style.color = 'var(--c-amber)';
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
      }
    });
    const counter = document.getElementById('hint-counter');
    if (counter) {
      counter.textContent = `${hintsUsed}/3`;
      if (hintsUsed >= 3) counter.style.color = 'var(--c-danger)';
      else if (hintsUsed >= 2) counter.style.color = 'var(--c-amber)';
    }
  };

  const fetchAndRenderHint = async (qIdx, targetContainer) => {
    if (hintsUsed >= 3) return;

    // Show loading stub
    const loadingEl = document.createElement('div');
    loadingEl.className = 'hint-card hint-card-enter';
    loadingEl.innerHTML = `<span class="spinner" style="width:14px;height:14px;border-width:2px;"></span><span style="color:var(--c-text-2);font-size:13px;">Synthesizing progressive hint for Question ${qIdx}…</span>`;
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
        el.className = 'hint-card hint-card-enter';
        el.innerHTML = `
          <span class="hint-badge">Hint #${hintsUsed} · Q${qIdx}</span>
          <span style="color:var(--c-text-2);font-size:13px;line-height:1.65;">${cleanHint}</span>
        `;
        targetContainer.appendChild(el);
        updateAllHintButtons();
      }
    } catch (err) {
      loadingEl.remove();
      alert('Failed to get hint: ' + err.message);
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
      regenQuizBtn.innerHTML = `<span class="spinner" style="width:11px;height:11px;border-width:1.5px;"></span> Synthesizing new challenge…`;
      onRegenerateQuiz();
    };
  }

  // Submit quiz
  document.getElementById('multi-quiz-form').onsubmit = async (e) => {
    e.preventDefault();
    clearInterval(timerInterval);
    const btn = document.getElementById('btn-submit-quiz');
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner" style="width:14px;height:14px;border-width:2px;"></span> Evaluating…`;
    const fd = new FormData(e.target);
    const answersMap = {};
    questions.forEach((q, idx) => {
      answersMap[q.id || `q${idx + 1}`] = (fd.get(`q_${q.id || idx}`) || '').trim();
    });
    try {
      await onSubmitAnswer(answersMap, { timeElapsed: secondsElapsed, hintsUsed });
    } catch (err) {
      alert('Evaluation failed: ' + err.message);
      btn.disabled = false;
      btn.textContent = 'Submit for grading →';
    }
  };
}
