// ui/static/js/components/toast.js
/**
 * Project ROAR: Toast notification system.
 * Pure CSS-variable driven, lightweight and accessible.
 */
export function showToast(message, type = 'info', durationMs = 3500) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const styles = {
    info:    { bg: 'rgba(26, 34, 48, 0.98)', border: 'rgba(56, 189, 248, 0.35)', text: '#38BDF8', icon: 'i' },
    success: { bg: 'rgba(16, 32, 24, 0.98)', border: 'rgba(16, 185, 129, 0.35)', text: '#10B981', icon: '✓' },
    warning: { bg: 'rgba(40, 28, 12, 0.98)', border: 'rgba(245, 158, 11, 0.35)', text: '#F59E0B', icon: '!' },
    error:   { bg: 'rgba(40, 16, 16, 0.98)', border: 'rgba(239, 68, 68, 0.35)', text: '#EF4444', icon: '×' },
  };

  const s = styles[type] || styles.info;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.style.cssText = `
    pointer-events: auto;
    padding: 10px 14px;
    border-radius: 6px;
    border: 1px solid ${s.border};
    background: ${s.bg};
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: var(--font-sans);
    font-size: 12.5px;
    font-weight: 500;
    color: var(--c-text);
    max-width: 360px;
    transform: translateY(8px);
    opacity: 0;
    transition: transform 0.18s cubic-bezier(0.16,1,0.3,1), opacity 0.18s ease;
  `;

  toast.innerHTML = `
    <span style="
      width: 18px; height: 18px; border-radius: 4px;
      background: ${s.border};
      color: ${s.text};
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-mono);
      font-size: 11px; font-weight: 700; flex-shrink: 0;
    ">${s.icon}</span>
    <span style="flex: 1; line-height: 1.4;">${message}</span>
  `;

  container.appendChild(toast);

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      toast.style.transform = 'translateY(0)';
      toast.style.opacity   = '1';
    });
  });

  setTimeout(() => {
    toast.style.transform = 'translateX(12px)';
    toast.style.opacity   = '0';
    setTimeout(() => toast.remove(), 200);
  }, durationMs);
}
