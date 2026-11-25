# Student Performance Analyzer — Developer Workspace & Web Application

A comprehensive academic analytics, student diagnostic advisory, and performance management platform developed in Python. Features both a modern, minimalist **Developer Workspace Web Interface** (Flask, HTML5, CSS3 Glassmorphism, Vanilla JS) and the untouched **Original Terminal Application** (`main.py`).

---

## 1. Project Overview

The **Student Performance Analyzer** assists college students, educators, and academic counselors in evaluating examination performance and attendance trends. By reading and writing records to structured CSV storage (`data/students.csv`) via Pandas, the application computes aggregate metrics (percentages, grade allocations, and statistical medians) and applies rule-based analytical logic to generate actionable, personalized improvement recommendations.

### Key Capabilities
* **Interactive Web Dashboard**: Live metric counters, class average, topper display, attendance rate, and performance tier distribution.
* **Student Roster Management**: Full CRUD operations (Add, Edit, Delete with auto-backup, Search, and Sort).
* **Diagnostic Performance Analysis**: In-depth individual evaluation with subject breakdown bars, comparative benchmarks, failing subject alerts, and personalized recommendations.
* **Class Analytics**: Cohort averages, medians, highest/lowest scores, subject-wise pass rates, and grade distribution.
* **CSV Workspace**: Spreadsheet-style editor directly synced with `data/students.csv`, including validation, duplicate prevention, and atomic backups.
* **Python Terminal**: VS Code-style sandboxed code execution environment with AST safety verification, resource limits, and execution timers.
* **Reports Archive**: Instant generation, previewing, and downloading of timestamped individual and class text reports.
* **Original Terminal App**: Interactive CLI with password authentication (`python@2026`) and numerical menu.

---

## 2. Technology Stack & Design System

* **Backend**: Python 3.10+, Flask, Pandas, NumPy, Statistics
* **Frontend**: HTML5, CSS3 (Modern Glassmorphism), Vanilla JavaScript (No heavy frameworks)
* **Design Philosophy**: Minimalist dark developer workspace inspired by GitHub, VS Code, and Discord.
* **Color Palette**:
  * Main Background: `#090D0B` (Black)
  * Surface Panels: `#101612` (Dark Black with subtle glassmorphic blur)
  * Accent: `#B7F7C5` (Light Green)
  * Primary Text: `#FFFFFF` (White)
  * Secondary Text: `#AAB7AD` (Muted White)

---

## 3. Project Structure

```text
Student-Performance-Analyzer/
│
├── frontend/
│   ├── index.html                  # Single Page Application master shell
│   ├── css/
│   │   ├── style.css               # Design system tokens and master layout
│   │   ├── components.css          # Tables, buttons, badges, modals, toast alerts
│   │   ├── dashboard.css           # Metrics grids, stat counters, distribution cards
│   │   └── responsive.css          # Mobile and tablet responsiveness
│   └── js/
│       ├── app.js                  # Master SPA router and API helper
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
├── main.py                         # Original interactive terminal application
├── requirements.txt                # Dependencies (pandas, numpy, flask)
├── README.md                       # Project documentation
├── USER_GUIDE.md                   # Step-by-step user and setup manual
└── PROJECT_IMPLEMENTATION.md       # Comprehensive architectural documentation
```

---

## 4. Installation & Setup

1. **Verify Python 3.10+**:
   ```bash
   python --version
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. How to Run the Applications

### A. Launch the Web Application (Recommended)
```bash
python app.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

### B. Launch the Original Terminal Application
```bash
python main.py
```
* **Application Password**: `python@2026`

---

## 6. Cloud Deployment Guide (Render, Railway, Heroku, Docker)

The project includes all required deployment descriptors:
* `Procfile`: Configured with `web: gunicorn app:app`
* `runtime.txt`: Configured with `python-3.11.9`
* `requirements.txt`: Includes `gunicorn` and `waitress`
* Dynamic host & port binding: `0.0.0.0` and `$PORT`

### Deploying to Render (Free Web Service)
1. Push this repository to GitHub or GitLab.
2. In [Render Dashboard](https://dashboard.render.com/), click **New +** > **Web Service**.
3. Select your repository.
4. Set the following settings:
   * **Environment**: `Python 3`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app`
5. Click **Create Web Service**. Render will automatically detect the Procfile, bind the assigned port, and launch the application.

### Deploying to Railway / Heroku
* **Railway**: Create a new project from your GitHub repo. Railway auto-detects `Procfile` and deploys automatically.
* **Heroku**:
  ```bash
  heroku create student-performance-analyzer
  git push heroku main
  heroku open
  ```

### Deploying Locally on Windows with Waitress (Production WSGI)
```bash
waitress-serve --listen=0.0.0.0:5000 app:app
```

---

## 7. Running Tests

### Core Unit Tests:
```bash
python -m tests.test_basic
```

### Full Web & API Integration Tests:
```bash
python tests/test_web_integration.py
```

---

## 7. Documentation
* For detailed architectural analysis, API schemas, and technical implementation decisions, see **`PROJECT_IMPLEMENTATION.md`**.
* For step-by-step menu navigation and troubleshooting guide, see **`USER_GUIDE.md`**.
