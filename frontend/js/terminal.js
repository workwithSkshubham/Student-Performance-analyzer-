/**
 * VS Code-style Python Terminal & Code Execution Controller
 * Runs Python code inside an isolated subprocess with AST safety checks.
 */

const Terminal = {
  snippets: {
    basic_calc: `# Calculate total, percentage and letter grade
marks = [90, 85, 78, 92, 88]
total = sum(marks)
max_total = 500
percentage = round((total / max_total) * 100, 2)

def get_grade(pct):
    if pct >= 90: return "A+"
    elif pct >= 80: return "A"
    elif pct >= 70: return "B"
    elif pct >= 60: return "C"
    elif pct >= 40: return "D"
    else: return "F"

print("====================================")
print(f"Total Marks : {total} / {max_total}")
print(f"Percentage  : {percentage}%")
print(f"Letter Grade: {get_grade(percentage)}")
print("====================================")`,

    failing_filter: `# Identify failing marks below passing threshold of 40
student_scores = {
    "Maths": 78,
    "Physics": 34,
    "Chemistry": 65,
    "English": 28,
    "CS": 88
}

failing = {sub: score for sub, score in student_scores.items() if score < 40}

print("Subject Performance Evaluation:")
for sub, score in student_scores.items():
    status = "FAIL" if score < 40 else "PASS"
    print(f"  {sub:<10}: {score:>2}/100 [{status}]")

print("-" * 36)
if failing:
    print(f"Warning: {len(failing)} failing subject(s) detected: {list(failing.keys())}")
else:
    print("All subjects cleared successfully!")`,

    attendance_check: `# Attendance warning threshold verification (< 75%)
attendance_record = {
    "Rahul": 92.0,
    "Amit": 68.0,
    "Sneha": 96.0,
    "Karan": 72.0
}

THRESHOLD = 75.0

print("Attendance Eligibility Check:")
for student, att in attendance_record.items():
    if att < THRESHOLD:
        print(f"  [DEBARRED] {student:<8}: {att}% (Below {THRESHOLD}% threshold)")
    else:
        print(f"  [ELIGIBLE] {student:<8}: {att}%")`,

    numpy_stats: `# NumPy vectorized metrics computation
marks = np.array([90, 55, 75, 80, 85])
total = int(np.sum(marks))
mean = float(np.mean(marks))
std_dev = float(np.std(marks))

print("NumPy Vectorized Analytics:")
print(f"Total Sum : {total}")
print(f"Mean Score: {mean:.2f}")
print(f"Std Dev   : {std_dev:.2f}")`
  },

  async runCode() {
    const editor = document.getElementById('pythonEditorTextarea');
    const outputBox = document.getElementById('terminalOutputBox');
    const timeBadge = document.getElementById('termExecutionTimeBadge');
    if (!editor || !outputBox) return;

    const code = editor.value.trim();
    if (!code) {
      App.showToast('Please enter Python code to execute.', 'error');
      return;
    }

    outputBox.innerHTML = '<span style="color: var(--text-dim);">Executing code in sandboxed subprocess...</span>';

    try {
      const res = await App.fetchAPI('/api/terminal/run', {
        method: 'POST',
        body: JSON.stringify({ code: code })
      });

      timeBadge.textContent = `${res.execution_time_ms} ms`;

      if (res.success) {
        timeBadge.className = 'badge badge-good';
        outputBox.innerHTML = '';
        const out = document.createElement('span');
        out.style.color = '#B7F7C5';
        out.textContent = res.stdout || '(Program completed with no standard output)';
        outputBox.appendChild(out);
      } else {
        timeBadge.className = 'badge badge-danger';
        outputBox.innerHTML = '';
        if (res.stdout) {
          const out = document.createElement('span');
          out.style.color = '#B7F7C5';
          out.textContent = res.stdout + '\n';
          outputBox.appendChild(out);
        }
        const err = document.createElement('span');
        err.style.color = '#FF7B7B';
        err.textContent = res.stderr;
        outputBox.appendChild(err);
      }
    } catch (err) {
      timeBadge.className = 'badge badge-danger';
      outputBox.innerHTML = `<span style="color: #FF7B7B;">Terminal Execution Error:\n${err.message}</span>`;
    }
  },

  clear() {
    const outputBox = document.getElementById('terminalOutputBox');
    if (outputBox) {
      outputBox.innerHTML = '<span style="color: var(--text-dim);"># Console cleared. Ready for execution.</span>';
    }
    document.getElementById('termExecutionTimeBadge').textContent = '0.0 ms';
    document.getElementById('termExecutionTimeBadge').className = 'badge badge-good';
  },

  loadSnippet(key) {
    if (this.snippets[key]) {
      document.getElementById('pythonEditorTextarea').value = this.snippets[key];
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnRunPythonCode')?.addEventListener('click', () => Terminal.runCode());
  document.getElementById('btnClearTerminal')?.addEventListener('click', () => Terminal.clear());

  document.getElementById('terminalSnippetSelect')?.addEventListener('change', (e) => {
    if (e.target.value) {
      Terminal.loadSnippet(e.target.value);
    }
  });

  // Shortcut: Ctrl + Enter or Cmd + Enter to Run
  document.getElementById('pythonEditorTextarea')?.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      Terminal.runCode();
    }
  });
});
