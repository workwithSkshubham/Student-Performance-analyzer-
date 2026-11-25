/**
 * Dashboard Workspace Logic
 * Updates summary metrics, performance tiers, and recent student records.
 */

const Dashboard = {
  async load() {
    try {
      const res = await App.fetchAPI('/api/dashboard');
      if (res.success && res.data) {
        this.renderMetrics(res.data);
        this.renderRecentStudents(res.data.recent_students || []);
        this.renderPerformanceTiers(res.data.performance_breakdown || {});
      }
    } catch (err) {
      App.showToast('Failed to load dashboard metrics: ' + err.message, 'error');
    }
  },

  renderMetrics(data) {
    document.getElementById('dashTotalStudents').textContent = data.total_students;
    document.getElementById('dashClassAverage').textContent = data.class_average.toFixed(2);
    document.getElementById('dashMedianMeta').textContent = `Class Median: ${data.class_median.toFixed(2)}%`;
    document.getElementById('dashHighest').textContent = data.highest_percentage.toFixed(2);
    document.getElementById('dashTopperMeta').textContent = `Topper: ${data.topper || 'N/A'}`;
    document.getElementById('dashAvgAttendance').textContent = data.average_attendance.toFixed(2);
  },

  renderRecentStudents(students) {
    const tbody = document.getElementById('dashRecentStudentsTbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (students.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" style="text-align: center; color: var(--text-dim); padding: 24px;">
            No student records found in storage. Click "Add Student" to begin.
          </td>
        </tr>
      `;
      return;
    }

    students.forEach(s => {
      const tr = document.createElement('tr');
      const badgeClass = s.level === 'Good' ? 'badge-good' : (s.level === 'Average' ? 'badge-average' : 'badge-danger');
      const prevClass = s.previous_result === 'Improved' ? 'style="color: var(--accent-green);"' : (s.previous_result === 'Declined' ? 'style="color: #FF7B7B;"' : '');

      tr.innerHTML = `
        <td class="mono-cell">${s.roll_no}</td>
        <td style="font-weight: 500;">${s.name}</td>
        <td>${s.class}</td>
        <td class="mono-cell">${s.attendance}%</td>
        <td class="mono-cell">${s.percentage.toFixed(2)}%</td>
        <td><span class="badge ${badgeClass}">${s.grade}</span></td>
        <td class="mono-cell" ${prevClass}>${s.previous_result}</td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="Analysis.loadStudent(${s.roll_no})">Analyze</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  },

  renderPerformanceTiers(tiers) {
    const container = document.getElementById('dashPerformanceTiers');
    if (!container) return;
    container.innerHTML = '';

    const total = Object.values(tiers).reduce((a, b) => a + b, 0) || 1;
    const categories = [
      { label: 'Good (>= 75%)', count: tiers['Good'] || 0, color: 'var(--accent-green)' },
      { label: 'Average (50% - 74%)', count: tiers['Average'] || 0, color: 'var(--text-muted)' },
      { label: 'Needs Improvement (< 50%)', count: tiers['Needs Improvement'] || 0, color: '#FF7B7B' }
    ];

    categories.forEach(cat => {
      const pct = Math.round((cat.count / total) * 100);
      const item = document.createElement('div');
      item.className = 'distribution-item';
      item.innerHTML = `
        <div class="distribution-label-row">
          <span class="distribution-label">${cat.label}</span>
          <span class="distribution-val">${cat.count} (${pct}%)</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill" style="width: ${pct}%; background: ${cat.color};"></div>
        </div>
      `;
      container.appendChild(item);
    });
  }
};

document.getElementById('btnRefreshDashboard')?.addEventListener('click', () => {
  Dashboard.load();
  App.showToast('Dashboard metrics refreshed');
});
