// ui/static/js/views/login.js
/**
 * Project ROAR: Authentication View.
 * Clean, restrained layout with 1-click Demo Guest access.
 */

export function renderLoginView(container, { onLoginSuccess, onBackToHome, onGuestDemo }) {
  container.innerHTML = `
    <div class="auth-wrap animate-in">
      <div class="auth-card">
        
        <!-- Back to home -->
        <div class="auth-top-nav">
          <button id="btn-auth-back-home" class="auth-back-link">
            <svg viewBox="0 0 16 16" fill="currentColor" style="width:14px;height:14px;">
              <path fill-rule="evenodd" d="M15 8a.75.75 0 0 1-.75.75H4.06l3.72 3.72a.75.75 0 1 1-1.06 1.06l-5-5a.75.75 0 0 1 0-1.06l5-5a.75.75 0 0 1 1.06 1.06L4.06 7.25h10.19A.75.75 0 0 1 15 8z"/>
            </svg>
            Back to Overview
          </button>
        </div>

        <!-- Brand Header with Official Logo -->
        <div class="auth-brand-head">
          <img src="/static/img/roar-dark.svg" alt="Project R.O.A.R." class="auth-logo-full">
          <p class="auth-brand-sub">Autonomous Multi-Agent Socratic Tutoring System</p>
        </div>

        <!-- 1-Click Demo Entry -->
        <div class="auth-demo-box">
          <div class="auth-demo-text">
            <span class="auth-demo-badge">Instant Demo Access</span>
            <span class="auth-demo-desc">Try all 36 competency nodes immediately with a preconfigured student profile.</span>
          </div>
          <button id="btn-quick-guest-demo" class="btn btn-primary auth-demo-btn">
            Launch Demo Workspace →
          </button>
        </div>

        <div class="auth-divider">
          <span>or sign in with your account</span>
        </div>

        <!-- Mode tabs -->
        <div class="auth-tabs">
          <button id="auth-tab-login" class="auth-tab active">Sign In</button>
          <button id="auth-tab-register" class="auth-tab">Register</button>
        </div>

        <form id="auth-form" class="auth-form">
          <div class="auth-field">
            <label class="auth-label">Username</label>
            <input type="text" id="auth-username" required autocomplete="username" class="field-input" placeholder="Enter username">
          </div>

          <div id="auth-email-group" class="auth-field" style="display:none;">
            <label class="auth-label">Email <span style="color:var(--c-text-3);">(optional)</span></label>
            <input type="email" id="auth-email" autocomplete="email" class="field-input" placeholder="you@example.com">
          </div>

          <div class="auth-field">
            <label class="auth-label">Password</label>
            <input type="password" id="auth-password" required autocomplete="current-password" class="field-input" placeholder="••••••••">
          </div>

          <div id="auth-error" class="auth-error" style="display:none;"></div>

          <button type="submit" id="auth-submit-btn" class="btn btn-secondary auth-submit-btn">
            Sign In to Workspace →
          </button>
        </form>

        <div class="auth-foot">
          <span>Local 4-bit Inference · Model Context Protocol (MCP) · Zero Answer Leakage</span>
        </div>

      </div>
    </div>
  `;

  let mode = 'login';
  const tabLogin    = document.getElementById('auth-tab-login');
  const tabRegister = document.getElementById('auth-tab-register');
  const emailGroup  = document.getElementById('auth-email-group');
  const submitBtn   = document.getElementById('auth-submit-btn');
  const form        = document.getElementById('auth-form');
  const errEl       = document.getElementById('auth-error');
  const btnBackHome = document.getElementById('btn-auth-back-home');
  const btnDemo     = document.getElementById('btn-quick-guest-demo');

  if (btnBackHome) {
    btnBackHome.onclick = onBackToHome;
  }

  if (btnDemo) {
    btnDemo.onclick = onGuestDemo;
  }

  tabLogin.onclick = () => {
    mode = 'login';
    tabLogin.classList.add('active');
    tabRegister.classList.remove('active');
    emailGroup.style.display = 'none';
    submitBtn.textContent = 'Sign In to Workspace →';
    errEl.style.display = 'none';
  };

  tabRegister.onclick = () => {
    mode = 'register';
    tabRegister.classList.add('active');
    tabLogin.classList.remove('active');
    emailGroup.style.display = 'block';
    submitBtn.textContent = 'Create Account & Start →';
    errEl.style.display = 'none';
  };

  form.onsubmit = async (e) => {
    e.preventDefault();
    const username = document.getElementById('auth-username').value.trim();
    const password = document.getElementById('auth-password').value;
    const email    = document.getElementById('auth-email')?.value.trim() || '';

    if (!username || !password) {
      errEl.textContent = 'Username and password are required.';
      errEl.style.display = 'block';
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Authenticating…';
    errEl.style.display = 'none';

    try {
      const endpoint = mode === 'login' ? '/api/v1/auth/login' : '/api/v1/auth/register';
      const payload  = mode === 'login' ? { username, password } : { username, password, email };

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      onLoginSuccess(data);
    } catch (err) {
      errEl.textContent = err.message;
      errEl.style.display = 'block';
      submitBtn.disabled = false;
      submitBtn.textContent = mode === 'login' ? 'Sign In to Workspace →' : 'Create Account & Start →';
    }
  };
}
