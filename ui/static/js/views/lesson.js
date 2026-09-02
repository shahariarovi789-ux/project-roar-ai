// ui/static/js/views/lesson.js
/**
 * Project ROAR — Study Guide view.
 * Clean editorial layout for AI-generated lecture notes with vibrant visual hierarchy.
 */

export function renderLessonView(container, { lessonData, onStartQuiz, onSkipToQuiz, onRegenerateLesson, isExpert }) {
  const isPassed   = lessonData.is_passed;
  const wordCount  = (lessonData.lesson_markdown || '').split(/\s+/).length;
  const readMinutes = Math.max(1, Math.round(wordCount / 180));

  const bloomColors = {
    'Remember':    '#818CF8',
    'Understand':  '#60A5FA',
    'Apply':       '#34D399',
    'Analyze':     '#FB923C',
    'Evaluate':    '#F472B6',
    'Create':      '#FBBF24',
  };
  const bloomColor = bloomColors[lessonData.bloom_level] || 'var(--c-accent)';

  container.innerHTML = `
    <div class="animate-in" style="width:100%;max-width:820px;display:flex;flex-direction:column;gap:0;">

      <!-- Page header -->
      <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:24px;flex-wrap:wrap;">
        <div style="min-width:0;flex:1;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap;">
            <span class="chip chip-muted">${lessonData.category}</span>
            ${isPassed
              ? `<span class="chip chip-success">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width:10px;height:10px;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  Mastered
                </span>`
              : `<span class="chip chip-indigo">In progress</span>`
            }
            <span style="font-family:var(--font-mono);font-size:11px;font-weight:500;color:var(--c-text-3);">${readMinutes} min read</span>
          </div>
          <h1 style="font-size:24px;font-weight:800;color:var(--c-text);letter-spacing:-0.03em;line-height:1.2;margin:0 0 6px;">${lessonData.topic_title}</h1>
          <div style="font-family:var(--font-mono);font-size:11px;color:var(--c-text-3);">${lessonData.topic_path || ''}</div>
        </div>

        <!-- Action toolbar -->
        <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;flex-wrap:wrap;">
          <button id="btn-copy-notes" class="btn btn-ghost" style="font-size:12px;">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            Copy
          </button>
          <button id="btn-download-notes" class="btn btn-ghost" style="font-size:12px;">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
            Export
          </button>
          <button id="btn-regen-lesson" class="btn btn-ghost" style="font-size:12px;">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            Regen
          </button>
          ${isExpert && !isPassed
            ? `<button id="btn-expert-skip" class="btn btn-ghost" style="font-size:12px;color:var(--c-text-3);">Skip →</button>`
            : ''
          }
          <button id="btn-proceed-quiz" class="btn btn-primary" style="font-size:13px;padding:9px 20px;">
            ${isPassed ? 'Retake quiz' : 'Start quiz'} →
          </button>
        </div>
      </div>

      <!-- Meta strip -->
      <div style="display:flex;align-items:stretch;border:1px solid rgba(255,255,255,0.12);border-radius:var(--r-md);margin-bottom:24px;overflow:hidden;background:var(--c-surface);box-shadow:0 4px 16px rgba(0,0,0,0.35);">
        <div style="flex:1;padding:12px 18px;border-right:1px solid rgba(255,255,255,0.09);">
          <div style="font-family:var(--font-mono);font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:var(--c-text-3);margin-bottom:4px;">Weight</div>
          <div style="font-family:var(--font-mono);font-size:16px;font-weight:800;color:var(--c-text);">${lessonData.weight}</div>
        </div>
        <div style="flex:1.2;padding:12px 18px;border-right:1px solid rgba(255,255,255,0.09);">
          <div style="font-family:var(--font-mono);font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:var(--c-text-3);margin-bottom:4px;">Bloom Level</div>
          <div style="font-family:var(--font-mono);font-size:14px;font-weight:700;color:${bloomColor};">${lessonData.bloom_level}</div>
        </div>
        <div style="flex:2;padding:12px 18px;border-right:1px solid rgba(255,255,255,0.09);min-width:0;">
          <div style="font-family:var(--font-mono);font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:var(--c-text-3);margin-bottom:4px;">Model Engine</div>
          <div style="font-family:var(--font-mono);font-size:12.5px;font-weight:600;color:var(--c-text-2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${lessonData.model_used || '—'}</div>
        </div>
        <div style="flex:1.2;padding:12px 18px;${lessonData.rag_sources_used ? 'border-right:1px solid rgba(255,255,255,0.09);' : ''}">
          <div style="font-family:var(--font-mono);font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:var(--c-text-3);margin-bottom:4px;">Latency</div>
          <div style="font-family:var(--font-mono);font-size:14px;font-weight:700;color:var(--c-text);">${lessonData.latency_ms || 0}<span style="font-size:10px;font-weight:400;color:var(--c-text-3);">ms</span></div>
        </div>
        ${lessonData.rag_sources_used
          ? `<div style="display:flex;align-items:center;padding:12px 18px;background:rgba(165,180,252,0.06);">
               <span style="font-family:var(--font-mono);font-size:10.5px;font-weight:700;color:#A5B4FC;background:rgba(165,180,252,0.15);border:1px solid rgba(165,180,252,0.3);padding:3px 10px;border-radius:100px;">RAG Grounded</span>
             </div>`
          : ''
        }
      </div>

      <!-- Lesson card -->
      <div class="card stagger-item stagger-1" style="padding:40px 44px 44px;">
        <div class="prose">
          ${window.marked ? window.marked.parse(lessonData.lesson_markdown || '') : (lessonData.lesson_markdown || '')}
        </div>
      </div>

      <!-- Bottom CTA -->
      <div style="display:flex;align-items:center;justify-content:space-between;margin-top:22px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.10);">
        <span style="font-family:var(--font-mono);font-size:12px;font-weight:500;color:var(--c-text-3);">${wordCount} words · ${readMinutes} min read</span>
        <button id="btn-bottom-quiz" class="btn btn-primary" style="font-size:13.5px;padding:11px 26px;">
          ${isPassed ? 'Retake practice quiz →' : 'I understand — start quiz →'}
        </button>
      </div>

    </div>
  `;

  document.getElementById('btn-proceed-quiz').onclick  = onStartQuiz;
  document.getElementById('btn-bottom-quiz').onclick   = onStartQuiz;
  
  const regenBtn = document.getElementById('btn-regen-lesson');
  if (regenBtn) {
    regenBtn.onclick = () => {
      regenBtn.disabled = true;
      regenBtn.innerHTML = `<span class="spinner" style="width:11px;height:11px;border-width:1.5px;"></span> Regenerating…`;
      onRegenerateLesson();
    };
  }
  
  document.getElementById('btn-expert-skip')?.addEventListener('click', onSkipToQuiz);

  // Copy
  document.getElementById('btn-copy-notes').onclick = async () => {
    const btn = document.getElementById('btn-copy-notes');
    try {
      await navigator.clipboard.writeText(lessonData.lesson_markdown || '');
      btn.textContent = '✓ Copied';
      setTimeout(() => {
        btn.innerHTML = `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>Copy`;
      }, 2000);
    } catch (e) { alert('Copy failed.'); }
  };

  // Download
  document.getElementById('btn-download-notes').onclick = () => {
    const blob = new Blob([lessonData.lesson_markdown || ''], { type: 'text/markdown' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = `${(lessonData.topic_title || 'notes').replace(/[^a-zA-Z0-9_-]/g, '_')}.md`;
    document.body.appendChild(a); a.click();
    document.body.removeChild(a); URL.revokeObjectURL(url);
  };
}
