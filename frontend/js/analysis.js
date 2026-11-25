/**
 * Student Diagnostic Performance Analysis Controller
 * Connects to original Python analytics: calculate_metrics, analyze_student, build_report.
 */

const Analysis = {
  currentStudentRoll: null,
  currentReportText: '',

  async init() {
    try {
      const res = await App.fetchAPI('/api/students');
      if (res.success) {
        const select = document.getElementById('analysisStudentSelect');
        if (!select) return;
        select.innerHTML = '';

        if (res.students.length === 0) {
          select.innerHTML = '<option value="">No students available</option>';
          return;
        }

        res.students.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s.roll_no;
          opt.textContent = `Roll #${s.roll_no} — ${s.name} (${s.class})`;
          select.appendChild(opt);
        });

        // If currently selected or first
        const targetRoll = this.currentStudentRoll || res.students[0].roll_no;
        select.value = targetRoll;
        this.runAnalysis(targetRoll);
      }
    } catch (err) {
      App.showToast('Failed to initialize analysis selector: ' + err.message, 'error');
    }
  },

  async loadStudent(rollNo) {
    this.currentStudentRoll = rollNo;
    App.navigateTo('analysis');
    setTimeout(() => {
      const select = document.getElementById('analysisStudentSelect');
      if (select) select.value = rollNo;
      this.runAnalysis(rollNo);
    }, 150);
  },

  async runAnalysis(rollNo) {
    if (!rollNo) {
      rollNo = document.getElementById('analysisStudentSelect')?.value;
    }
    if (!rollNo) return;

    try {
      const res = await App.fetchAPI(`/api/students/${rollNo}/analysis`);
      if (res.success) {
        this.currentStudentRoll = rollNo;
        this.currentReportText = res.report_text;
        this.renderAnalysis(res);
      }
    } catch (err) {
      App.showToast('Failed to run student analysis: ' + err.message, 'error');
    }
  },

  renderAnalysis(data) {
    const s = data.student;
    const m = data.metrics;
    const a = data.analysis;

    document.getElementById('analysisResultContainer').style.display = 'block';

    // Profile card
    document.getElementById('anaStudentName').textContent = s.name;
    document.getElementById('anaRollAndClass').textContent = `Roll #${s.roll_no} · Class: ${s.class}`;
    document.getElementById('anaPercentage').textContent = m.percentage.toFixed(2);
    document.getElementById('anaGradeMeta').textContent = `Grade: ${m.grade} · Level: ${a.level}`;

    // Attendance
    document.getElementById('anaAttendance').textContent = s.attendance.toFixed(2);
    const attWarningEl = document.getElementById('anaAttendanceWarning');
    if (s.attendance < 75) {
      attWarningEl.textContent = 'Warning: Attendance below 75% threshold';
      attWarningEl.style.color = '#FF7B7B';
    } else {
      attWarningEl.textContent = 'Regular attendance maintained';
      attWarningEl.style.color = 'var(--accent-green)';
    }

    // Trajectory
    const gap = (s.target - m.percentage).toFixed(2);
    document.getElementById('anaTargetGap').textContent = `${a.target_result}`;
    document.getElementById('anaPreviousComparison').textContent = `Prev: ${s.previous}% · Trajectory: ${a.previous_result}`;

    // Subject breakdown bars
    document.getElementById('anaTotalMarksMeta').textContent = `Total: ${m.total} / ${m.max_total} (Average: ${m.average.toFixed(2)})`;
    const scoreBars = document.getElementById('anaSubjectScoreBars');
    scoreBars.innerHTML = '';

    for (const [sub, score] of Object.entries(s.marks)) {
      const item = document.createElement('div');
      item.className = 'distribution-item';
      const isWeak = score < 40;
      const barColor = isWeak ? '#FF7B7B' : 'var(--accent-green)';
      const statusLabel = isWeak ? '<span style="color: #FF7B7B; font-weight: 600;"> (Failing < 40)</span>' : '';

      item.innerHTML = `
        <div class="distribution-label-row">
          <span class="distribution-label">${sub}${statusLabel}</span>
          <span class="distribution-val">${score} / 100</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill" style="width: ${score}%; background: ${barColor};"></div>
        </div>
      `;
      scoreBars.appendChild(item);
    }

    // Benchmarks
    document.getElementById('anaBestSubject').textContent = `${a.best_subject} (${s.marks[a.best_subject]})`;
    document.getElementById('anaWeakestSubject').textContent = `${a.weakest_subject} (${s.marks[a.weakest_subject]})`;
    
    const failingEl = document.getElementById('anaFailingSubjects');
    if (a.weak_subjects && a.weak_subjects.length > 0) {
      failingEl.textContent = a.weak_subjects.join(', ');
      failingEl.style.color = '#FF7B7B';
    } else {
      failingEl.textContent = 'None (All >= 40)';
      failingEl.style.color = 'var(--accent-green)';
    }

    document.getElementById('anaTargetGoal').textContent = `${s.target}%`;
    document.getElementById('anaPrevGoal').textContent = `${s.previous}%`;

    // Observations
    const obsList = document.getElementById('anaObservationsList');
    obsList.innerHTML = '';
    a.reasons.forEach(r => {
      const li = document.createElement('li');
      li.style.display = 'flex';
      li.style.gap = '8px';
      li.innerHTML = `<span style="color: var(--accent-green); font-weight: 700;">•</span> <span>${r}</span>`;
      obsList.appendChild(li);
    });

    // Suggestions
    const sugList = document.getElementById('anaSuggestionsList');
    sugList.innerHTML = '';
    a.suggestions.forEach(sug => {
      const li = document.createElement('li');
      li.style.display = 'flex';
      li.style.gap = '8px';
      li.innerHTML = `<span style="color: var(--accent-green); font-weight: 700;">✓</span> <span>${sug}</span>`;
      sugList.appendChild(li);
    });

    // ASCII Text Report
    document.getElementById('anaAsciiReportBox').textContent = data.report_text;
  },

  async exportReport() {
    if (!this.currentStudentRoll) return;
    try {
      const res = await App.fetchAPI('/api/reports/student', {
        method: 'POST',
        body: JSON.stringify({ roll_no: this.currentStudentRoll })
      });
      App.showToast(res.message || 'Report generated and saved!');
    } catch (err) {
      App.showToast('Failed to export report: ' + err.message, 'error');
    }
  },

  copyReport() {
    if (!this.currentReportText) return;
    navigator.clipboard.writeText(this.currentReportText).then(() => {
      App.showToast('Report text copied to clipboard!');
    }).catch(() => {
      App.showToast('Failed to copy to clipboard', 'error');
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnRunStudentAnalysis')?.addEventListener('click', () => {
    const roll = document.getElementById('analysisStudentSelect')?.value;
    Analysis.runAnalysis(roll);
  });

  document.getElementById('analysisStudentSelect')?.addEventListener('change', (e) => {
    Analysis.runAnalysis(e.target.value);
  });

  document.getElementById('btnExportAnalysisReport')?.addEventListener('click', () => Analysis.exportReport());
  document.getElementById('btnCopyAnalysisReport')?.addEventListener('click', () => Analysis.copyReport());
});
