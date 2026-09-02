// ui/static/js/views/settings.js
/**
 * Dedicated Inference Provider Settings:
 * 1. Ollama Cloud Web API (https://api.ollama.com) & Ollama Local Daemon (http://localhost:11434)
 * 2. OpenRouter Cloud API (https://openrouter.ai/api/v1)
 * Real live API key validation and dynamic model fetching with high-contrast, developer-grade UI.
 */

export function renderSettingsView(container, { token, onModelChanged }) {
  container.innerHTML = `
    <div class="animate-in" style="width:100%;max-width:680px;display:flex;flex-direction:column;gap:18px;">

      <!-- Header Card -->
      <div class="card" style="padding:24px;">
        <div class="section-label" style="color:var(--c-accent);margin-bottom:6px;">Inference Provider Architecture</div>
        <h1 style="font-size:20px;font-weight:700;color:var(--c-text);letter-spacing:-0.02em;margin:0 0 6px;">Model &amp; API Key Configuration</h1>
        <p style="font-size:12.5px;color:var(--c-text-2);line-height:1.6;margin:0;">
          Select between <strong>Ollama Cloud (Web API)</strong>, <strong>Ollama Local Daemon</strong>, or <strong>OpenRouter</strong>. Every model list is fetched live from your provider.
        </p>
      </div>

      <!-- Main Provider Card -->
      <div class="card" style="padding:24px;display:flex;flex-direction:column;gap:20px;">
        
        <!-- Tab Selector: Ollama vs OpenRouter -->
        <div>
          <div class="section-label" style="margin-bottom:10px;">Select Provider</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
            <button type="button" id="tab-ollama" class="option-card selected" style="text-align:left;width:100%;">
              <span style="font-size:22px;line-height:1;">🦙</span>
              <div>
                <div class="option-title">Ollama (Cloud &amp; Local)</div>
                <div class="option-desc">Web API (api.ollama.com) or Localhost</div>
              </div>
            </button>

            <button type="button" id="tab-openrouter" class="option-card" style="text-align:left;width:100%;">
              <span style="font-size:22px;line-height:1;">🌐</span>
              <div>
                <div class="option-title">OpenRouter Cloud</div>
                <div class="option-desc">Llama-3.3, Claude, Gemini, DeepSeek</div>
              </div>
            </button>
          </div>
        </div>

        <!-- ================= 1. OLLAMA CONFIGURATION SECTION ================= -->
        <div id="section-ollama" style="display:flex;flex-direction:column;gap:16px;">
          <!-- Ollama Host Mode (Cloud vs Local) -->
          <div>
            <label style="display:block;font-size:12px;font-weight:600;color:var(--c-text-2);margin-bottom:8px;">Ollama Connection Mode</label>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
              <label class="option-card selected" id="label-mode-cloud" style="margin:0;">
                <input type="radio" name="ollama_mode" value="cloud" checked style="display:none;">
                <div class="option-radio"><div class="option-radio-dot"></div></div>
                <div>
                  <div class="option-title">☁️ Ollama Cloud API (Web)</div>
                  <div style="font-family:var(--font-mono);font-size:10.5px;color:var(--c-text-3);margin-top:2px;">https://api.ollama.com</div>
                </div>
              </label>

              <label class="option-card" id="label-mode-local" style="margin:0;">
                <input type="radio" name="ollama_mode" value="local" style="display:none;">
                <div class="option-radio"><div class="option-radio-dot"></div></div>
                <div>
                  <div class="option-title">🖥️ Ollama Local Daemon</div>
                  <div style="font-family:var(--font-mono);font-size:10.5px;color:var(--c-text-3);margin-top:2px;">http://localhost:11434</div>
                </div>
              </label>
            </div>
          </div>

          <!-- Ollama Host (Editable) -->
          <div id="group-ollama-host">
            <label style="display:block;font-size:12px;font-weight:600;color:var(--c-text-2);margin-bottom:6px;">Host Endpoint URL</label>
            <input type="text" id="input-ollama-host" value="https://api.ollama.com" class="field-input" style="font-family:var(--font-mono);font-size:12px;">
          </div>

          <!-- Ollama API Key -->
          <div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
              <label style="font-size:12px;font-weight:600;color:var(--c-text-2);">Ollama API Key</label>
              <button type="button" id="btn-verify-ollama-key" class="btn btn-ghost" style="font-size:11px;padding:3px 8px;height:auto;gap:4px;">
                ⚡ Refresh Models
              </button>
            </div>
            <input type="password" id="input-ollama-key" value="bde6d88060dc48fa9261e6c378318715.CpVL75eu-kd23mJlzF48uD50" placeholder="Paste your Ollama Cloud API key..." class="field-input" style="font-family:var(--font-mono);font-size:12px;">
          </div>

          <!-- Ollama Key Status Badge -->
          <div id="ollama-key-status" style="display:flex;align-items:center;gap:8px;padding:10px 14px;border:1px solid rgba(74,222,128,0.25);border-radius:var(--r-md);background:rgba(74,222,128,0.08);font-family:var(--font-mono);font-size:11.5px;color:#4ADE80;">
            <span>🟢</span>
            <span><strong>Valid API Key:</strong> Authenticated with Ollama Cloud API</span>
          </div>

          <!-- Dynamic Model Selection -->
          <div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
              <label style="font-size:12px;font-weight:600;color:var(--c-text-2);">Select Model</label>
              <span id="model-count-badge" class="tag" style="font-size:10px;padding:2px 8px;color:var(--c-accent);border-color:rgba(232,200,74,0.3);background:var(--c-accent-dim);">Loading models...</span>
            </div>
            <select id="select-ollama-model" class="field-input" style="font-family:var(--font-mono);font-size:12px;cursor:pointer;">
              <option value="gpt-oss:20b" selected>gpt-oss:20b (Recommended - Cloud Fast 20B)</option>
            </select>
          </div>
        </div>

        <!-- ================= 2. OPENROUTER CONFIGURATION SECTION ================= -->
        <div id="section-openrouter" style="display:none;flex-direction:column;gap:16px;">
          <div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
              <label style="font-size:12px;font-weight:600;color:var(--c-text-2);">OpenRouter API Key (Required)</label>
              <button type="button" id="btn-verify-openrouter-key" class="btn btn-ghost" style="font-size:11px;padding:3px 8px;height:auto;gap:4px;">
                ⚡ Verify Key
              </button>
            </div>
            <input type="password" id="input-openrouter-key" placeholder="sk-or-v1-..." class="field-input" style="font-family:var(--font-mono);font-size:12px;">
            <div style="font-size:11px;color:var(--c-text-3);margin-top:4px;">Get your key from <a href="https://openrouter.ai/keys" target="_blank" style="color:var(--c-accent);text-decoration:underline;">openrouter.ai/keys</a></div>
          </div>

          <!-- OpenRouter Key Status Badge -->
          <div id="openrouter-key-status" style="display:none;padding:10px 14px;border-radius:var(--r-md);font-family:var(--font-mono);font-size:11.5px;"></div>

          <!-- OpenRouter Model Dropdown -->
          <div>
            <label style="display:block;font-size:12px;font-weight:600;color:var(--c-text-2);margin-bottom:6px;">Select OpenRouter Model</label>
            <select id="select-openrouter-model" class="field-input" style="font-family:var(--font-mono);font-size:12px;cursor:pointer;">
              <option value="meta-llama/llama-3.3-70b-instruct">meta-llama/llama-3.3-70b-instruct (Recommended)</option>
              <option value="google/gemini-2.0-flash-001">google/gemini-2.0-flash-001 (Ultra Fast)</option>
              <option value="deepseek/deepseek-r1">deepseek/deepseek-r1 (Reasoning)</option>
              <option value="anthropic/claude-3.5-sonnet">anthropic/claude-3.5-sonnet</option>
              <option value="qwen/qwen-2.5-72b-instruct">qwen/qwen-2.5-72b-instruct</option>
            </select>
          </div>
        </div>

        <!-- Connection Test Result Banner -->
        <div id="test-status-banner" style="display:none;padding:10px 14px;border-radius:var(--r-md);font-family:var(--font-mono);font-size:11.5px;"></div>

        <!-- Action Footer -->
        <div style="display:flex;align-items:center;gap:10px;padding-top:16px;border-top:1px solid var(--c-border);flex-wrap:wrap;">
          <button type="button" id="btn-test-ping" class="btn btn-ghost" style="padding:10px 18px;font-size:12.5px;">
            ⚡ Test Inference Ping
          </button>
          <button type="button" id="btn-save-provider" class="btn btn-primary" style="flex:1;padding:10px 22px;font-size:13px;font-weight:700;justify-content:center;color:#000000 !important;background:var(--c-accent);">
            Save &amp; Activate Provider 🚀
          </button>
        </div>

      </div>

    </div>
  `;

  // Elements
  let activeProvider = 'ollama'; // 'ollama' or 'openrouter'

  const tabOllama = document.getElementById('tab-ollama');
  const tabOpenRouter = document.getElementById('tab-openrouter');
  const secOllama = document.getElementById('section-ollama');
  const secOpenRouter = document.getElementById('section-openrouter');

  const ollamaHostInput = document.getElementById('input-ollama-host');
  const ollamaKeyInput = document.getElementById('input-ollama-key');
  const ollamaKeyStatus = document.getElementById('ollama-key-status');
  const ollamaModelSelect = document.getElementById('select-ollama-model');
  const modelCountBadge = document.getElementById('model-count-badge');
  const btnVerifyOllama = document.getElementById('btn-verify-ollama-key');

  const openRouterKeyInput = document.getElementById('input-openrouter-key');
  const openRouterKeyStatus = document.getElementById('openrouter-key-status');
  const openRouterModelSelect = document.getElementById('select-openrouter-model');
  const btnVerifyOpenRouter = document.getElementById('btn-verify-openrouter-key');

  const btnTestPing = document.getElementById('btn-test-ping');
  const btnSave = document.getElementById('btn-save-provider');
  const testStatus = document.getElementById('test-status-banner');

  // Helper: Live Fetch Ollama Models
  async function fetchOllamaModels(showLoading = false) {
    if (showLoading) {
      btnVerifyOllama.textContent = 'Fetching...';
      ollamaKeyStatus.style.display = 'flex';
      ollamaKeyStatus.style.borderColor = 'rgba(232,200,74,0.3)';
      ollamaKeyStatus.style.background = 'var(--c-accent-dim)';
      ollamaKeyStatus.style.color = 'var(--c-accent)';
      ollamaKeyStatus.innerHTML = '<span>⏳</span><span>Validating key & fetching live models...</span>';
    }

    try {
      const res = await fetch('/api/v1/model/validate-ollama', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          host: ollamaHostInput.value.trim(),
          api_key: ollamaKeyInput.value.trim()
        })
      });
      const data = await res.json();

      if (data.valid) {
        ollamaKeyStatus.style.display = 'flex';
        ollamaKeyStatus.style.borderColor = 'rgba(74,222,128,0.3)';
        ollamaKeyStatus.style.background = 'rgba(74,222,128,0.08)';
        ollamaKeyStatus.style.color = '#4ADE80';
        ollamaKeyStatus.innerHTML = `<span>🟢</span><span><strong>${data.message}</strong></span>`;

        if (data.models && data.models.length > 0) {
          modelCountBadge.textContent = `${data.models.length} Cloud Models Available`;
          const currentSelected = ollamaModelSelect.value || 'gpt-oss:20b';
          ollamaModelSelect.innerHTML = data.models.map(m => `
            <option value="${m}" ${m === currentSelected || (m === 'gpt-oss:20b' && !data.models.includes(currentSelected)) ? 'selected' : ''}>
              ${m} ${m === 'gpt-oss:20b' ? '⚡ (Active Cloud Model)' : ''}
            </option>
          `).join('');
        }
      } else {
        modelCountBadge.textContent = 'Authentication Error';
        ollamaKeyStatus.style.display = 'flex';
        ollamaKeyStatus.style.borderColor = 'rgba(248,113,113,0.3)';
        ollamaKeyStatus.style.background = 'rgba(248,113,113,0.08)';
        ollamaKeyStatus.style.color = '#F87171';
        ollamaKeyStatus.innerHTML = `<span>❌</span><span><strong>Verification Failed:</strong> ${data.error}</span>`;
      }
    } catch (err) {
      modelCountBadge.textContent = 'Connection Failed';
      ollamaKeyStatus.style.display = 'flex';
      ollamaKeyStatus.style.borderColor = 'rgba(248,113,113,0.3)';
      ollamaKeyStatus.style.background = 'rgba(248,113,113,0.08)';
      ollamaKeyStatus.style.color = '#F87171';
      ollamaKeyStatus.innerHTML = `<span>❌</span><span><strong>Network Error:</strong> ${err.message}</span>`;
    } finally {
      btnVerifyOllama.textContent = '⚡ Refresh Models';
    }
  }

  // Initial Auto-Fetch on Render
  fetchOllamaModels(false);

  // Tab switching
  tabOllama.onclick = () => {
    activeProvider = 'ollama';
    tabOllama.classList.add('selected');
    tabOpenRouter.classList.remove('selected');
    secOllama.style.display = 'flex';
    secOpenRouter.style.display = 'none';
    testStatus.style.display = 'none';
  };

  tabOpenRouter.onclick = () => {
    activeProvider = 'openrouter';
    tabOpenRouter.classList.add('selected');
    tabOllama.classList.remove('selected');
    secOpenRouter.style.display = 'flex';
    secOllama.style.display = 'none';
    testStatus.style.display = 'none';
  };

  // Ollama Mode Radio Change
  const modeCloud = document.getElementById('label-mode-cloud');
  const modeLocal = document.getElementById('label-mode-local');

  document.querySelectorAll('input[name="ollama_mode"]').forEach(radio => {
    radio.onchange = () => {
      if (radio.value === 'cloud') {
        modeCloud?.classList.add('selected');
        modeLocal?.classList.remove('selected');
        ollamaHostInput.value = 'https://api.ollama.com';
      } else {
        modeLocal?.classList.add('selected');
        modeCloud?.classList.remove('selected');
        ollamaHostInput.value = 'http://localhost:11434';
      }
      fetchOllamaModels(true);
    };
  });

  // Verify / Refresh Button
  btnVerifyOllama.onclick = () => fetchOllamaModels(true);

  // Verify OpenRouter API Key
  btnVerifyOpenRouter.onclick = async () => {
    const key = openRouterKeyInput.value.trim();
    if (!key) {
      alert('Please enter an OpenRouter API key.');
      return;
    }
    btnVerifyOpenRouter.textContent = 'Verifying...';
    openRouterKeyStatus.style.display = 'flex';
    openRouterKeyStatus.style.borderColor = 'rgba(232,200,74,0.3)';
    openRouterKeyStatus.style.background = 'var(--c-accent-dim)';
    openRouterKeyStatus.style.color = 'var(--c-accent)';
    openRouterKeyStatus.innerHTML = '<span>⏳</span><span>Validating key with OpenRouter...</span>';

    try {
      const res = await fetch('/api/v1/model/validate-openrouter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: key })
      });
      const data = await res.json();

      if (data.valid) {
        openRouterKeyStatus.style.borderColor = 'rgba(74,222,128,0.3)';
        openRouterKeyStatus.style.background = 'rgba(74,222,128,0.08)';
        openRouterKeyStatus.style.color = '#4ADE80';
        openRouterKeyStatus.innerHTML = `<span>🟢</span><span><strong>${data.message}</strong></span>`;
      } else {
        openRouterKeyStatus.style.borderColor = 'rgba(248,113,113,0.3)';
        openRouterKeyStatus.style.background = 'rgba(248,113,113,0.08)';
        openRouterKeyStatus.style.color = '#F87171';
        openRouterKeyStatus.innerHTML = `<span>❌</span><span><strong>Verification Failed:</strong> ${data.error}</span>`;
      }
    } catch (err) {
      openRouterKeyStatus.style.borderColor = 'rgba(248,113,113,0.3)';
      openRouterKeyStatus.style.background = 'rgba(248,113,113,0.08)';
      openRouterKeyStatus.style.color = '#F87171';
      openRouterKeyStatus.innerHTML = `<span>❌</span><span><strong>Network Error:</strong> ${err.message}</span>`;
    } finally {
      btnVerifyOpenRouter.textContent = '⚡ Verify Key';
    }
  };

  // Get current active payload
  function getCurrentPayload() {
    if (activeProvider === 'ollama') {
      return {
        backend: 'ollama',
        model: ollamaModelSelect.value || 'gpt-oss:20b',
        ollama_host: ollamaHostInput.value.trim() || 'https://api.ollama.com',
        api_key: ollamaKeyInput.value.trim() || null,
        base_url: null
      };
    } else {
      return {
        backend: 'openrouter',
        model: openRouterModelSelect.value || 'meta-llama/llama-3.3-70b-instruct',
        api_key: openRouterKeyInput.value.trim(),
        base_url: 'https://openrouter.ai/api/v1',
        ollama_host: null
      };
    }
  }

  // Test Inference Ping
  btnTestPing.onclick = async () => {
    const payload = getCurrentPayload();
    btnTestPing.disabled = true;
    btnTestPing.innerHTML = '<span>⏳ Pinging Model...</span>';
    testStatus.style.display = 'flex';
    testStatus.style.borderColor = 'rgba(232,200,74,0.3)';
    testStatus.style.background = 'var(--c-accent-dim)';
    testStatus.style.color = 'var(--c-accent)';
    testStatus.innerHTML = '<span>⚡ Sending test token generation request...</span>';

    try {
      const res = await fetch('/api/v1/model/test-connection', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (data.success) {
        testStatus.style.borderColor = 'rgba(74,222,128,0.3)';
        testStatus.style.background = 'rgba(74,222,128,0.08)';
        testStatus.style.color = '#4ADE80';
        testStatus.innerHTML = `<span>✅</span><div><strong>Ping Success!</strong> ${data.message} (${data.latency_ms}ms)</div>`;
      } else {
        testStatus.style.borderColor = 'rgba(248,113,113,0.3)';
        testStatus.style.background = 'rgba(248,113,113,0.08)';
        testStatus.style.color = '#F87171';
        testStatus.innerHTML = `<span>❌</span><div><strong>Ping Failed:</strong> ${data.error}</div>`;
      }
    } catch (err) {
      testStatus.style.borderColor = 'rgba(248,113,113,0.3)';
      testStatus.style.background = 'rgba(248,113,113,0.08)';
      testStatus.style.color = '#F87171';
      testStatus.innerHTML = `<span>❌</span><div><strong>Network Error:</strong> ${err.message}</div>`;
    } finally {
      btnTestPing.disabled = false;
      btnTestPing.innerHTML = '⚡ Test Inference Ping';
    }
  };

  // Save & Apply
  btnSave.onclick = async () => {
    const payload = getCurrentPayload();
    btnSave.disabled = true;
    btnSave.innerHTML = '<span>Activating Provider...</span>';

    try {
      const res = await fetch('/api/v1/model/switch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      onModelChanged(data);
      alert(`🎉 Active Provider Configured!\n\nBackend: ${data.active_backend.toUpperCase()}\nModel: ${data.active_model}\nEndpoint: ${data.active_host}`);
    } catch (err) {
      alert('Failed to save provider: ' + err.message);
    } finally {
      btnSave.disabled = false;
      btnSave.innerHTML = 'Save & Activate Provider 🚀';
    }
  };
}
