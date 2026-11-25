/**
 * CSV Spreadsheet Workspace Controller
 * Direct spreadsheet table for data/students.csv with cell editing, row deletion, and atomic backups.
 */

const CsvEditor = {
  columns: [],
  records: [],
  filteredRecords: [],

  async load() {
    try {
      const res = await App.fetchAPI('/api/csv');
      if (res.success) {
        this.columns = res.columns;
        this.records = res.records;
        this.filteredRecords = [...this.records];
        
        const fInfo = res.file_info;
        if (fInfo) {
          document.getElementById('csvFileInfo').textContent = 
            `File: ${fInfo.path} · Records: ${res.total_records} · Modified: ${fInfo.last_modified}`;
        }
        this.renderTable();
      }
    } catch (err) {
      App.showToast('Failed to load CSV records: ' + err.message, 'error');
    }
  },

  renderTable() {
    const thead = document.getElementById('csvTableThead');
    const tbody = document.getElementById('csvTableTbody');
    if (!thead || !tbody) return;

    // Headers
    thead.innerHTML = `
      <tr>
        <th style="width: 50px;">#</th>
        ${this.columns.map(col => `<th>${col.toUpperCase()}</th>`).join('')}
        <th style="width: 80px; text-align: center;">ACTION</th>
      </tr>
    `;

    // Filtered Rows
    tbody.innerHTML = '';
    if (this.filteredRecords.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="${this.columns.length + 2}" style="text-align: center; color: var(--text-dim); padding: 28px;">
            No CSV records found. Click "+ Add Row" or "+ Add Student" to insert a record.
          </td>
        </tr>
      `;
      return;
    }

    this.filteredRecords.forEach((row, rowIdx) => {
      const tr = document.createElement('tr');
      const isNew = row.__is_new === true;
      if (isNew) {
        tr.style.background = 'rgba(183, 247, 197, 0.08)';
      }

      let cellsHtml = `<td class="mono-cell" style="color: var(--text-dim);">${rowIdx + 1}</td>`;

      this.columns.forEach(col => {
        const val = row[col] !== undefined ? row[col] : '';
        const isNumeric = col !== 'name' && col !== 'class_name';
        cellsHtml += `
          <td style="padding: 4px 6px;">
            <input 
              type="${isNumeric ? 'number' : 'text'}" 
              ${isNumeric ? 'step="any"' : ''}
              class="form-input mono-cell" 
              style="padding: 5px 8px; font-size: 12px; height: 30px; background: rgba(9, 13, 11, 0.4);"
              data-col="${col}" 
              data-roll="${row.roll_no}"
              data-row="${rowIdx}"
              value="${val}">
          </td>
        `;
      });

      cellsHtml += `
        <td style="padding: 4px 6px; text-align: center;">
          <button class="btn btn-icon" style="color: #FF7B7B;" onclick="CsvEditor.deleteRow(${rowIdx})" title="Delete row from CSV">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
          </button>
        </td>
      `;

      tr.innerHTML = cellsHtml;
      tbody.appendChild(tr);
    });

    // Attach change handlers to update records in memory immediately
    tbody.querySelectorAll('input').forEach(input => {
      input.addEventListener('change', (e) => {
        const rollNo = parseInt(e.target.dataset.roll, 10);
        const col = e.target.dataset.col;
        const val = e.target.value.trim();

        // Update in filteredRecords
        const rowIdx = parseInt(e.target.dataset.row, 10);
        if (this.filteredRecords[rowIdx]) {
          this.filteredRecords[rowIdx][col] = val;
        }

        // Also update in master records list
        const masterRow = this.records.find(r => r.roll_no == rollNo);
        if (masterRow) {
          masterRow[col] = val;
        }
      });
    });
  },

  addRow() {
    const existingRolls = this.records.map(r => parseInt(r.roll_no || 0, 10)).filter(n => !isNaN(n));
    const newRoll = existingRolls.length > 0 ? Math.max(...existingRolls) + 1 : 101;

    const newRow = {
      roll_no: newRoll,
      name: 'New Student',
      class_name: 'Sem 3',
      maths: 75,
      physics: 75,
      chemistry: 75,
      english: 75,
      cs: 75,
      attendance: 80.0,
      target: 80.0,
      previous: 70.0,
      __is_new: true
    };

    this.records.push(newRow);
    this.filteredRecords.push(newRow);
    this.renderTable();
    App.showToast(`Row #${newRoll} added. Edit cells and click "Save Changes" to commit.`, 'success');
  },

  async deleteRow(idx) {
    const target = this.filteredRecords[idx];
    if (!target) return;

    const rollNo = target.roll_no;
    const name = target.name || 'Student';

    // If it's an unsaved newly added row, just remove it from client state
    if (target.__is_new) {
      this.filteredRecords.splice(idx, 1);
      this.records = this.records.filter(r => r !== target);
      this.renderTable();
      App.showToast(`Unsaved row removed from editor.`);
      return;
    }

    if (!confirm(`Are you sure you want to permanently delete Roll #${rollNo} (${name}) from data/students.csv?`)) {
      return;
    }

    try {
      const res = await App.fetchAPI(`/api/csv/${rollNo}`, { method: 'DELETE' });
      App.showToast(res.message || `Roll #${rollNo} deleted from CSV file.`);
      
      // Reload CSV editor and sync other views
      await this.load();
      if (typeof Students !== 'undefined' && Students.load) Students.load();
      if (typeof Dashboard !== 'undefined' && Dashboard.load) Dashboard.load();
    } catch (err) {
      App.showToast('Failed to delete CSV record: ' + err.message, 'error');
    }
  },

  filter(query) {
    query = query.toLowerCase().trim();
    if (!query) {
      this.filteredRecords = [...this.records];
    } else {
      this.filteredRecords = this.records.filter(row => {
        return Object.values(row).some(v => String(v).toLowerCase().includes(query));
      });
    }
    this.renderTable();
  },

  async save() {
    // Read current input values from visible DOM into memory
    const tbody = document.getElementById('csvTableTbody');
    if (tbody) {
      tbody.querySelectorAll('input').forEach(inp => {
        const rollNo = inp.dataset.roll;
        const col = inp.dataset.col;
        const val = inp.value.trim();
        const row = this.records.find(r => String(r.roll_no) === String(rollNo));
        if (row) {
          row[col] = val;
        }
      });
    }

    // Clean records to save (strip temporary flags)
    const recordsToSave = this.records.map(r => {
      const clean = { ...r };
      delete clean.__is_new;
      return clean;
    });

    try {
      const res = await App.fetchAPI('/api/csv', {
        method: 'PUT',
        body: JSON.stringify({ records: recordsToSave })
      });
      App.showToast(res.message || 'CSV saved successfully with backup created!');
      await this.load();
      if (typeof Students !== 'undefined' && Students.load) Students.load();
      if (typeof Dashboard !== 'undefined' && Dashboard.load) Dashboard.load();
    } catch (err) {
      App.showToast('Validation / Save Error: ' + err.message, 'error');
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnCsvRefresh')?.addEventListener('click', () => CsvEditor.load());
  document.getElementById('btnCsvAddRow')?.addEventListener('click', () => CsvEditor.addRow());
  document.getElementById('btnCsvSave')?.addEventListener('click', () => CsvEditor.save());
  document.getElementById('csvFilterInput')?.addEventListener('input', (e) => CsvEditor.filter(e.target.value));
});
