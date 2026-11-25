/**
 * Class Performance Summary Controller
 * Connects to class_summary and build_class_report.
 */

const ClassSummary = {
  currentReportText: '',

  async load() {
    try {
      const res = await App.fetchAPI('/api/class-summary');
      if (res.success && res.data) {
        this.renderSummary(res.data);
      }
    } catch (err) {
      App.showToast('Failed to load class analytics: ' + err.message, 'error');
    }
  },

  renderSummary(data) {
    const s = data.summary;
    this.currentReportText = data.report_text;

    document.getElementById('clsTotalStudents').textContent = s.students;
    document.getElementById('clsAverage').textContent = s.average.toFixed(2);
    document.getElementById('clsMedianMeta').textContent = `Median: ${s.median.toFixed(2)}%`;
    document.getElementById('clsHighest').textContent = s.highest.toFixed(2);
    document.getElementById('clsLowestMeta').textContent = `Lowest Score: ${s.lowest.toFixed(2)}%`;
    document.getElementById('clsTopper').textContent = s.topper || 'N/A';

    // Render Subject-wise Analytics
    const tbody = document.getElementById('clsSubjectStatsTbody');
    if (tbody) {
      tbody.innerHTML = '';
      for (const [sub, stats] of Object.entries(data.subject_stats || {})) {
        const tr = document.createElement('tr');
        const failColor = stats.failing_count > 0 ? 'style="color: #FF7B7B; font-weight: 600;"' : 'style="color: var(--accent-green);"';
        tr.innerHTML = `
          <td style="font-weight: 500;">${sub}</td>
          <td class="mono-cell">${stats.average.toFixed(2)} / 100</td>
          <td class="mono-cell" style="color: var(--accent-green);">${stats.highest}</td>
          <td class="mono-cell">${stats.lowest}</td>
          <td class="mono-cell" ${failColor}>${stats.failing_count} student(s)</td>
        `;
        tbody.appendChild(tr);
      }
    }

    // Render Letter Grade Distribution Bars
    const gradeContainer = document.getElementById('clsGradeDistributionBars');
    if (gradeContainer) {
      gradeContainer.innerHTML = '';
      const totalStudents = s.students || 1;
      const grades = data.grade_distribution || {};

      for (const [grade, count] of Object.entries(grades)) {
        const pct = Math.round((count / totalStudents) * 100);
        const item = document.createElement('div');
        item.className = 'distribution-item';
        item.innerHTML = `
          <div class="distribution-label-row">
            <span class="distribution-label">Grade ${grade}</span>
            <span class="distribution-val">${count} (${pct}%)</span>
          </div>
          <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: ${pct}%;"></div>
          </div>
        `;
        gradeContainer.appendChild(item);
      }
    }

    // Preview raw text report
    document.getElementById('clsReportPreviewBox').textContent = data.report_text;
  },

  async generateClassReport() {
    try {
      const res = await App.fetchAPI('/api/reports/class', { method: 'POST' });
      App.showToast(res.message || 'Class report saved to reports/');
    } catch (err) {
      App.showToast('Failed to save class report: ' + err.message, 'error');
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnSaveClassReport')?.addEventListener('click', () => ClassSummary.generateClassReport());
});
