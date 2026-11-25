/**
 * Reports Archive & Document Viewer Controller
 * Interacts with /api/reports and reads saved files from reports/
 */

const Reports = {
  activeFilename: null,

  async load() {
    try {
      const res = await App.fetchAPI('/api/reports');
      if (res.success) {
        this.renderTable(res.reports || []);
      }
    } catch (err) {
      App.showToast('Failed to load reports archive: ' + err.message, 'error');
    }
  },

  renderTable(reports) {
    const tbody = document.getElementById('reportsTableTbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (reports.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; color: var(--text-dim); padding: 24px;">
            No generated reports in <code>reports/</code> yet.
          </td>
        </tr>
      `;
      return;
    }

    reports.forEach((rep, idx) => {
      const tr = document.createElement('tr');
      const badgeClass = rep.type === 'Class Summary' ? 'badge-good' : 'badge-average';
      const sizeKb = (rep.size_bytes / 1024).toFixed(1);

      tr.innerHTML = `
        <td class="mono-cell"><strong>${rep.filename}</strong></td>
        <td><span class="badge ${badgeClass}">${rep.type}</span></td>
        <td class="mono-cell">${rep.created_at}</td>
        <td class="mono-cell">${sizeKb} KB</td>
        <td>
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-secondary btn-sm" onclick="Reports.viewReport('${rep.filename}')">Inspect</button>
            <a href="/api/reports/${rep.filename}?download=1" class="btn btn-icon" title="Download">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            </a>
          </div>
        </td>
      `;
      tbody.appendChild(tr);

      // Auto-preview first report if none active
      if (idx === 0 && !this.activeFilename) {
        this.viewReport(rep.filename);
      }
    });
  },

  async viewReport(filename) {
    this.activeFilename = filename;
    try {
      const res = await App.fetchAPI(`/api/reports/${filename}`);
      if (res.success) {
        document.getElementById('reportViewerTitle').textContent = `Document: ${filename}`;
        document.getElementById('reportViewerContentBox').textContent = res.content;
        
        const dlBtn = document.getElementById('btnDownloadCurrentReport');
        if (dlBtn) {
          dlBtn.style.display = 'inline-flex';
          dlBtn.onclick = () => {
            window.location.href = `/api/reports/${filename}?download=1`;
          };
        }
      }
    } catch (err) {
      App.showToast('Failed to view report: ' + err.message, 'error');
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnRefreshReports')?.addEventListener('click', () => Reports.load());
});
