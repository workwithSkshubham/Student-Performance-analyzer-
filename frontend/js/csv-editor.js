/**
 * CSV Spreadsheet Workspace Controller
 * Direct spreadsheet table for data/students.csv with cell editing and atomic backups.
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
        <th style="width: 60px;">ACTION</th>
      </tr>
    `;

    // Filtered Rows
    tbody.innerHTML = '';
    if (this.filteredRecords.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="${this.columns.length + 2}" style="text-align: center; color: var(--text-dim); padding: 24px;">
            No CSV rows found. Click "+ Add Row" to insert a record.
          </td>
        </tr>
      `;
      return;
    }

    this.filteredRecords.forEach((row, rowIdx) => {
      const tr = document.createElement('tr');
      tr.dataset.index = rowIdx;

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
              data-row="${rowIdx}"
              value="${val}">
          </td>
        `;
      });

      cellsHtml += `
        <td style="padding: 4px 6px; text-align: center;">
          <button class="btn btn-icon" style="color: #FF7B7B;" onclick="CsvEditor.deleteRow(${rowIdx})" title="Delete Row">
            &times;
          </button>
        </td>
      `;

      tr.innerHTML = cellsHtml;
      tbody.appendChild(tr);
    });

    // Attach change handlers to capture cell edits
    tbody.querySelectorAll('input').forEach(input => {
      input.addEventListener('change', (e) => {
        const rowIdx = parseInt(e.target.dataset.row, 10);
        const col = e.target.dataset.col;
        const val = e.target.value.trim();
        this.filteredRecords[rowIdx][col] = val;
      });
    });
  },

  addRow() {
    const newRoll = this.filteredRecords.length > 0 
      ? Math.max(...this.filteredRecords.map(r => parseInt(r.roll_no || 0, 10))) + 1 
      : 101;

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
      previous: 70.0
    };

    this.filteredRecords.push(newRow);
    this.records.push(newRow);
    this.renderTable();
    App.showToast(`New row with Roll #${newRoll} added to editor.`);
  },

  deleteRow(idx) {
    this.filteredRecords.splice(idx, 1);
    this.records = [...this.filteredRecords];
    this.renderTable();
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
    // Read current state from DOM inputs to avoid missed blurs
    const tbody = document.getElementById('csvTableTbody');
    const inputs = tbody.querySelectorAll('input');
    const rowsMap = {};

    inputs.forEach(inp => {
      const rowIdx = parseInt(inp.dataset.row, 10);
      const col = inp.dataset.col;
      if (!rowsMap[rowIdx]) rowsMap[rowIdx] = {};
      rowsMap[rowIdx][col] = inp.value.trim();
    });

    const recordsToSave = Object.values(rowsMap);

    try {
      const res = await App.fetchAPI('/api/csv', {
        method: 'PUT',
        body: JSON.stringify({ records: recordsToSave })
      });
      App.showToast(res.message || 'CSV saved successfully with backup created!');
      this.load();
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
