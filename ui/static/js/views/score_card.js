// ui/static/js/views/score_card.js
/**
 * Project ROAR — Evaluation Score Card.
 * Circular score ring + 5-variable adaptive scoring breakdown.
 */

export function renderScoreCardView(container, { scoreData, onAdvanceNode, onRetryNode }) {
  const b      = scoreData.breakdown;
  const passed = b.passed;
  const pct    = v => Math.round(v * 100);
  const score  = pct(b.final_score);
  const thresh = pct(b.passing_threshold);

  // SVG ring calc
  const R  = 54;
  const circumference = 2 * Math.PI * R;
  const filled  = circumference * (Math.min(score, 100) / 100);
  const ringColor = passed ? '#34D399' : score >= thresh * 0.8 ? '#FBBF24' : '#F87171';

  const barRow = (label, value, color, sub = '') => `
    <div style="display:flex;flex-direction:column;gap:5px;">
      <div style="display:flex;align-items:center;justify-content:space-between;">
        <span style="font-family:var(--font-mono);font-size:11.5px;font-weight:600;color:var(--c-text-2);">${label}</span>
        <span style="font-family:var(--font-mono);font-size:12px;font-weight:700;color:${color};">${value}%</span>
      </div>
      <div class="progress-track" style="height:7px;">
        <div class="progress-fill" style="width:${Math.max(0, value)}%;background:${color};"></div>
      </div>
      ${sub ? `<div style="font-family:var(--font-mono);font-size:10px;color:var(--c-text-3);">${sub}</div>` : ''}
    </div>
  `;

  container.innerHTML = `
    <div class="animate-in" style="width:100%;max-width:640px;display:flex;flex-direction:column;gap:16px;">

      <!-- Result banner -->
      <div class="card" style="padding:32px 32px 28px;border-color:${passed ? 'rgba(52,211,153,0.35)' : 'rgba(248,113,113,0.35)'};box-shadow:0 8px 32px ${passed ? 'rgba(52,211,153,0.12)' : 'rgba(248,113,113,0.12)'};">
        <div style="display:flex;align-items:center;gap:28px;flex-wrap:wrap;">

          <!-- Score ring -->
          <div style="flex-shrink:0;position:relative;width:136px;height:136px;display:flex;align-items:center;justify-content:center;">
            <svg width="136" height="136" viewBox="0 0 136 136">
              <circle class="score-ring-track" cx="68" cy="68" r="${R}"/>
              <circle class="score-ring-fill score-ring"
                cx="68" cy="68" r="${R}"
                stroke="${ringColor}"
                stroke-dasharray="${circumference}"
                stroke-dashoffset="${circumference - filled}"
              />
            </svg>
            <div style="position:absolute;text-align:center;">
              <div style="font-family:var(--font-mono);font-size:28px;font-weight:800;line-height:1;color:${ringColor};letter-spacing:-0.03em;">${score}<span style="font-size:15px;">%</span></div>
              <div style="font-family:var(--font-mono);font-size:10px;font-weight:700;color:var(--c-text-3);margin-top:4px;letter-spacing:0.06em;">FINAL</div>
            </div>
          </div>

          <!-- Status text -->
          <div style="flex:1;min-width:0;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
              <div style="
                width:34px;height:34px;border-radius:var(--r-sm);flex-shrink:0;
                display:flex;align-items:center;justify-content:center;
                background:${passed ? 'rgba(52,211,153,0.15)' : 'rgba(248,113,113,0.15)'};
                border:1px solid ${passed ? 'rgba(52,211,153,0.35)' : 'rgba(248,113,113,0.35)'};
              ">
                ${passed
                  ? `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:18px;height:18px;color:var(--c-success);"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>`
                  : `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:18px;height:18px;color:var(--c-danger);"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`
                }
              </div>
              <div>
                <div style="font-size:17px;font-weight:800;color:var(--c-text);">
                  ${passed ? 'Topic Mastered! 🎉' : 'Below Passing Threshold'}
                </div>
                <div style="font-family:var(--font-mono);font-size:11px;color:var(--c-text-3);margin-top:2px;">
                  Required: <span style="color:var(--c-text-2);font-weight:600;">${thresh}%</span> · Achieved: <span style="color:${ringColor};font-weight:700;">${score}%</span>
                </div>
              </div>
            </div>

            <!-- Rationale -->
            <div style="padding:14px 16px;background:var(--c-raised);border:1px solid rgba(255,255,255,0.10);border-radius:var(--r-md);">
              <div class="section-label" style="margin-bottom:6px;color:var(--c-accent);">Evaluator feedback</div>
              <p style="font-size:13.5px;color:var(--c-text-2);line-height:1.65;margin:0;">${b.rationale}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Score breakdown -->
      <div class="card stagger-item stagger-2" style="padding:24px 28px;">
        <div class="section-label" style="margin-bottom:18px;">Score breakdown</div>

        <div style="display:flex;flex-direction:column;gap:16px;">
          ${barRow('Semantic similarity', pct(b.semantic_score), pct(b.semantic_score) >= 60 ? '#34D399' : '#F87171')}
          ${barRow('Structure & rules', pct(b.rule_score), pct(b.rule_score) >= 60 ? '#34D399' : '#F87171')}
        </div>

        <div style="height:1px;background:rgba(255,255,255,0.10);margin:18px 0;"></div>

        <!-- Penalty grid -->
        <div class="section-label" style="margin-bottom:14px;">Penalties applied</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
          <div class="metric-card">
            <div class="metric-label" style="${b.hints_used > 0 ? 'color:var(--c-amber);' : ''}">Hint penalty</div>
            <div class="metric-value" style="color:${b.hints_used > 0 ? 'var(--c-amber)' : 'var(--c-text-3)'};">
              ${b.hint_penalty > 0 ? `−${pct(b.hint_penalty)}%` : '—'}
            </div>
            <div class="metric-sub">${b.hints_used} hint${b.hints_used !== 1 ? 's' : ''} used</div>
          </div>

          <div class="metric-card">
            <div class="metric-label" style="${b.time_penalty > 0 ? 'color:var(--c-danger);' : ''}">Time penalty</div>
            <div class="metric-value" style="color:${b.time_penalty > 0 ? 'var(--c-danger)' : 'var(--c-text-3)'};">
              ${b.time_penalty > 0 ? `−${pct(b.time_penalty)}%` : '—'}
            </div>
            <div class="metric-sub">${Math.round(b.time_elapsed_seconds)}s / ${Math.round(b.time_budget_seconds)}s</div>
          </div>

          <div class="metric-card">
            <div class="metric-label" style="${b.retry_penalty > 0 ? 'color:var(--c-danger);' : ''}">Streak penalty</div>
            <div class="metric-value" style="color:${b.retry_penalty > 0 ? 'var(--c-danger)' : 'var(--c-text-3)'};">
              ${b.retry_penalty > 0 ? `−${pct(b.retry_penalty)}%` : '—'}
            </div>
            <div class="metric-sub">${b.fail_streak} fail streak</div>
          </div>
        </div>

        <!-- Final score row -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-top:18px;padding-top:18px;border-top:1px solid rgba(255,255,255,0.10);">
          <div style="font-family:var(--font-mono);font-size:11px;color:var(--c-text-3);">
            (0.5 × semantic) + (0.5 × structure) − penalties
          </div>
          <div style="font-family:var(--font-mono);font-size:18px;font-weight:800;color:${passed ? 'var(--c-success)' : 'var(--c-danger)'};">
            ${score}% final
          </div>
        </div>
      </div>

      <!-- Action -->
      <div class="stagger-item stagger-3" style="display:flex;justify-content:flex-end;gap:12px;">
        ${passed
          ? `<button id="btn-advance-node" class="btn btn-primary" style="padding:12px 30px;font-size:14px;">
               Unlock Next Topic →
             </button>`
          : `<div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;width:100%;">
               <button id="btn-retry-node" class="btn btn-primary" style="padding:12px 30px;font-size:14px;">
                 Review Notes &amp; Retry Quiz →
               </button>
               <span style="font-family:var(--font-mono);font-size:10.5px;color:var(--c-text-3);">
                 Scaffolding hint support will be enabled for this retry
               </span>
             </div>`
        }
      </div>

    </div>
  `;

  document.getElementById('btn-advance-node')?.addEventListener('click', onAdvanceNode);
  document.getElementById('btn-retry-node')?.addEventListener('click', onRetryNode);
}
