# Student Performance Analyzer — Comprehensive Project Implementation Document

## 1. Project Overview
The **Student Performance Analyzer (SPA)** is a data-driven academic analytics, diagnostic advisory, and performance management platform designed for higher education students and faculty. Originally developed as a terminal-based CLI tool, this release enhances the project into a professional, modern web application modeled after developer environments such as GitHub, Visual Studio Code, and Discord.

The core design philosophy of this transformation is **strict preservation of the original Python engine**: all mathematical calculations, grading metrics, statistical evaluations, and recommendations are directly executed by the existing Python modules without rewriting or duplicating business logic in client-side JavaScript.

---

## 2. Original Python Architecture
The terminal application is organized around clean, single-responsibility Python modules:

* `main.py`: Interactive CLI controller presenting an ASCII banner, credential authentication prompt (`python@2026`), and a 6-option numerical menu.
* `src/intro.py`: Startup welcome screen, mission statements, and terminal loading bar.
* `src/auth.py`: Password verification mechanism with a 3-attempt limit.
* `src/data_input.py`: User input validation enforcing strict range constraints (`0 <= marks <= 100`, `0 <= attendance, target, previous <= 100`).
* `src/storage.py`: Centralized CSV persistence layer using pandas. Reads and writes records to `data/students.csv`.
* `src/calculator.py`: Academic metric computations (`calculate_metrics`, `class_summary`, `get_grade`) using numpy and standard statistics.
* `src/analyzer.py`: Diagnostic evaluation engine (`get_performance_level`, `compare_with_target`, `compare_with_previous`, `find_strong_weak`, `find_reasons`, `generate_suggestions`, `analyze_student`).
* `src/report.py`: ASCII progress bar generator (`text_bar`) and report formatters (`build_report`, `save_report`, `build_class_report`).
* `data/students.csv`: Comma-separated relational database preserving 11 structured columns.
* `tests/test_basic.py`: 14 pure assertion unit tests verifying academic mathematics and boundary conditions.

---

## 3. New Web Application Architecture
The web application architecture integrates the original Python modules into a lightweight, high-performance full-stack system:

```text
+-------------------------------------------------------------------------+
|                        Browser Frontend (Client)                        |
|   HTML5  ·  CSS3 (Glassmorphism & Dark Palette)  ·  Vanilla JavaScript  |
+-------------------------------------------------------------------------+
                                     │
                             REST API / JSON
                                     ▼
+-------------------------------------------------------------------------+
|                        Flask Web Server (app.py)                        |
|  - Thread-Safe File Locks (csv_lock)                                    |
|  - Subprocess Code Runner with AST static security & timeout            |
|  - RESTful Endpoints (/api/dashboard, /api/students, /api/csv, etc.)   |
+-------------------------------------------------------------------------+
                                     │
                     Direct Module Function Imports
                                     ▼
+-------------------------------------------------------------------------+
|                        Original Python Engine                           |
|  src/storage.py    src/calculator.py    src/analyzer.py   src/report.py |
+-------------------------------------------------------------------------+
                                     │
                             Read / Write
                                     ▼
+-------------------------------------------------------------------------+
|                   Persistent Storage: data/students.csv                 |
|                   Automatic Backups: data/backups/                      |
+-------------------------------------------------------------------------+
```

---

## 4. Frontend Design System
The user interface avoids noisy or generic AI layouts. Instead, it delivers a focused, developer-workspace experience:
* **Glassmorphism**: Translucent panels (`background: rgba(16, 22, 18, 0.75)` with `backdrop-filter: blur(12px)`), hairline borders (`rgba(183, 247, 197, 0.12)`), and deep soft drop shadows.
* **Layout**: Collapsible left sidebar navigation, top workspace breadcrumb bar, and modular panels.
* **Componentry**: Modals with backdrop blur, customizable data tables, live toast notifications, and animated progress meters.

---

## 5. Color Palette and Typography
Strict adherence to the approved dark visual color family:

| Role | Color Name | Hex Code | Visual Application |
|---|---|---|---|
| Main Background | Black | `#090D0B` | Body background, terminal backgrounds |
| Surface Panels | Dark Black | `#101612` | Glassmorphic cards, sidebar, table containers |
| Primary Accent | Light Green | `#B7F7C5` | Active indicators, buttons, metrics, progress bars |
| Primary Text | White | `#FFFFFF` | Headings, key figures, table values |
| Muted Text | Muted White | `#AAB7AD` | Descriptions, labels, secondary metadata |

### Typography
* **Interface Text**: `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, `sans-serif`.
* **Code & Data**: `JetBrains Mono`, `Fira Code`, `Cascadia Code`, `monospace`.

---

## 6. Folder Structure
```text
Student-Performance-Analyzer/
│
├── frontend/
│   ├── index.html                  # Single Page Application master shell
│   │
│   ├── css/
│   │   ├── style.css               # Design system tokens, variables, master layout
│   │   ├── components.css          # Tables, buttons, badges, modals, toast alerts
│   │   ├── dashboard.css           # Metrics grids, stat counters, distribution cards
│   │   └── responsive.css          # Media queries for tablet and mobile devices
│   │
│   └── js/
│       ├── app.js                  # Master router, API fetch wrapper, toast alerts
│       ├── dashboard.js            # Dashboard stats and tier distribution
│       ├── students.js             # Student CRUD operations, search, and validation
│       ├── analysis.js             # Deep diagnostic evaluation and report export
│       ├── class-summary.js        # Class statistics and subject analytics
│       ├── csv-editor.js           # Spreadsheet editor and live CSV synchronization
│       ├── terminal.js             # VS Code-style sandboxed code executor
│       └── reports.js              # Generated reports archive and ASCII viewer
│
├── src/
│   ├── __init__.py                 # Package marker
│   ├── intro.py                    # Terminal startup welcome and loading bar
│   ├── auth.py                     # CLI passcode verification logic
│   ├── data_input.py               # Input validation boundaries (0-100)
│   ├── storage.py                  # CSV persistence and DataFrame conversion
│   ├── calculator.py               # Academic math, grades, and class statistics
│   ├── analyzer.py                 # Diagnostic analysis and improvement suggestions
│   └── report.py                   # ASCII visual progress bars and report writing
│
├── data/
│   ├── students.csv                # Primary CSV database (11 structured columns)
│   └── backups/                    # Auto-generated timestamped backups before saves
│
├── reports/                        # Saved ASCII individual and class reports
│
├── tests/
│   ├── __init__.py                 # Package marker
│   ├── test_basic.py               # Original 14 assertion unit tests
│   └── test_web_integration.py     # 10 comprehensive web and API integration tests
│
├── app.py                          # Flask web server and REST API controller
├── main.py                         # Untouched original terminal application
├── requirements.txt                # Dependencies (pandas, numpy, flask)
├── README.md                       # High-level project summary and quickstart
├── USER_GUIDE.md                   # Comprehensive user and beginner manual
└── PROJECT_IMPLEMENTATION.md       # Full architecture and engineering documentation
```

---

## 7. Backend Integration
`app.py` directly imports and calls functions from the `src/` modules:
1. `calculate_metrics(student)` computes total marks (out of 500), percentage, average, and grade.
2. `analyze_student(student, metrics)` identifies strong/weak subjects, failing marks (< 40), target gap, previous trajectory, and personalized advice.
3. `class_summary(students)` computes class averages, medians, highest, lowest, and toppers.
4. `build_report()` and `build_class_report()` generate standard ASCII text reports with visual block bars (`█`).

Thread safety is guaranteed via `threading.Lock()` (`csv_lock`), ensuring atomic file updates.

---

## 8. API Endpoint Documentation

| Method | Endpoint | Description | Request Body / Query Params | Response Structure |
|---|---|---|---|---|
| `GET` | `/` | Serves SPA frontend | None | HTML |
| `GET` | `/api/dashboard` | Dashboard metrics | None | `{ success, data: { total_students, class_average, class_median, topper, ... } }` |
| `GET` | `/api/students` | Retrieve students | `?search=...&sort=...&order=...` | `{ success, count, students: [...] }` |
| `POST` | `/api/students` | Add a new student | JSON Student object | `{ success, message, student: {...} }` |
| `GET` | `/api/students/<roll>` | Retrieve single student | None | `{ success, student: {...} }` |
| `PUT` | `/api/students/<roll>` | Update student | JSON Student object | `{ success, message, student: {...} }` |
| `DELETE` | `/api/students/<roll>` | Delete student | None | `{ success, message }` |
| `GET` | `/api/students/<roll>/analysis` | Individual analysis | None | `{ success, student, metrics, analysis, report_text }` |
| `GET` | `/api/class-summary` | Class statistics | None | `{ success, data: { summary, subject_stats, ... } }` |
| `GET` | `/api/csv` | Raw CSV records | None | `{ success, columns, records, total_records, file_info }` |
| `POST` | `/api/csv` | Add row to CSV | JSON Student object | `{ success, message, student: {...} }` |
| `PUT` | `/api/csv` | Update CSV records | `{ records: [...] }` | `{ success, message, total_records }` |
| `DELETE` | `/api/csv/<roll>` | Delete row from CSV | None | `{ success, message, roll_no }` |
| `GET` | `/api/csv/download` | Download students.csv | None | File download (`text/csv`) |
| `GET` | `/api/health` | Deployment health check | None | `{ status: "healthy", service, timestamp, storage }` |
| `POST` | `/api/reports/student` | Generate student report | `{ roll_no: int }` | `{ success, message, filename, report_text }` |
| `POST` | `/api/reports/class` | Generate class report | None | `{ success, message, filename, report_text }` |
| `GET` | `/api/reports` | List saved reports | None | `{ success, reports: [...] }` |
| `GET` | `/api/reports/<filename>` | View / download report | `?download=1` | File content / download |
| `POST` | `/api/terminal/run` | Execute Python code | `{ code: str }` | `{ success, stdout, stderr, execution_time_ms }` |

---

## 9. CSV Viewer and Editor
The CSV workspace allows full spreadsheet interaction directly linked with `data/students.csv`:
* **Spreadsheet Table**: Displays row indices, all 11 columns, and cell editing inputs.
* **Validation**: Checks for numeric values between 0 and 100 for marks and percentages, non-empty student names, and roll number range (1–999999).
* **Duplicate Prevention**: Rejects any duplicate roll numbers before writing to disk.
* **Automatic Backup**: On every save operation, a copy of `data/students.csv` is automatically backed up to `data/backups/students_backup_<timestamp>.csv`.

---

## 10. CSV Download Mechanism
The `/api/csv/download` route reads the currently saved `data/students.csv` from storage and streams it to the user's browser with the header `Content-Disposition: attachment; filename="students.csv"`. This guarantees that users always receive the authentic, up-to-date dataset.

---

## 11. Python Terminal Architecture
The Python Terminal is inspired by Visual Studio Code. It provides:
* Monospaced code textarea with line numbers, tab indent support, and keyboard shortcut (`Ctrl + Enter` / `Cmd + Enter`).
* One-click presets: *Calculate Percentage & Grade*, *Identify Failing Scores (< 40)*, *Attendance Eligibility Check*, *NumPy Vectorized Metrics*.
* Real-time millisecond execution timer badge.
* Terminal output console displaying stdout in light green (`#B7F7C5`) and errors in soft red (`#FF7B7B`).

---

## 12. Terminal Security Restrictions
To prevent unauthorized access, infinite loops, and server compromise, user code is executed under strict security rules:
1. **AST Static Analysis**: Code is parsed into an Abstract Syntax Tree before execution. Any attempts to import blocked modules (`os`, `sys`, `subprocess`, `socket`, `shutil`, `urllib`, etc.) or call restricted functions (`open`, `eval`, `exec`, `__import__`, `input`) are immediately rejected before running.
2. **Subprocess Isolation**: Code is saved to a temporary directory (`tempfile.mkdtemp()`) and executed in an isolated child Python process with isolated working directory.
3. **Execution Timeout**: Enforced hard timeout of 5.0 seconds. Any infinite loops (`while True: pass`) are killed automatically.
4. **Filesystem Protection**: The temporary directory is deleted immediately after execution, preventing file accumulation.

---

## 13. Installation Instructions
1. **Verify Python 3.10+**:
   ```bash
   python --version
   ```
2. **Clone / Open Workspace**:
   Navigate to the project root directory.
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 14. Dependency Management
The project intentionally minimizes external dependencies:
* `pandas`: Required for CSV DataFrame manipulation.
* `numpy`: Required for mathematical summations and statistics.
* `flask`: Required for web server and REST API routing.

---

## 15. How to Run the Original Terminal Application
The original terminal application remains 100% operational and independent:
```bash
python main.py
```
* **Authentication Password**: `python@2026`
* **Features**: Complete 6-option menu loop with interactive student data entry, individual analysis, class reports, and ASCII progress bars.

---

## 16. How to Start the Flask Web Application
To launch the developer workspace web interface:
```bash
python app.py
```
* Access the interface in your web browser at: **`http://127.0.0.1:5000`**
* The server will automatically load `data/students.csv` and serve the dashboard.

---

## 17. Testing Instructions
The project includes two layers of automated test suites:

### A. Core Mathematical & Logic Tests
```bash
python -c "from tests.test_basic import run_all_tests; run_all_tests()"
```
Runs 14 pure assertion unit tests verifying Rahul's metrics, grade calculations, strong/weak subject identification, trajectory logic, and class summaries.

### B. Full Web & API Integration Tests
```bash
python tests/test_web_integration.py
```
Executes 10 comprehensive tests covering:
1. Original unit test regression.
2. Frontend index page serving.
3. Dashboard metrics API.
4. Student retrieval and search query filtering.
5. Student creation, bounds validation, and duplicate rejection.
6. Student PUT update and deletion.
7. Diagnostic analysis and class summary.
8. CSV spreadsheet endpoints and download.
9. Report generation and archive listing.
10. Sandboxed Python terminal execution, AST blocks, and timeouts.

---

## 18. Troubleshooting
* **`ModuleNotFoundError: No module named 'flask'`**: Run `pip install -r requirements.txt`.
* **Port 5000 Already in Use**: Run with a custom port: `set PORT=5050 && python app.py` (Windows) or `PORT=5050 python app.py` (Linux/macOS).
* **CSV Permissions Error**: Ensure `data/students.csv` is not open in exclusive write mode in desktop Excel.
* **Terminal Script Timeout**: Code taking longer than 5 seconds will terminate with a timeout warning. Ensure loops have termination conditions.

---

## 19. Known Limitations
* The application runs locally as a single-instance development tool.
* For multi-user concurrent production deployment on public networks, production WSGI servers (such as Gunicorn or Waitress) and HTTPS reverse proxies (e.g. Nginx) are recommended.

---

## 20. Future Development Possibilities
* Export reports to PDF with custom letterheads.
* Multi-semester historical trend tracking across 8 semesters.
* Role-based authentication (Student Portal vs Faculty Advisory Portal).
* Automatic email dispatch of academic warnings to counselors.
