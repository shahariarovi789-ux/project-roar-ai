// ui/static/js/components/toast.js
/**
 * Project ROAR — Toast notification system.
 * Pure CSS-variable driven, no Tailwind dependency.
 */
export function showToast(message, type = 'info', durationMs = 3500) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const styles = {
    info:    { bg: 'rgba(30,34,58,0.97)',   border: 'rgba(165,180,252,0.35)', text: '#A5B4FC', icon: 'ℹ' },
    success: { bg: 'rgba(15,40,30,0.97)',   border: 'rgba(74,222,128,0.35)',  text: '#4ADE80', icon: '✓' },
    warning: { bg: 'rgba(40,28,10,0.97)',   border: 'rgba(251,146,60,0.35)',  text: '#FB923C', icon: '!' },
    error:   { bg: 'rgba(42,18,18,0.97)',   border: 'rgba(248,113,113,0.35)', text: '#F87171', icon: '×' },
  };

  const s = styles[type] || styles.info;

  const toast = document.createElement('div');
  toast.style.cssText = `
    pointer-events: auto;
    padding: 10px 14px;
    border-radius: 8px;
    border: 1px solid ${s.border};
    background: ${s.bg};
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 12.5px;
    font-weight: 500;
    color: #E8EAF0;
    max-width: 340px;
    transform: translateY(8px);
    opacity: 0;
    transition: transform 0.22s cubic-bezier(0.16,1,0.3,1), opacity 0.22s ease;
  `;

  toast.innerHTML = `
    <span style="
      width:18px;height:18px;border-radius:4px;
      background:${s.border};
      color:${s.text};
      display:flex;align-items:center;justify-content:center;
      font-size:11px;font-weight:800;flex-shrink:0;
    ">${s.icon}</span>
    <span style="flex:1;">${message}</span>
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
    setTimeout(() => toast.remove(), 260);
  }, durationMs);
}
