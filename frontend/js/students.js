/**
 * Student Management & Roster Controller
 * Handles student listing, client-side filtering, modal CRUD, and validation.
 */

const Students = {
  studentsList: [],
  deleteTargetRoll: null,

  async load() {
    try {
      const search = document.getElementById('studentSearchInput')?.value.trim() || '';
      const sortVal = document.getElementById('studentSortSelect')?.value || 'roll_no-asc';
      const [sortBy, order] = sortVal.split('-');

      const res = await App.fetchAPI(`/api/students?search=${encodeURIComponent(search)}&sort=${sortBy}&order=${order}`);
      if (res.success) {
        this.studentsList = res.students;
        this.renderTable(this.studentsList);
      }
    } catch (err) {
      App.showToast('Failed to load students: ' + err.message, 'error');
    }
  },

  renderTable(students) {
    const tbody = document.getElementById('studentsTableTbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (students.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="14" style="text-align: center; color: var(--text-dim); padding: 32px;">
            No matching student records found.
          </td>
        </tr>
      `;
      return;
    }

    students.forEach(s => {
      const m = s.metrics;
      const a = s.analysis;
      const tr = document.createElement('tr');
      const badgeClass = a.level === 'Good' ? 'badge-good' : (a.level === 'Average' ? 'badge-average' : 'badge-danger');
      const attWarning = s.attendance < 75 ? 'style="color: #FF7B7B; font-weight: 600;"' : '';

      tr.innerHTML = `
        <td class="mono-cell"><strong>${s.roll_no}</strong></td>
        <td style="font-weight: 500;">${s.name}</td>
        <td>${s.class}</td>
        <td class="mono-cell">${s.marks.Maths}</td>
        <td class="mono-cell">${s.marks.Physics}</td>
        <td class="mono-cell">${s.marks.Chemistry}</td>
        <td class="mono-cell">${s.marks.English}</td>
        <td class="mono-cell">${s.marks.CS}</td>
        <td class="mono-cell">${m.total}/500</td>
        <td class="mono-cell"><strong>${m.percentage.toFixed(2)}%</strong></td>
        <td><span class="badge ${badgeClass}">${m.grade}</span></td>
        <td class="mono-cell" ${attWarning}>${s.attendance}%</td>
        <td class="mono-cell">${s.target}%</td>
        <td>
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-secondary btn-sm" onclick="Analysis.loadStudent(${s.roll_no})" title="Run Deep Analysis">Analyze</button>
            <button class="btn btn-icon" onclick="Students.openEditModal(${s.roll_no})" title="Edit Student">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
            </button>
            <button class="btn btn-icon" style="color: #FF7B7B;" onclick="Students.openDeleteModal(${s.roll_no}, '${s.name.replace(/'/g, "\\'")}')" title="Delete Student">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
            </button>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    });
  },

  openAddModal() {
    document.getElementById('studentModalTitle').textContent = 'Add New Student Record';
    document.getElementById('studentFormIsEdit').value = '0';
    document.getElementById('studentRecordForm').reset();
    document.getElementById('inpStudentRoll').disabled = false;
    document.getElementById('studentFormModal').classList.add('active');
  },

  openEditModal(rollNo) {
    const s = this.studentsList.find(item => item.roll_no === rollNo);
    if (!s) return;

    document.getElementById('studentModalTitle').textContent = `Edit Student #${s.roll_no} (${s.name})`;
    document.getElementById('studentFormIsEdit').value = '1';
    document.getElementById('inpStudentRoll').value = s.roll_no;
    document.getElementById('inpStudentRoll').disabled = true;
    document.getElementById('inpStudentName').value = s.name;
    document.getElementById('inpStudentClass').value = s.class;
    document.getElementById('inpMarkMaths').value = s.marks.Maths;
    document.getElementById('inpMarkPhysics').value = s.marks.Physics;
    document.getElementById('inpMarkChemistry').value = s.marks.Chemistry;
    document.getElementById('inpMarkEnglish').value = s.marks.English;
    document.getElementById('inpMarkCS').value = s.marks.CS;
    document.getElementById('inpAttendance').value = s.attendance;
    document.getElementById('inpTarget').value = s.target;
    document.getElementById('inpPrevious').value = s.previous;

    document.getElementById('studentFormModal').classList.add('active');
  },

  closeModal() {
    document.getElementById('studentFormModal').classList.remove('active');
  },

  async handleFormSubmit() {
    const isEdit = document.getElementById('studentFormIsEdit').value === '1';
    const rollNo = parseInt(document.getElementById('inpStudentRoll').value, 10);
    const name = document.getElementById('inpStudentName').value.trim();
    const className = document.getElementById('inpStudentClass').value.trim();

    if (!rollNo || isNaN(rollNo) || rollNo < 1 || rollNo > 999999) {
      App.showToast('Please enter a valid Roll Number between 1 and 999999.', 'error');
      return;
    }
    if (!name) {
      App.showToast('Student Name cannot be empty.', 'error');
      return;
    }
    if (!className) {
      App.showToast('Class / Semester cannot be empty.', 'error');
      return;
    }

    const payload = {
      roll_no: rollNo,
      name: name,
      class: className,
      marks: {
        Maths: parseFloat(document.getElementById('inpMarkMaths').value || 0),
        Physics: parseFloat(document.getElementById('inpMarkPhysics').value || 0),
        Chemistry: parseFloat(document.getElementById('inpMarkChemistry').value || 0),
        English: parseFloat(document.getElementById('inpMarkEnglish').value || 0),
        CS: parseFloat(document.getElementById('inpMarkCS').value || 0)
      },
      attendance: parseFloat(document.getElementById('inpAttendance').value || 0),
      target: parseFloat(document.getElementById('inpTarget').value || 0),
      previous: parseFloat(document.getElementById('inpPrevious').value || 0)
    };

    try {
      if (isEdit) {
        const res = await App.fetchAPI(`/api/students/${rollNo}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        App.showToast(res.message || 'Student updated successfully.');
      } else {
        const res = await App.fetchAPI('/api/students', {
          method: 'POST',
          body: JSON.stringify(payload)
        });
        App.showToast(res.message || 'Student added successfully.');
      }
      this.closeModal();
      await this.load();
      if (typeof Dashboard !== 'undefined' && Dashboard.load) Dashboard.load();
      if (typeof CsvEditor !== 'undefined' && CsvEditor.load) CsvEditor.load();
    } catch (err) {
      App.showToast(err.message, 'error');
    }
  },

  openDeleteModal(rollNo, name) {
    this.deleteTargetRoll = rollNo;
    document.getElementById('deleteStudentName').textContent = name;
    document.getElementById('deleteStudentRoll').textContent = rollNo;
    document.getElementById('deleteConfirmModal').classList.add('active');
  },

  closeDeleteModal() {
    this.deleteTargetRoll = null;
    document.getElementById('deleteConfirmModal').classList.remove('active');
  },

  async confirmDelete() {
    if (!this.deleteTargetRoll) return;
    try {
      const res = await App.fetchAPI(`/api/students/${this.deleteTargetRoll}`, {
        method: 'DELETE'
      });
      App.showToast(res.message || 'Student record deleted.');
      this.closeDeleteModal();
      await this.load();
      if (typeof Dashboard !== 'undefined' && Dashboard.load) Dashboard.load();
      if (typeof CsvEditor !== 'undefined' && CsvEditor.load) CsvEditor.load();
    } catch (err) {
      App.showToast(err.message, 'error');
    }
  }
};

// Event Listeners for Students Workspace
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnOpenAddStudentModal')?.addEventListener('click', () => Students.openAddModal());
  document.getElementById('btnCloseStudentModal')?.addEventListener('click', () => Students.closeModal());
  document.getElementById('btnCancelStudentForm')?.addEventListener('click', () => Students.closeModal());
  document.getElementById('btnSaveStudentRecord')?.addEventListener('click', () => Students.handleFormSubmit());

  document.getElementById('btnCloseDeleteModal')?.addEventListener('click', () => Students.closeDeleteModal());
  document.getElementById('btnCancelDelete')?.addEventListener('click', () => Students.closeDeleteModal());
  document.getElementById('btnConfirmDelete')?.addEventListener('click', () => Students.confirmDelete());

  document.getElementById('btnRefreshStudents')?.addEventListener('click', () => Students.load());
  document.getElementById('studentSearchInput')?.addEventListener('input', () => Students.load());
  document.getElementById('studentSortSelect')?.addEventListener('change', () => Students.load());
});
