// ui/static/js/components/sidebar.js
/**
 * Project ROAR: Accredited Curriculum Knowledge Graph Sidebar.
 * Displays curriculum as a structured, university-grade syllabus:
 * - Module headers (Module 1: Foundations, Module 2: Output Configuration...)
 * - Lesson indexing (1.1, 1.2, 2.1...)
 * - Clean status indicators (Mastered, Active, Locked)
 * - Ergonomic typography with no awkward truncation
 */

const MODULE_ORDER = [
  'Foundations',
  'Output Configuration',
  'Prompting Techniques',
  'Code Prompting',
  'Best Practices',
  'Output Engineering',
  'Collaborative & Workflow',
  'Advanced Reasoning'
];

export function renderSidebarCurriculum(nodes, activeNodeId, onSelectNode) {
  const container = document.getElementById('sidebar-curriculum-list');
  if (!container) return;
  container.innerHTML = '';

  // Group by category
  const categories = {};
  nodes.forEach(node => {
    const cat = node.category || 'General';
    if (!categories[cat]) categories[cat] = [];
    categories[cat].push(node);
  });

  // Sort categories by predefined module order
  const sortedCategories = Object.keys(categories).sort((a, b) => {
    const idxA = MODULE_ORDER.indexOf(a);
    const idxB = MODULE_ORDER.indexOf(b);
    return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
  });

  sortedCategories.forEach(category => {
    const catNodes = categories[category];
    const moduleIdx = MODULE_ORDER.indexOf(category) + 1;
    const moduleLabel = moduleIdx > 0 ? `Module ${moduleIdx}: ${category}` : category;

    const group = document.createElement('div');
    group.className = 'sb-category-group';

    // Module Header
    const header = document.createElement('div');
    header.className = 'sb-tier-header';
    header.innerHTML = `
      <span class="sb-module-title">${moduleLabel}</span>
      <span class="sb-category-count">${catNodes.length} topics</span>
    `;
    group.appendChild(header);

    // Lessons in this module
    catNodes.forEach((node, nodeIdx) => {
      const isPassed   = Boolean(node.is_passed);
      const isUnlocked = Boolean(node.is_unlocked);
      const isActive   = node.id === activeNodeId;

      let stateClass = 'locked';
      if (isPassed) stateClass = 'passed';
      else if (isActive) stateClass = 'active';
      else if (isUnlocked) stateClass = 'unlocked';

      let iconSvg = '';
      if (isPassed) {
        iconSvg = `<span class="sb-node-icon passed" title="Mastered"><svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg></span>`;
      } else if (!isUnlocked) {
        iconSvg = `<span class="sb-node-icon locked" title="Locked"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg></span>`;
      } else if (isActive) {
        iconSvg = `<span class="sb-node-icon active" title="Current Topic"><span class="sb-dot-pulse"></span></span>`;
      } else {
        iconSvg = `<span class="sb-node-icon unlocked" title="Ready to Study"><span class="sb-dot-idle"></span></span>`;
      }

      const lessonIndexStr = moduleIdx > 0 ? `${moduleIdx}.${nodeIdx + 1}` : `${nodeIdx + 1}`;

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `sb-item ${stateClass}`;
      btn.setAttribute('data-node-id', node.id);
      btn.innerHTML = `
        <div class="sb-item-left">
          ${iconSvg}
          <div class="sb-item-text-col">
            <span class="sb-item-num">${lessonIndexStr}</span>
            <span class="sb-item-title">${node.title}</span>
          </div>
        </div>
        <span class="sb-item-tier">T${node.difficulty_tier || 1}</span>
      `;

      if (isUnlocked || isPassed) {
        btn.onclick = () => onSelectNode(node.id);
      } else {
        btn.disabled = true;
      }

      if (isActive) {
        setTimeout(() => {
          btn.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }, 80);
      }

      group.appendChild(btn);
    });

    container.appendChild(group);
  });
}
