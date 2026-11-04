// ui/static/js/app.js
/**
 * Master Application Controller & Router for Project ROAR.
 * Coordinates the public Executive Homepage, the interactive Socratic workspace,
 * real-time agent telemetry, and session state.
 */

import { showToast } from './components/toast.js?v=13.0';
import { renderSidebarCurriculum } from './components/sidebar.js?v=13.0';
import { renderHomeView } from './views/home.js?v=13.0';
import { renderLoginView } from './views/login.js?v=13.0';
import { renderOnboardingView } from './views/onboarding.js?v=13.0';
import { renderLessonView } from './views/lesson.js?v=13.0';
import { renderQuizView } from './views/quiz.js?v=13.0';
import { renderScoreCardView } from './views/score_card.js?v=13.0';
import { renderProgressView } from './views/progress.js?v=13.0';
import { renderSettingsView } from './views/settings.js?v=13.0';
import { renderFinalExamView } from './views/final_exam.js?v=13.0';

class AppState {
  constructor() {
    this.token = localStorage.getItem('prompt_tutor_jwt') || null;
    this.userId = localStorage.getItem('prompt_tutor_uid') || null;
    this.username = localStorage.getItem('prompt_tutor_user') || 'Student';

    // Route inspection
    const params = new URLSearchParams(window.location.search);
    const viewParam = params.get('view');
    const hash = window.location.hash;

    if (viewParam === 'app' || viewParam === 'study' || hash === '#app' || hash === '#study') {
      this.currentView = this.token ? 'study' : 'login';
    } else if (viewParam === 'progress' || hash === '#progress') {
      this.currentView = this.token ? 'progress' : 'login';
    } else if (viewParam === 'exam' || hash === '#exam') {
      this.currentView = this.token ? 'exam' : 'login';
    } else if (viewParam === 'quiz' || hash === '#quiz') {
      this.currentView = this.token ? 'quiz' : 'login';
    } else if (viewParam === 'login' || hash === '#login') {
      this.currentView = 'login';
    } else {
      this.currentView = 'home';
    }

    this.session = null;
    this.selectedNodeId = null;
    this.curriculumNodes = [];
    this.activityDrawerOpen = false;
  }

  setAuth(token, userId, username) {
    this.token = token;
    this.userId = userId;
    this.username = username;
    localStorage.setItem('prompt_tutor_jwt', token);
    localStorage.setItem('prompt_tutor_uid', userId);
    localStorage.setItem('prompt_tutor_user', username);
  }

  clearAuth() {
    this.token = null;
    this.userId = null;
    this.session = null;
    this.selectedNodeId = null;
    localStorage.removeItem('prompt_tutor_jwt');
    localStorage.removeItem('prompt_tutor_uid');
    localStorage.removeItem('prompt_tutor_user');
  }

  isAuthenticated() {
    return !!this.token;
  }
}

const state = new AppState();
const viewContainer = document.getElementById('view-container');
const hpRoot = document.getElementById('homepage-root');
const appRoot = document.getElementById('app-root');

// API helper with Bearer token
async function apiFetch(endpoint, options = {}) {
  const headers = options.headers || {};
  if (state.token) {
    headers['Authorization'] = `Bearer ${state.token}`;
  }
  if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(options.body);
  }
  options.headers = headers;

  const res = await fetch(endpoint, options);
  if (res.status === 401) {
    state.clearAuth();
    state.currentView = 'login';
    renderApp();
    throw new Error('Session expired. Please sign in again.');
  }
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'API request failed');
  }

  if (data.recent_activity) {
    updateActivityFeed(data.recent_activity);
  }

  return data;
}

// 1-Click Guest Demo Login
async function quickDemoLogin() {
  try {
    showToast('Connecting to Demo Workspace…', 'info');
    let res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'demo_student', password: 'demopassword123' })
    });

    if (!res.ok) {
      res = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'demo_student', password: 'demopassword123', email: 'demo@roar.ai' })
      });
    }

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Demo login failed');
    }

    state.setAuth(data.access_token, data.user_id, data.username);
    showToast('Welcome to Project ROAR Demo Workspace', 'success');
    const params = new URLSearchParams(window.location.search);
    state.currentView = (params.get('view') === 'quiz' || window.location.hash === '#quiz') ? 'quiz' : 'study';
    renderApp();
  } catch (err) {
    showToast('Demo access error: ' + err.message, 'error');
    state.currentView = 'login';
    renderApp();
  }
}

// Initial Boot & Global Events
async function init() {
  setupGlobalNavEvents();
  setupActivityDrawer();

  const params = new URLSearchParams(window.location.search);
  if ((params.get('demo') === '1' || params.get('view') === 'demo') && !state.isAuthenticated()) {
    await quickDemoLogin();
    return;
  }

  renderApp();
}

function openSettingsView() {
  state.currentView = 'settings';
  updateNavButtons();
  renderSettingsView(viewContainer, {
    token: state.token,
    onModelChanged: (data) => {
      const isCloud = data.is_cloud !== false;
      const providerLabel = data.active_backend === 'ollama' ? (isCloud ? 'Ollama Cloud' : 'Ollama Local') : 'OpenRouter';
      const label = `${providerLabel}: ${data.active_model}`;

      const sidebarTag = document.getElementById('sidebar-model-tag');
      const headerTag = document.getElementById('header-provider-text');

      if (sidebarTag) sidebarTag.textContent = `${data.active_model}`;
      if (headerTag) headerTag.textContent = label;

      showToast(`Active Provider: ${label}`, 'success');
      refreshActivity();
    }
  });
}

function setupGlobalNavEvents() {
  // Homepage toggles
  const btnSidebarHome = document.getElementById('btn-sidebar-home');
  if (btnSidebarHome) {
    btnSidebarHome.onclick = () => {
      state.currentView = 'home';
      renderApp();
    };
  }

  const btnHeaderHome = document.getElementById('btn-header-home');
  if (btnHeaderHome) {
    btnHeaderHome.onclick = () => {
      state.currentView = 'home';
      renderApp();
    };
  }

  document.getElementById('nav-btn-learn').onclick = () => {
    state.currentView = 'study';
    updateNavButtons();
    loadStudyNode(state.selectedNodeId || state.session?.current_node?.id);
  };

  document.getElementById('nav-btn-progress').onclick = async () => {
    state.currentView = 'progress';
    updateNavButtons();
    try {
      const progressData = await apiFetch('/api/v1/progress/tree');
      renderProgressView(viewContainer, {
        progressData,
        onSelectNode: async (nodeId) => {
          showToast(`Opening ${nodeId}…`, 'info');
          state.currentView = 'study';
          state.selectedNodeId = nodeId;
          updateNavButtons();
          await loadStudyNode(nodeId);
        }
      });
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  document.getElementById('nav-btn-exam').onclick = () => {
    state.currentView = 'exam';
    updateNavButtons();
    renderFinalExamView(viewContainer, {
      token: state.token,
      onExamCompleted: (result) => {
        showToast('Final Exam Submitted', result.passed ? 'success' : 'warning');
      }
    });
  };

  document.getElementById('btn-settings-toggle').onclick = openSettingsView;

  const headerProviderBtn = document.getElementById('btn-header-provider-badge');
  if (headerProviderBtn) headerProviderBtn.onclick = openSettingsView;

  const sidebarModelContainer = document.getElementById('sidebar-model-container');
  if (sidebarModelContainer) sidebarModelContainer.onclick = openSettingsView;

  document.getElementById('btn-logout').onclick = () => {
    state.clearAuth();
    showToast('Signed out of workspace.', 'info');
    state.currentView = 'home';
    renderApp();
  };
}

function setupActivityDrawer() {
  const toggleBtn = document.getElementById('btn-toggle-activity-feed');
  const closeBtn  = document.getElementById('btn-close-activity-drawer');
  const drawer    = document.getElementById('activity-drawer');

  if (toggleBtn) {
    toggleBtn.onclick = () => {
      state.activityDrawerOpen = !state.activityDrawerOpen;
      drawer.style.display = state.activityDrawerOpen ? 'block' : 'none';
      if (state.activityDrawerOpen) refreshActivity();
    };
  }

  if (closeBtn) {
    closeBtn.onclick = () => {
      state.activityDrawerOpen = false;
      drawer.style.display = 'none';
    };
  }
}

async function refreshActivity() {
  if (!state.isAuthenticated()) return;
  try {
    const data = await apiFetch('/api/v1/session/activity');
    if (data.events) {
      updateActivityFeed(data.events);
    }
  } catch (e) {
    // Silent background fetch
  }
}

function updateActivityFeed(events) {
  const list = document.getElementById('activity-events-list');
  if (!list || !events || events.length === 0) return;

  list.innerHTML = events.slice().reverse().map(ev => {
    let dotColor = 'var(--c-accent)';
    let agentColor = 'var(--c-accent)';
    if (ev.status === 'success') { agentColor = 'var(--c-success)'; dotColor = 'var(--c-success)'; }
    if (ev.status === 'error')   { agentColor = 'var(--c-danger)';  dotColor = 'var(--c-danger)';  }
    if (ev.status === 'warning') { agentColor = 'var(--c-amber)';   dotColor = 'var(--c-amber)';   }

    return `
      <div class="log-entry">
        <div class="log-dot" style="background:${dotColor};"></div>
        <span class="log-time">${ev.timestamp}</span>
        <div>
          <strong class="log-agent" style="color:${agentColor};">${ev.agent}</strong>
          <span class="log-action"> ${ev.action}</span>
          ${ev.details ? `<div style="color:var(--c-text-3);font-size:10px;margin-top:2px;">${ev.details}</div>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function updateNavButtons() {
  const btnLearn = document.getElementById('nav-btn-learn');
  const btnProg  = document.getElementById('nav-btn-progress');
  const btnExam  = document.getElementById('nav-btn-exam');

  if (btnLearn && btnProg && btnExam) {
    [btnLearn, btnProg, btnExam].forEach(b => {
      b.className = 'sb-tab';
    });

    if (state.currentView === 'study')    btnLearn.className = 'sb-tab active';
    if (state.currentView === 'progress') btnProg.className  = 'sb-tab active';
    if (state.currentView === 'exam')     btnExam.className  = 'sb-tab active';
  }
}

// Master Render Router
async function renderApp() {
  // 1. Home View
  if (state.currentView === 'home') {
    document.body.classList.remove('in-workspace');
    if (appRoot) appRoot.style.display = 'none';
    if (hpRoot) {
      hpRoot.style.display = 'block';
      renderHomeView(hpRoot, {
        isAuthenticated: state.isAuthenticated(),
        username: state.username,
        onLaunchApp: () => {
          state.currentView = state.isAuthenticated() ? 'study' : 'login';
          renderApp();
        },
        onOpenLogin: () => {
          state.currentView = 'login';
          renderApp();
        },
        onQuickDemo: () => {
          if (state.isAuthenticated()) {
            state.currentView = 'study';
            renderApp();
          } else {
            quickDemoLogin();
          }
        }
      });
      window.scrollTo(0, 0);
    }
    return;
  }

  // 2. Login View
  if (state.currentView === 'login') {
    if (appRoot) appRoot.style.display = 'none';
    if (hpRoot) {
      hpRoot.style.display = 'block';
      renderLoginView(hpRoot, {
        onLoginSuccess: (authData) => {
          state.setAuth(authData.access_token, authData.user_id, authData.username);
          showToast(`Welcome, ${authData.username}`, 'success');
          state.currentView = 'study';
          renderApp();
        },
        onBackToHome: () => {
          state.currentView = 'home';
          renderApp();
        },
        onGuestDemo: () => {
          quickDemoLogin();
        }
      });
      window.scrollTo(0, 0);
    }
    return;
  }

  // 3. Workspace Views (require authentication)
  if (!state.isAuthenticated()) {
    state.currentView = 'login';
    renderApp();
    return;
  }

  if (hpRoot) hpRoot.style.display = 'none';
  if (appRoot) appRoot.style.display = 'flex';
  document.body.classList.add('in-workspace');
  window.scrollTo(0, 0);

  const sidebarEl = document.getElementById('sidebar-container');
  if (sidebarEl) sidebarEl.style.display = '';
  const usernameEl = document.getElementById('sidebar-username');
  if (usernameEl) usernameEl.textContent = state.username;

  try {
    const sessionData = await apiFetch('/api/v1/session/start', { method: 'POST' });
    state.session = sessionData;
    if (!state.selectedNodeId) {
      state.selectedNodeId = sessionData.current_node.id;
    }

    // Fetch model info
    try {
      const modelInfo = await apiFetch('/api/v1/model/info');
      const isCloud = modelInfo.is_cloud !== false;
      const providerLabel = modelInfo.backend === 'ollama' ? (isCloud ? 'Ollama Cloud' : 'Ollama Local') : 'OpenRouter';
      const label = `${providerLabel}: ${modelInfo.model}`;

      const sidebarTag = document.getElementById('sidebar-model-tag');
      const headerTag = document.getElementById('header-provider-text');

      if (sidebarTag) sidebarTag.textContent = `${modelInfo.model}`;
      if (headerTag) headerTag.textContent = label;
    } catch (e) {}

    // Fetch curriculum tree
    const progressData = await apiFetch('/api/v1/progress/tree');
    state.curriculumNodes = progressData.nodes;

    // Render sidebar curriculum
    renderSidebarCurriculum(state.curriculumNodes, state.selectedNodeId, (nodeId) => {
      state.selectedNodeId = nodeId;
      loadStudyNode(nodeId);
    });

    const progressBadge = document.getElementById('sidebar-progress-badge');
    if (progressBadge) {
      progressBadge.textContent = `${progressData.completed_nodes_count}/${progressData.total_nodes}`;
    }

    // Onboarding check
    if (!sessionData.profile.onboarding_done) {
      renderOnboardingView(viewContainer, {
        token: state.token,
        onOnboardingComplete: (updatedSession) => {
          state.session = updatedSession;
          state.selectedNodeId = updatedSession.current_node.id;
          showToast('Onboarding completed. Starting Lesson 1…', 'success');
          if (state.currentView === 'quiz') {
      startQuizFlow(false, state.selectedNodeId);
      return;
    }

    loadStudyNode(state.selectedNodeId);
        }
      });
      return;
    }

    if (state.currentView === 'quiz') {
      startQuizFlow(false, state.selectedNodeId);
      return;
    }

    loadStudyNode(state.selectedNodeId);
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function loadStudyNode(nodeId, isRegen = false) {
  state.currentView = 'study';
  updateNavButtons();

  if (viewContainer) {
    viewContainer.scrollTop = 0;
  }

  const targetId = nodeId || state.selectedNodeId || state.session?.current_node?.id || 'node_01';
  state.selectedNodeId = targetId;

  if (isRegen) {
    showToast('Synthesizing fresh lesson variation…', 'info');
  }

  viewContainer.innerHTML = `
    <div class="animate-in" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:280px;gap:14px;color:var(--c-text-2);">
      <div class="spinner"></div>
      <div style="font-size:13px;font-weight:600;color:var(--c-text);">${isRegen ? 'Synthesizing fresh lesson variation…' : 'Lesson Agent synthesizing'}</div>
      <div style="font-family:var(--font-mono);font-size:11px;color:var(--c-text-3);">Querying vector store and formatting topic guide…</div>
    </div>
  `;

  try {
    const lessonData = await apiFetch(`/api/v1/lesson/current?node_id=${targetId}${isRegen ? '&regen=true' : ''}&_t=${Date.now()}`);
    updateHeader(lessonData.topic_title, lessonData.difficulty_tier, lessonData.is_passed ? 'MASTERED' : 'LESSON', lessonData.category);

    if (state.curriculumNodes) {
      renderSidebarCurriculum(state.curriculumNodes, targetId, (clickedId) => {
        state.selectedNodeId = clickedId;
        loadStudyNode(clickedId);
      });
    }

    renderLessonView(viewContainer, {
      lessonData,
      isExpert: state.session?.profile?.prior_experience === 'expert',
      onStartQuiz: () => startQuizFlow(false, targetId),
      onSkipToQuiz: () => startQuizFlow(true, targetId),
      onRegenerateLesson: () => loadStudyNode(targetId, true)
    });
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function startQuizFlow(isSkip = false, nodeId = null, isRegen = false) {
  const targetId = nodeId || state.selectedNodeId || 'node_01';

  if (isRegen) {
    showToast('Synthesizing challenge question set…', 'info');
  }

  viewContainer.innerHTML = `
    <div class="animate-in" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:280px;gap:14px;">
      <div class="spinner"></div>
      <div style="font-size:13px;font-weight:600;color:var(--c-text);">${isRegen ? 'Quiz Agent formulating fresh questions…' : 'Quiz Agent formulating challenge'}</div>
      <div style="font-family:var(--font-mono);font-size:11px;color:var(--c-text-3);">Synthesizing questions calibrated to difficulty tier…</div>
    </div>
  `;

  try {
    const quizData = await apiFetch(`/api/v1/quiz/current?node_id=${targetId}${isRegen ? '&regen=true' : ''}&_t=${Date.now()}`);
    updateHeader(quizData.topic_title, quizData.difficulty_tier, 'QUIZ', quizData.category || 'Assessment');

    renderQuizView(viewContainer, {
      quizData,
      onRequestHint: async (qIdx = 1) => {
        return await apiFetch('/api/v1/quiz/hint', {
          method: 'POST',
          body: { node_id: targetId, question_idx: Number(qIdx) || 1 }
        });
      },

      onRegenerateQuiz: () => startQuizFlow(false, targetId, true),
      onSubmitAnswer: async (answersMap, meta = {}) => {
        const scoreData = await apiFetch('/api/v1/quiz/submit', {
          method: 'POST',
          body: {
            node_id: targetId,
            student_answers: answersMap,
            time_elapsed_seconds: meta.timeElapsed || 45.0,
            hints_used: meta.hintsUsed || 0
          }
        });

        const progressData = await apiFetch('/api/v1/progress/tree');
        state.curriculumNodes = progressData.nodes;
        renderSidebarCurriculum(state.curriculumNodes, targetId, (clickedId) => {
          state.selectedNodeId = clickedId;
          loadStudyNode(clickedId);
        });

        const progressBadge = document.getElementById('sidebar-progress-badge');
        if (progressBadge) {
          progressBadge.textContent = `${progressData.completed_nodes_count}/${progressData.total_nodes}`;
        }

        renderScoreCardView(viewContainer, {
          scoreData,
          onAdvanceNode: async () => {
            if (scoreData.next_node_id) {
              state.selectedNodeId = scoreData.next_node_id;
              await loadStudyNode(scoreData.next_node_id);
            } else {
              showToast('Curriculum Complete. Proceeding to Final Exam.', 'success');
              state.currentView = 'exam';
              updateNavButtons();
              renderFinalExamView(viewContainer, { token: state.token });
            }
          },
          onRetryNode: () => loadStudyNode(targetId)
        });
      }
    });
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function updateHeader(title, tier, phase, category = '') {
  const nodeTitle = document.getElementById('header-node-title');
  const tierBadge = document.getElementById('header-tier-badge');
  const phaseBadge = document.getElementById('header-phase-badge');

  if (nodeTitle) {
    nodeTitle.innerHTML = category
      ? `<span style="color:var(--c-text-3);">${category}</span> <span style="color:var(--c-border-hi);margin:0 4px;">/</span> <span style="color:#FFFFFF;">${title}</span>`
      : title;
  }
  if (tierBadge) tierBadge.textContent = `Tier ${tier}`;
  if (phaseBadge) phaseBadge.textContent = phase;
}

// Boot application
window.addEventListener('DOMContentLoaded', init);
