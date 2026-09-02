// ui/static/js/views/login.js
/**
 * Project ROAR — Authentication View.
 */

export function renderLoginView(container, { onLoginSuccess }) {
  container.innerHTML = `
    <div class="animate-in" style="width:100%;max-width:380px;margin:auto;">
      <div class="card" style="padding:36px 32px 28px;box-shadow:0 8px 40px rgba(0,0,0,0.5);">

        <!-- Brand -->
        <div style="margin-bottom:32px;text-align:center;">
          <div style="
            width:44px;height:44px;margin:0 auto 14px;
            background:var(--c-accent);
            border-radius:8px;
            display:flex;align-items:center;justify-content:center;
          ">
            <svg viewBox="0 0 16 16" style="width:20px;height:20px;fill:#000;">
              <path d="M8 1L15 8L8 15L1 8Z"/>
            </svg>
          </div>
          <div style="font-size:16px;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;color:var(--c-text);">Project ROAR</div>
          <div style="font-family:var(--font-mono);font-size:10.5px;color:var(--c-text-3);margin-top:5px;">Adaptive Prompt Engineering Tutor</div>
        </div>

        <!-- Mode tabs -->
        <div style="display:flex;border:1px solid var(--c-border);border-radius:var(--r-sm);overflow:hidden;margin-bottom:24px;background:var(--c-raised);">
          <button id="auth-tab-login" style="flex:1;padding:8px;font-size:12.5px;font-weight:700;background:var(--c-accent);color:#000;border:none;cursor:pointer;transition:background 0.12s;font-family:var(--font-sans);">
            Sign in
          </button>
          <button id="auth-tab-register" style="flex:1;padding:8px;font-size:12.5px;font-weight:500;background:transparent;color:var(--c-text-2);border:none;cursor:pointer;font-family:var(--font-sans);">
            Register
          </button>
        </div>

        <form id="auth-form" style="display:flex;flex-direction:column;gap:14px;">
          <div>
            <label style="display:block;font-family:var(--font-mono);font-size:10px;font-weight:600;color:var(--c-text-3);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.08em;">Username</label>
            <input type="text" id="auth-username" required autocomplete="username" class="field-input" placeholder="your_username" style="font-size:13.5px;">
          </div>

          <div id="auth-email-group" style="display:none;">
            <label style="display:block;font-family:var(--font-mono);font-size:10px;font-weight:600;color:var(--c-text-3);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.08em;">Email <span style="color:var(--c-text-4);">(optional)</span></label>
            <input type="email" id="auth-email" autocomplete="email" class="field-input" placeholder="you@example.com" style="font-size:13.5px;">
          </div>

          <div>
            <label style="display:block;font-family:var(--font-mono);font-size:10px;font-weight:600;color:var(--c-text-3);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.08em;">Password</label>
            <input type="password" id="auth-password" required autocomplete="current-password" class="field-input" placeholder="••••••••" style="font-size:14px;">
          </div>

          <div id="auth-error" style="display:none;padding:9px 12px;border:1px solid rgba(248,113,113,0.3);border-radius:var(--r-sm);background:rgba(248,113,113,0.08);font-size:12.5px;color:var(--c-danger);font-family:var(--font-mono);"></div>

          <button type="submit" id="auth-submit-btn" class="btn btn-primary" style="width:100%;justify-content:center;padding:10px;font-size:13px;margin-top:4px;">
            Sign in to ROAR →
          </button>
        </form>

        <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--c-border);text-align:center;">
          <span style="font-family:var(--font-mono);font-size:10px;color:var(--c-text-3);">Multi-agent cognition · Local &amp; Cloud LLM</span>
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

  const setActiveTab = (activeTab, inactiveTab) => {
    activeTab.style.cssText   = 'flex:1;padding:8px;font-size:12.5px;font-weight:700;background:var(--c-accent);color:#000;border:none;cursor:pointer;font-family:var(--font-sans);';
    inactiveTab.style.cssText = 'flex:1;padding:8px;font-size:12.5px;font-weight:500;background:transparent;color:var(--c-text-2);border:none;cursor:pointer;font-family:var(--font-sans);';
  };

  tabLogin.onclick = () => {
    mode = 'login';
    setActiveTab(tabLogin, tabRegister);
    emailGroup.style.display = 'none';
    submitBtn.textContent    = 'Sign in to ROAR →';
    errEl.style.display      = 'none';
  };

  tabRegister.onclick = () => {
    mode = 'register';
    setActiveTab(tabRegister, tabLogin);
    emailGroup.style.display = 'block';
    submitBtn.textContent    = 'Create account →';
    errEl.style.display      = 'none';
  };

  form.onsubmit = async (e) => {
    e.preventDefault();
    const username = document.getElementById('auth-username').value.trim();
    const password = document.getElementById('auth-password').value;
    const email    = document.getElementById('auth-email')?.value.trim() || '';
    if (!username || !password) return;

    errEl.style.display   = 'none';
    submitBtn.disabled    = true;
    submitBtn.innerHTML   = `<span class="spinner" style="width:13px;height:13px;border-width:1.5px;"></span> Authenticating…`;

    try {
      const endpoint = mode === 'login' ? '/api/v1/auth/login' : '/api/v1/auth/register';
      const payload  = mode === 'login' ? { username, password } : { username, password, email: email || null };

      const res  = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Authentication failed');
      onLoginSuccess(data);
    } catch (err) {
      errEl.textContent   = err.message;
      errEl.style.display = 'block';
    } finally {
      submitBtn.disabled  = false;
      submitBtn.textContent = mode === 'login' ? 'Sign in to ROAR →' : 'Create account →';
    }
  };
}
