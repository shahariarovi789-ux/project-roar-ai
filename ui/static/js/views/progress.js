// ui/static/js/views/progress.js
/**
 * Project ROAR — Curriculum Progress & Knowledge Graph.
 * High-contrast, developer-tool aesthetic.
 */

export function renderProgressView(container, { progressData, onSelectNode }) {
  container.innerHTML = `
    <div class="animate-in" style="width:100%;max-width:880px;display:flex;flex-direction:column;gap:20px;">

      <!-- Progress Overview Header Card -->
      <div class="card" style="padding:28px 32px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:20px;">
        <div>
          <div class="section-label" style="color:var(--c-accent);margin-bottom:6px;">Curriculum Knowledge Graph</div>
          <h1 style="font-size:22px;font-weight:800;color:var(--c-text);letter-spacing:-0.025em;margin:0 0 8px;">Prompt Engineering Mastery Map</h1>
          <p style="font-size:13px;color:var(--c-text-2);margin:0;">
            Completed <strong style="color:#FFFFFF;">${progressData.completed_nodes_count}</strong> of <strong style="color:#FFFFFF;">${progressData.total_nodes}</strong> weighted curriculum nodes.
          </p>
        </div>

        <div style="display:flex;align-items:center;gap:20px;">
          <div style="text-align:right;">
            <div style="font-family:var(--font-mono);font-size:32px;font-weight:800;line-height:1;color:var(--c-accent);">
              ${progressData.overall_progress_percentage}%
            </div>
            <div style="font-family:var(--font-mono);font-size:10px;font-weight:700;color:var(--c-text-3);margin-top:5px;text-transform:uppercase;letter-spacing:0.06em;">
              Completion Rate
            </div>
          </div>
          <div style="width:110px;height:8px;border-radius:4px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);overflow:hidden;">
            <div style="background:linear-gradient(90deg, #FDE047, #F59E0B);height:100%;width:${progressData.overall_progress_percentage}%;transition:width 0.6s ease;"></div>
          </div>
        </div>
      </div>

      <!-- Node Grid categorized by section -->
      <div style="display:flex;flex-direction:column;gap:18px;">
        ${renderCategorySections(progressData.nodes)}
      </div>

    </div>
  `;

  // Bind click on unlocked nodes
  container.querySelectorAll('.node-card-btn').forEach(btn => {
    btn.onclick = () => {
      const nodeId = btn.getAttribute('data-node-id');
      if (nodeId) onSelectNode(nodeId);
    };
  });
}

function renderCategorySections(nodes) {
  const categories = {};
  nodes.forEach(n => {
    if (!categories[n.category]) categories[n.category] = [];
    categories[n.category].push(n);
  });

  return Object.entries(categories).map(([catName, catNodes]) => `
    <div class="card" style="padding:24px 26px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.10);">
        <h2 style="font-size:13.5px;font-weight:800;color:var(--c-text);text-transform:uppercase;letter-spacing:0.06em;margin:0;">${catName}</h2>
        <span style="font-family:var(--font-mono);font-size:11.5px;font-weight:600;color:var(--c-text-3);">
          ${catNodes.filter(n => n.is_passed).length}/${catNodes.length} passed
        </span>
      </div>

      <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(250px, 1fr));gap:12px;">
        ${catNodes.map(n => {
          let statusBadge = '<span style="color:var(--c-text-4);">🔒 Locked</span>';
          let borderStyle = 'border:1px solid rgba(255,255,255,0.08);opacity:0.65;background:var(--c-base);';

          if (n.is_passed) {
            statusBadge = `<span style="color:var(--c-success);font-weight:700;">✅ ${Math.round(n.mastery_score * 100)}%</span>`;
            borderStyle = 'border:1px solid rgba(52,211,153,0.35);background:rgba(52,211,153,0.06);box-shadow:0 2px 8px rgba(0,0,0,0.3);';
          } else if (n.is_current) {
            statusBadge = '<span style="color:var(--c-accent);font-weight:700;">🟡 Active</span>';
            borderStyle = 'border:1px solid rgba(251,191,36,0.45);background:rgba(251,191,36,0.12);box-shadow:0 0 16px rgba(251,191,36,0.2);';
          } else if (n.is_unlocked) {
            statusBadge = '<span style="color:var(--c-text-2);font-weight:600;">⚪ Ready</span>';
            borderStyle = 'border:1px solid rgba(255,255,255,0.16);background:var(--c-raised);box-shadow:0 2px 8px rgba(0,0,0,0.3);';
          }

          const isClickable = n.is_unlocked || n.is_passed;

          return `
            <button 
              ${isClickable ? `data-node-id="${n.id}"` : 'disabled'}
              class="node-card-btn option-card"
              style="${borderStyle};padding:14px 16px;text-align:left;display:flex;flex-direction:column;gap:7px;cursor:${isClickable ? 'pointer' : 'not-allowed'};margin:0;"
            >
              <div style="display:flex;align-items:center;justify-content:space-between;width:100%;font-family:var(--font-mono);font-size:10.5px;">
                <span style="color:var(--c-text-3);font-weight:600;">T${n.difficulty_tier} • W${n.weight}</span>
                <span>${statusBadge}</span>
              </div>
              <div class="option-title" style="font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:100%;">${n.title}</div>
              <div style="font-size:12px;color:var(--c-text-3);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">
                ${n.description || ''}
              </div>
            </button>
          `;
        }).join('')}
      </div>
    </div>
  `).join('');
}
