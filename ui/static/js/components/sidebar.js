// ui/static/js/components/sidebar.js
/**
 * Project ROAR — Curriculum Knowledge Graph Sidebar.
 * Renders grouped curriculum nodes with precise state indicators.
 */

export function renderSidebarCurriculum(nodes, activeNodeId, onSelectNode) {
  const container = document.getElementById('sidebar-curriculum-list');
  if (!container) return;
  container.innerHTML = '';

  const categories = {};
  nodes.forEach(node => {
    const cat = node.category || 'General';
    if (!categories[cat]) categories[cat] = [];
    categories[cat].push(node);
  });

  for (const [category, catNodes] of Object.entries(categories)) {
    const label = document.createElement('div');
    label.className = 'sb-section-label';
    label.textContent = category;
    container.appendChild(label);

    catNodes.forEach(node => {
      const isPassed   = node.is_passed;
      const isUnlocked = node.is_unlocked;
      const isActive   = node.id === activeNodeId;

      let stateClass = 'locked';
      if (isPassed)   stateClass = 'passed';
      else if (isActive) stateClass = 'active';
      else if (isUnlocked) stateClass = '';

      // Icon SVG
      let iconSvg = '';
      if (isPassed) {
        iconSvg = `<svg class="sb-item-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color:var(--c-success)"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>`;
      } else if (!isUnlocked) {
        iconSvg = `<svg class="sb-item-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color:var(--c-text-4);opacity:0.75;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>`;
      } else if (isActive) {
        iconSvg = `<span style="width:7px;height:7px;border-radius:50%;background:var(--c-accent);box-shadow:0 0 8px rgba(251,191,36,0.8);display:inline-block;flex-shrink:0;"></span>`;
      } else {
        iconSvg = `<span style="width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,0.22);display:inline-block;flex-shrink:0;"></span>`;
      }

      const btn = document.createElement('button');
      btn.className = `sb-item ${stateClass}`;
      btn.innerHTML = `
        ${iconSvg}
        <span class="sb-item-label">${node.title}</span>
        <span class="sb-item-tier">T${node.difficulty_tier}</span>
      `;

      if (isUnlocked || isPassed) {
        btn.onclick = () => onSelectNode(node.id);
      } else {
        btn.disabled = true;
      }

      container.appendChild(btn);
    });
  }
}
