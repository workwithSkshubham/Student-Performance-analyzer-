/**
 * Main Application Orchestrator & State Manager
 * Handles SPA navigation, modal controllers, and notification toasts.
 */

const App = {
  currentPage: 'dashboard',

  // API helper with JSON parsing and error handling
  async fetchAPI(endpoint, options = {}) {
    try {
      const response = await fetch(endpoint, {
        headers: {
          'Content-Type': 'application/json',
          ...(options.headers || {})
        },
        ...options
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || `HTTP ${response.status}: Request failed`);
      }
      return data;
    } catch (err) {
      console.error(`API Error [${endpoint}]:`, err);
      throw err;
    }
  },

  // Notification Toast System
  showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icon = type === 'success' ? '✓' : '⚠';
    toast.innerHTML = `
      <span class="toast-icon" style="font-weight: 700; font-family: monospace;">${icon}</span>
      <span class="toast-message">${message}</span>
    `;

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 250);
    }, 3800);
  },

  // Single Page Application Navigation
  navigateTo(pageId) {
    this.currentPage = pageId;

    // Update sidebar navigation links
    document.querySelectorAll('.nav-item').forEach(item => {
      if (item.getAttribute('data-page') === pageId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Update visible views
    document.querySelectorAll('.page-view').forEach(view => {
      view.classList.remove('active');
    });

    const targetView = document.getElementById(`view-${pageId}`);
    if (targetView) {
      targetView.classList.add('active');
    }

    // Update header titles
    const titles = {
      'dashboard': { title: 'Dashboard', breadcrumb: 'workspace / overview' },
      'class-summary': { title: 'Class Analytics', breadcrumb: 'analytics / aggregate summary' },
      'analysis': { title: 'Performance Analysis', breadcrumb: 'analytics / student diagnostic' },
      'students': { title: 'Students Roster', breadcrumb: 'management / student directory' },
      'csv-workspace': { title: 'CSV Workspace', breadcrumb: 'database / students.csv editor' },
      'terminal': { title: 'Python Terminal', breadcrumb: 'developer / isolated execution' },
      'reports': { title: 'Reports Archive', breadcrumb: 'documents / generated text reports' }
    };

    const header = titles[pageId] || { title: pageId, breadcrumb: 'workspace' };
    document.getElementById('pageHeaderTitle').textContent = header.title;
    document.getElementById('pageHeaderBreadcrumb').textContent = header.breadcrumb;

    // Close mobile navigation drawer if open
    document.getElementById('appSidebar')?.classList.remove('open');
    document.getElementById('sidebarBackdrop')?.classList.remove('active');

    // Trigger page-specific data refresh
    if (pageId === 'dashboard') Dashboard.load();
    else if (pageId === 'students') Students.load();
    else if (pageId === 'analysis') Analysis.init();
    else if (pageId === 'class-summary') ClassSummary.load();
    else if (pageId === 'csv-workspace') CsvEditor.load();
    else if (pageId === 'reports') Reports.load();
  },

  init() {
    // Setup Navigation Listeners
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const page = item.getAttribute('data-page');
        if (page) this.navigateTo(page);
      });
    });

    // Mobile nav toggle
    const mobileToggle = document.getElementById('mobileNavToggle');
    const sidebar = document.getElementById('appSidebar');
    const backdrop = document.getElementById('sidebarBackdrop');

    if (mobileToggle && sidebar && backdrop) {
      mobileToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        backdrop.classList.toggle('active');
      });
      backdrop.addEventListener('click', () => {
        sidebar.classList.remove('open');
        backdrop.classList.remove('active');
      });
    }

    // Header Quick Add Student
    document.getElementById('btnQuickAddStudent')?.addEventListener('click', () => {
      this.navigateTo('students');
      setTimeout(() => Students.openAddModal(), 100);
    });

    // Initialize Dashboard as default view
    this.navigateTo('dashboard');
  }
};

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
