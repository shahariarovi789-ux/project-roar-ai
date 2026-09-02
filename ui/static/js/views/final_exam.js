// ui/static/js/views/final_exam.js
/**
 * Project ROAR — Capstone Assessment View.
 * High-contrast, publication-grade examination interface.
 */

export function renderFinalExamView(container, { token, onExamCompleted }) {
  container.innerHTML = `
    <div class="animate-in" style="width:100%;max-width:760px;display:flex;flex-direction:column;gap:18px;" id="final-exam-wrapper">
      
      <!-- Header Card -->
      <div class="card" style="padding:28px;text-align:center;">
        <div class="section-label" style="color:var(--c-accent);margin-bottom:6px;">Summative Capstone Assessment</div>
        <h1 style="font-size:22px;font-weight:700;color:var(--c-text);letter-spacing:-0.02em;margin:0 0 6px;">Prompt Engineering Final Examination</h1>
        <p style="font-size:12.5px;color:var(--c-text-2);max-width:520px;margin:0 auto;line-height:1.6;">
          A comprehensive 3-phase evaluation covering theory recall, applied prompt construction, and failure mode diagnosis.
        </p>
      </div>

      <div id="exam-content-area" style="display:flex;flex-direction:column;gap:16px;">
        <div style="text-align:center;padding:32px 0;color:var(--c-text-3);font-family:var(--font-mono);font-size:12px;">
          Checking exam eligibility...
        </div>
      </div>
    </div>
  `;

  loadExam();

  async function loadExam() {
    const area = document.getElementById('exam-content-area');
    try {
      const statusRes = await fetch('/api/v1/final-exam/status', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const statusData = await statusRes.json();

      if (!statusData.unlocked) {
        area.innerHTML = `
          <div class="card" style="padding:36px;text-align:center;border-color:rgba(251,146,60,0.3);background:rgba(251,146,60,0.04);display:flex;flex-direction:column;align-items:center;gap:12px;">
            <div style="font-size:36px;line-height:1;">🔒</div>
            <h2 style="font-size:18px;font-weight:700;color:var(--c-text);margin:0;">Final Exam Locked</h2>
            <p style="font-size:12.5px;color:var(--c-text-2);max-width:440px;line-height:1.6;margin:0;">${statusData.message}</p>
            <div style="font-family:var(--font-mono);font-size:12px;font-weight:600;color:var(--c-accent);padding:4px 12px;border:1px solid rgba(232,200,74,0.3);border-radius:var(--r-sm);background:var(--c-accent-dim);margin-top:4px;">
              Progress: ${statusData.completed_nodes} / ${statusData.total_required} Nodes Passed
            </div>
          </div>
        `;
        return;
      }

      // Fetch Exam Questions
      const qRes = await fetch('/api/v1/final-exam/questions', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const questions = await qRes.json();

      renderExamForm(area, questions);
    } catch (err) {
      area.innerHTML = `<div class="card" style="padding:20px;color:var(--c-danger);font-family:var(--font-mono);font-size:12px;">Error loading exam: ${err.message}</div>`;
    }
  }

  function renderExamForm(area, questions) {
    area.innerHTML = `
      <form id="final-exam-form" style="display:flex;flex-direction:column;gap:18px;">

        <!-- Phase A: Theory MCQ -->
        <div class="card" style="padding:24px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--c-border);">
            <div>
              <div class="section-label" style="color:var(--c-accent);">Phase A (30% Weight)</div>
              <h2 style="font-size:15px;font-weight:700;color:var(--c-text);margin:2px 0 0;">Theory &amp; Mechanics Multiple Choice</h2>
            </div>
            <span class="tag">5 Questions</span>
          </div>

          <div style="display:flex;flex-direction:column;gap:16px;">
            ${questions.phase_a.map((q, idx) => `
              <div class="card-raised" style="padding:16px;">
                <p style="font-size:13px;font-weight:600;color:var(--c-text);margin-bottom:12px;line-height:1.5;">${idx + 1}. ${q.q}</p>
                <div style="display:flex;flex-direction:column;gap:8px;">
                  ${q.opts.map(opt => {
                    const letter = opt.charAt(0);
                    return `
                      <label class="option-card" style="margin:0;">
                        <input type="radio" name="phase_a_${q.id}" value="${letter}" required style="display:none;">
                        <div class="option-radio"><div class="option-radio-dot"></div></div>
                        <div class="option-title">${opt}</div>
                      </label>
                    `;
                  }).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Phase B: Applied Writing -->
        <div class="card" style="padding:24px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--c-border);">
            <div>
              <div class="section-label" style="color:var(--c-accent);">Phase B (50% Weight)</div>
              <h2 style="font-size:15px;font-weight:700;color:var(--c-text);margin:2px 0 0;">Applied Prompt Construction Scenarios</h2>
            </div>
            <span class="tag">3 Scenarios</span>
          </div>

          <div style="display:flex;flex-direction:column;gap:16px;">
            ${questions.phase_b.map((item, idx) => `
              <div class="card-raised" style="padding:16px;display:flex;flex-direction:column;gap:10px;">
                <div style="font-size:13px;font-weight:700;color:var(--c-accent);">${item.title}</div>
                <p style="font-size:12.5px;color:var(--c-text);line-height:1.6;margin:0;">${item.prompt}</p>
                <textarea name="phase_b_${idx}" rows="4" required class="field-input" placeholder="Write your full production prompt here..."></textarea>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Phase C: Portfolio Critique -->
        <div class="card" style="padding:24px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--c-border);">
            <div>
              <div class="section-label" style="color:var(--c-accent);">Phase C (20% Weight)</div>
              <h2 style="font-size:15px;font-weight:700;color:var(--c-text);margin:2px 0 0;">Portfolio Prompt Critique &amp; Rewrite</h2>
            </div>
            <span class="tag">2 Critiques</span>
          </div>

          <div style="display:flex;flex-direction:column;gap:16px;">
            ${questions.phase_c.map((item, idx) => `
              <div class="card-raised" style="padding:16px;display:flex;flex-direction:column;gap:10px;">
                <div style="font-size:13px;font-weight:700;color:var(--c-amber);">${item.title}</div>
                <div style="padding:10px 12px;background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.25);border-radius:var(--r-sm);color:#FCA5A5;font-family:var(--font-mono);font-size:12px;line-height:1.5;">
                  "${item.flawed_prompt}"
                </div>
                <p style="font-size:12.5px;color:var(--c-text-2);line-height:1.6;margin:0;">${item.task}</p>
                <textarea name="phase_c_${idx}" rows="4" required class="field-input" placeholder="Identify flaws and write your rewritten prompt..."></textarea>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Submit Button -->
        <div style="padding-top:8px;">
          <button type="submit" id="btn-submit-final-exam" class="btn btn-primary" style="width:100%;padding:14px;font-size:13.5px;font-weight:700;justify-content:center;color:#000000 !important;background:var(--c-accent);">
            Submit Final Examination for Comprehensive Grading 🎓
          </button>
        </div>

      </form>
    `;

    // Radio option card selection
    document.getElementById('final-exam-form').addEventListener('change', (e) => {
      if (e.target.type === 'radio') {
        const name = e.target.name;
        document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
          r.closest('.option-card')?.classList.remove('selected');
        });
        e.target.closest('.option-card')?.classList.add('selected');
      }
    });

    const form = document.getElementById('final-exam-form');
    form.onsubmit = async (e) => {
      e.preventDefault();
      const submitBtn = document.getElementById('btn-submit-final-exam');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Evaluating all three examination phases...';

      const formData = new FormData(form);
      const phaseA = {};
      questions.phase_a.forEach(q => {
        phaseA[q.id] = formData.get(`phase_a_${q.id}`) || 'A';
      });

      const phaseB = [
        formData.get('phase_b_0') || '',
        formData.get('phase_b_1') || '',
        formData.get('phase_b_2') || ''
      ];

      const phaseC = [
        formData.get('phase_c_0') || '',
        formData.get('phase_c_1') || ''
      ];

      try {
        const res = await fetch('/api/v1/final-exam/submit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            phase_a_answers: phaseA,
            phase_b_answers: phaseB,
            phase_c_answers: phaseC
          })
        });

        const result = await res.json();
        renderExamResult(area, result);
      } catch (err) {
        alert('Exam grading failed: ' + err.message);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Final Examination 🎓';
      }
    };
  }

  function renderExamResult(area, res) {
    const passed = res.passed;
    area.innerHTML = `
      <div class="card" style="padding:32px;text-align:center;border-color:${passed ? 'rgba(74,222,128,0.3)' : 'rgba(248,113,113,0.3)'};background:${passed ? 'rgba(74,222,128,0.04)' : 'rgba(248,113,113,0.04)'};display:flex;flex-direction:column;align-items:center;gap:18px;">
        <div style="font-size:44px;line-height:1;">${passed ? '🏆' : '❌'}</div>
        <div>
          <h2 style="font-size:22px;font-weight:700;color:var(--c-text);margin:0 0 6px;">${passed ? 'Graduate Certified!' : 'Examination Incomplete'}</h2>
          <p style="font-size:12.5px;color:var(--c-text-2);max-width:480px;margin:0 auto;line-height:1.6;">${res.feedback}</p>
        </div>

        <!-- Section Scores -->
        <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:12px;width:100%;max-width:480px;">
          <div class="metric-card">
            <div class="metric-label">Phase A (MCQ)</div>
            <div class="metric-value" style="color:var(--c-accent);">${Math.round(res.section_a_score * 100)}%</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Phase B (Writing)</div>
            <div class="metric-value" style="color:var(--c-accent);">${Math.round(res.section_b_score * 100)}%</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Phase C (Critique)</div>
            <div class="metric-value" style="color:var(--c-accent);">${Math.round(res.section_c_score * 100)}%</div>
          </div>
        </div>

        <div style="padding:16px 24px;border-radius:var(--r-md);background:var(--c-raised);border:1px solid var(--c-border);width:100%;max-width:480px;">
          <div class="metric-label">Overall Weighted Score</div>
          <div style="font-family:var(--font-mono);font-size:36px;font-weight:700;color:${passed ? 'var(--c-success)' : 'var(--c-danger)'};margin-top:2px;">
            ${Math.round(res.overall_score * 100)}%
          </div>
        </div>
      </div>
    `;
  }
}
