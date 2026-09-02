// ui/static/js/views/onboarding.js
/**
 * Project ROAR — Onboarding Questionnaire Wizard.
 * High-contrast, developer-tool aesthetic with explicit button styling.
 */

export function renderOnboardingView(container, { onOnboardingComplete, token }) {
  const questions = [
    {
      key: 'name',
      title: 'Welcome to Project ROAR',
      subtitle: 'First, what should we call you? (Required)',
      type: 'text',
      placeholder: 'Enter your preferred name...'
    },
    {
      key: 'prior_experience',
      title: 'Experience Level',
      subtitle: 'What is your background with prompt engineering and LLMs?',
      type: 'choice',
      options: [
        { value: 'beginner', title: 'Beginner', desc: 'New to prompt engineering principles' },
        { value: 'intermediate', title: 'Intermediate', desc: 'Regularly craft prompts for daily workflows' },
        { value: 'expert', title: 'Expert', desc: 'Build LLM apps, fine-tune models, or design agentic systems' }
      ]
    },
    {
      key: 'prefers_examples',
      title: 'Learning Style Preference',
      subtitle: 'When mastering a new concept, what helps you more?',
      type: 'choice',
      options: [
        { value: true, title: 'Concrete Examples First', desc: 'Show me realistic prompts and outputs before the theory' },
        { value: false, title: 'Core Mental Model First', desc: 'Explain the underlying mathematical & attention theory first' }
      ]
    },
    {
      key: 'prefers_detailed',
      title: 'Explanation Depth',
      subtitle: 'How in-depth should lesson explanations be?',
      type: 'choice',
      options: [
        { value: true, title: 'Deep & Detailed', desc: '8–10 sentences exploring nuances, edge cases, and mechanics' },
        { value: false, title: 'Concise & Direct', desc: '4–6 sentences focusing strictly on actionable rules' }
      ]
    },
    {
      key: 'prefers_steps',
      title: 'Structure & Breakdown',
      subtitle: 'How do you prefer breakdowns formatted?',
      type: 'choice',
      options: [
        { value: true, title: 'Step-by-Step Guidance', desc: 'Numbered sequential points and procedural checklists' },
        { value: false, title: 'Holistic Narrative', desc: 'Fluid conceptual explanation without excessive lists' }
      ]
    },
    {
      key: 'preferred_quiz_style',
      title: 'Challenge Modality',
      subtitle: 'What type of quiz exercises do you prefer?',
      type: 'choice',
      options: [
        { value: 'writing', title: 'Hands-on Writing & Coding', desc: 'Authoring prompts and reviewing code scenarios' },
        { value: 'mcq', title: 'Conceptual MCQs', desc: 'Fast-paced multiple choice with reasoning explanations' },
        { value: 'mixed', title: 'Adaptive Mixed', desc: 'Dynamic mix calibrated to each topic’s difficulty tier' }
      ]
    },
    {
      key: 'session_time_budget',
      title: 'Session Focus Time',
      subtitle: 'How much time do you typically have per learning session?',
      type: 'choice',
      options: [
        { value: 15, title: '15 Minutes', desc: 'Focused bite-sized lessons' },
        { value: 30, title: '30 Minutes', desc: 'Standard deep-work study session' },
        { value: 60, title: '60 Minutes', desc: 'Intensive masterclass session' }
      ]
    }
  ];

  let currentStep = 0;
  const answers = {};

  function renderStep() {
    const q = questions[currentStep];
    const isLast = currentStep === questions.length - 1;
    const progressPercent = Math.round(((currentStep + 1) / questions.length) * 100);

    const isAnswered = q.type === 'text' 
      ? (typeof answers[q.key] === 'string' && answers[q.key].trim().length > 0)
      : (answers[q.key] !== undefined);

    container.innerHTML = `
      <div class="animate-in card" style="width:100%;max-width:580px;padding:32px;">
        
        <!-- Header & Progress -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <span class="section-label" style="color:var(--c-accent);">Step ${currentStep + 1} of ${questions.length}</span>
          <span style="font-family:var(--font-mono);font-size:11px;color:var(--c-text-3);">${progressPercent}% complete</span>
        </div>

        <div style="width:100%;background:var(--c-raised);height:4px;border-radius:2px;overflow:hidden;margin-bottom:24px;border:1px solid var(--c-border);">
          <div style="background:var(--c-accent);height:100%;width:${progressPercent}%;transition:width 0.3s ease;"></div>
        </div>

        <h1 style="font-size:20px;font-weight:700;color:var(--c-text);letter-spacing:-0.02em;margin:0 0 6px;">${q.title}</h1>
        <p style="font-size:12.5px;color:var(--c-text-2);margin:0 0 20px;">${q.subtitle}</p>

        <!-- Input options -->
        <div id="step-input-container" style="display:flex;flex-direction:column;gap:10px;margin-bottom:28px;">
          ${
            q.type === 'text'
              ? `
                <div>
                  <input type="text" id="step-text-input" class="field-input" placeholder="${q.placeholder}" value="${answers[q.key] || ''}" style="font-size:13px;padding:12px 14px;">
                  <div id="name-validation-msg" style="display:none;font-size:11px;color:var(--c-danger);margin-top:6px;font-family:var(--font-mono);">Please enter your name before proceeding.</div>
                </div>
              `
              : q.options.map((opt, i) => {
                  const isSelected = answers[q.key] === opt.value;
                  return `
                    <button type="button" data-opt-idx="${i}" class="opt-btn option-card ${isSelected ? 'selected' : ''}" style="width:100%;text-align:left;">
                      <div class="option-radio">
                        <div class="option-radio-dot" style="${isSelected ? 'display:block;' : ''}"></div>
                      </div>
                      <div>
                        <div class="option-title">${opt.title}</div>
                        <div class="option-desc">${opt.desc}</div>
                      </div>
                    </button>
                  `;
                }).join('')
          }
        </div>

        <!-- Footer Navigation -->
        <div style="display:flex;align-items:center;justify-content:space-between;padding-top:16px;border-top:1px solid var(--c-border);">
          <button type="button" id="btn-prev" class="btn btn-ghost" style="visibility:${currentStep === 0 ? 'hidden' : 'visible'};">
            ← Back
          </button>
          <button type="button" id="btn-next" ${!isAnswered ? 'disabled' : ''} class="btn ${isAnswered ? 'btn-primary' : 'btn-ghost'}" style="${isAnswered ? 'color:#000000 !important;background:var(--c-accent);' : 'opacity:0.5;cursor:not-allowed;'}padding:10px 20px;font-size:12.5px;">
            ${isLast ? 'Complete & Enter Workspace →' : 'Next Step →'}
          </button>
        </div>

      </div>
    `;

    // Handle Text Input Real-time Validation
    if (q.type === 'text') {
      const textInput = document.getElementById('step-text-input');
      const nextBtn = document.getElementById('btn-next');
      const valMsg = document.getElementById('name-validation-msg');

      textInput.focus();
      textInput.oninput = () => {
        const val = textInput.value.trim();
        answers[q.key] = val;
        if (val.length > 0) {
          nextBtn.disabled = false;
          nextBtn.className = 'btn btn-primary';
          nextBtn.style.color = '#000000';
          nextBtn.style.background = 'var(--c-accent)';
          nextBtn.style.opacity = '1';
          nextBtn.style.cursor = 'pointer';
          valMsg.style.display = 'none';
        } else {
          nextBtn.disabled = true;
          nextBtn.className = 'btn btn-ghost';
          nextBtn.style.opacity = '0.5';
          nextBtn.style.cursor = 'not-allowed';
        }
      };

      textInput.onkeydown = (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          if (textInput.value.trim().length > 0) {
            nextBtn.click();
          } else {
            valMsg.style.display = 'block';
          }
        }
      };
    }

    // Handle Choice Selection with Direct Index Access
    if (q.type === 'choice') {
      container.querySelectorAll('.opt-btn').forEach(btn => {
        btn.onclick = () => {
          const idx = parseInt(btn.getAttribute('data-opt-idx'), 10);
          if (!isNaN(idx) && q.options[idx]) {
            answers[q.key] = q.options[idx].value;
            renderStep();
          }
        };
      });
    }

    // Prev / Next bindings
    const prevBtn = document.getElementById('btn-prev');
    const nextBtn = document.getElementById('btn-next');

    if (prevBtn) {
      prevBtn.onclick = () => {
        if (currentStep > 0) {
          currentStep--;
          renderStep();
        }
      };
    }

    if (nextBtn) {
      nextBtn.onclick = async () => {
        if (q.type === 'text') {
          const val = (document.getElementById('step-text-input')?.value || '').trim();
          if (!val) {
            const valMsg = document.getElementById('name-validation-msg');
            if (valMsg) valMsg.style.display = 'block';
            return;
          }
          answers[q.key] = val;
        } else if (answers[q.key] === undefined) {
          alert('Please select an option before continuing.');
          return;
        }

        if (isLast) {
          nextBtn.disabled = true;
          nextBtn.textContent = 'Saving Profile...';
          try {
            const res = await fetch('/api/v1/onboarding/submit', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify(answers)
            });
            const sessionData = await res.json();
            onOnboardingComplete(sessionData);
          } catch (err) {
            alert('Failed to complete onboarding: ' + err.message);
            nextBtn.disabled = false;
            nextBtn.textContent = 'Complete & Enter Workspace →';
          }
        } else {
          currentStep++;
          renderStep();
        }
      };
    }
  }

  renderStep();
}
