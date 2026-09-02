// ui/static/js/app.js
/**
 * Master Application Controller & Router for PromptTutor AI.
 * Coordinates views, live agent activity telemetry, and study flow.
 */

import { showToast } from './components/toast.js';
import { renderSidebarCurriculum } from './components/sidebar.js';
import { renderLoginView } from './views/login.js';
import { renderOnboardingView } from './views/onboarding.js';
import { renderLessonView } from './views/lesson.js';
import { renderQuizView } from './views/quiz.js';
import { renderScoreCardView } from './views/score_card.js';
import { renderProgressView } from './views/progress.js';
import { renderSettingsView } from './views/settings.js';
import { renderFinalExamView } from './views/final_exam.js';

class AppState {
  constructor() {
    this.token = localStorage.getItem('prompt_tutor_jwt') || null;
    this.userId = localStorage.getItem('prompt_tutor_uid') || null;
    this.username = localStorage.getItem('prompt_tutor_user') || 'Student';
    this.currentView = 'study'; // 'study', 'progress', 'settings', 'exam'
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
    renderApp();
    throw new Error('Session expired. Please log in again.');
  }
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'API request failed');
  }

  // Update activity feed if events returned
  if (data.recent_activity) {
    updateActivityFeed(data.recent_activity);
  }

  return data;
}

// Initial Boot & Router
async function init() {
  setupGlobalNavEvents();
  setupActivityDrawer();
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
          showToast(`Opening ${nodeId}...`, 'info');
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
        showToast('Final Exam Submitted!', result.passed ? 'success' : 'warning');
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
    showToast('Logged out.', 'info');
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
    // Ignore silent fetch
  }
}

function updateActivityFeed(events) {
  const list = document.getElementById('activity-events-list');
  if (!list || !events || events.length === 0) return;

  list.innerHTML = events.slice().reverse().map(ev => {
    let dotColor = '#818CF8';
    let agentColor = '#818CF8';
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

  [btnLearn, btnProg, btnExam].forEach(b => {
    b.className = 'sb-tab';
  });

  if (state.currentView === 'study')    btnLearn.className = 'sb-tab active';
  if (state.currentView === 'progress') btnProg.className  = 'sb-tab active';
  if (state.currentView === 'exam')     btnExam.className  = 'sb-tab active';
}


async function renderApp() {
  if (!state.isAuthenticated()) {
    document.getElementById('sidebar-container').style.display = 'none';
    renderLoginView(viewContainer, {
      onLoginSuccess: (authData) => {
        state.setAuth(authData.access_token, authData.user_id, authData.username);
        showToast(`Welcome, ${authData.username}!`, 'success');
        document.getElementById('sidebar-container').style.display = '';
        renderApp();
      }
    });
    return;
  }

  document.getElementById('sidebar-container').style.display = '';
  document.getElementById('sidebar-username').textContent = state.username;


  try {
    const sessionData = await apiFetch('/api/v1/session/start', { method: 'POST' });
    state.session = sessionData;
    if (!state.selectedNodeId) {
      state.selectedNodeId = sessionData.current_node.id;
    }

    // Fetch model info to update header & sidebar tags
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

    // Fetch curriculum tree for sidebar
    const progressData = await apiFetch('/api/v1/progress/tree');
    state.curriculumNodes = progressData.nodes;

    // Update sidebar
    renderSidebarCurriculum(state.curriculumNodes, state.selectedNodeId, (nodeId) => {
      state.selectedNodeId = nodeId;
      loadStudyNode(nodeId);
    });

    document.getElementById('sidebar-progress-badge').textContent = `${progressData.completed_nodes_count}/${progressData.total_nodes}`;

    // Check onboarding
    if (!sessionData.profile.onboarding_done) {
      renderOnboardingView(viewContainer, {
        token: state.token,
        onOnboardingComplete: (updatedSession) => {
          state.session = updatedSession;
          state.selectedNodeId = updatedSession.current_node.id;
          showToast('Onboarding completed! Starting Lesson 1...', 'success');
          loadStudyNode(state.selectedNodeId);
        }
      });
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
  
  const targetId = nodeId || state.selectedNodeId || state.session?.current_node?.id || 'node_01';
  state.selectedNodeId = targetId;

  if (isRegen) {
    showToast('Regenerating fresh lesson guide with alternative examples…', 'info');
  }

  viewContainer.innerHTML = `
    <div class="animate-in" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:280px;gap:14px;color:var(--c-text-2);">
      <div class="spinner"></div>
      <div style="font-size:13px;font-weight:600;color:var(--c-text);">${isRegen ? 'Synthesizing fresh lesson variation…' : 'Lesson Agent synthesizing'}</div>
      <div style="font-family:var(--font-mono);font-size:11px;color:var(--c-text-3);">Querying vector store &amp; formatting topic guide…</div>
    </div>
  `;

  try {
    const lessonData = await apiFetch(`/api/v1/lesson/current?node_id=${targetId}${isRegen ? '&regen=true' : ''}&_t=${Date.now()}`);
    updateHeader(lessonData.topic_title, lessonData.difficulty_tier, lessonData.is_passed ? 'MASTERED' : 'LESSON');

    // Refresh sidebar active highlight
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
    showToast('Synthesizing fresh challenge question set…', 'info');
  }

  viewContainer.innerHTML = `
    <div class="animate-in" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:280px;gap:14px;">
      <div class="spinner"></div>
      <div style="font-size:13px;font-weight:600;color:var(--c-text);">${isRegen ? 'Quiz Agent formulating fresh questions…' : 'Quiz Agent formulating challenge'}</div>
      <div style="font-family:var(--font-mono);font-size:11px;color:var(--c-text-3);">Synthesizing 3 questions calibrated to difficulty weight…</div>
    </div>
  `;

  try {
    const quizData = await apiFetch(`/api/v1/quiz/current?node_id=${targetId}${isRegen ? '&regen=true' : ''}&_t=${Date.now()}`);
    updateHeader(quizData.topic_title, quizData.difficulty_tier, 'QUIZ');

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


        // Re-fetch curriculum tree to update progress badges
        const progressData = await apiFetch('/api/v1/progress/tree');
        state.curriculumNodes = progressData.nodes;
        renderSidebarCurriculum(state.curriculumNodes, targetId, (clickedId) => {
          state.selectedNodeId = clickedId;
          loadStudyNode(clickedId);
        });
        document.getElementById('sidebar-progress-badge').textContent = `${progressData.completed_nodes_count}/${progressData.total_nodes}`;

        renderScoreCardView(viewContainer, {
          scoreData,
          onAdvanceNode: async () => {
            if (scoreData.next_node_id) {
              state.selectedNodeId = scoreData.next_node_id;
              await loadStudyNode(scoreData.next_node_id);
            } else {
              showToast('Congratulations! Curriculum Complete.', 'success');
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

function updateHeader(title, tier, phase) {
  const nodeTitle = document.getElementById('header-node-title');
  const tierBadge = document.getElementById('header-tier-badge');
  const phaseBadge = document.getElementById('header-phase-badge');

  if (nodeTitle) nodeTitle.textContent = title;
  if (tierBadge) tierBadge.textContent = `Tier ${tier}`;
  if (phaseBadge) phaseBadge.textContent = phase;
}

// Boot application
window.addEventListener('DOMContentLoaded', init);
