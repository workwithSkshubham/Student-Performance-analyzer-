# Student Performance Analyzer

A comprehensive, terminal-based academic analytics and student advisory application developed in Python. Designed for high clarity, transparency, and data-driven insights without requiring complex database engines or external network connectivity.

---

## 1. Project Overview

The **Student Performance Analyzer** is an educational software tool built to assist college students, educators, and academic counselors in evaluating examination performance and attendance trends. By reading and permanently writing records to structured CSV storage via Pandas, the application computes aggregate metrics (percentages, grade allocations, and statistical medians) and applies rule-based analytical logic to generate actionable, personalized improvement recommendations.

---

## 2. Problem Statement

In many educational settings:
- Student performance evaluation is confined to simple percentage calculation without understanding subject-level disparities.
- Academic counseling often lacks personalization; students receive generic advice rather than tailored action plans.
- Traditional database-driven systems (e.g., MySQL, cloud databases) involve heavy configuration, authentication setups, and external network dependencies, making them cumbersome for local demonstration and classroom evaluation.
- Teachers need an immediate, transparent method to assess both individual student growth and class-wide statistics without manual spreadsheet calculations.

---

## 3. Proposed Solution

The **Student Performance Analyzer** bridges these gaps by providing:
1. **Lightweight, Local Storage**: Uses a standard CSV file (`data/students.csv`) managed seamlessly through Pandas, requiring zero database installation or network connection.
2. **Deterministic Academic Analytics**: Accurately computes totals, percentages, averages, and letter grades using standard mathematical and statistical formulations.
3. **Comparative Benchmarking**: Compares current performance against individual target goals and previous semester scores to classify trajectory as *Improved*, *Declined*, or *Maintained*.
4. **Subject Disparity & Weak-Spot Detection**: Identifies failing subjects (< 40 marks), flags high discrepancies between strongest and weakest subjects (> 30 marks), and monitors attendance thresholds (< 75%).
5. **Personalized Advisory Engine**: Generates unique, tailored study tips and diagnostic observations based on specific student metrics.
6. **Permanent Report Generation**: Outputs well-structured, timestamped individual and class summary text reports into the `reports/` folder.

---

## 4. Key Features

- **Educational Welcome & Loading Animation**: Clean terminal greeting with inspirational academic quotes.
- **Passcode Authentication**: Built-in 3-attempt credential gate protecting academic data.
- **Data Validation Guardrails**: Safe numeric input readers preventing crashes from invalid characters or out-of-bounds numbers.
- **Duplicate Prevention**: Rejects duplicate roll numbers to maintain data integrity.
- **Pandas DataFrame Display**: Tabular overview of registered students with roll numbers, names, classes, and attendance rates.
- **Comprehensive Class Summary**: Computes total student count, class average, median, highest score, lowest score, and class topper (with tie handling).
- **Persistent Text Reports**: Visual progress bars (`█`) representing individual subject marks, saved with unique timestamps.

---

## 5. Technologies Used

- **Language**: Python 3.10+
- **Data Manipulation**: `pandas` (for CSV read/write operations and tabular display)
- **Numerical Computing**: `numpy` (for vectorized summation and mean calculations)
- **Statistical Analysis**: `statistics` (Python standard library for class median and average calculations)
- **Time Tracking**: `datetime` (Python standard library for timestamped report generation)

> **Architectural Note**: This project strictly abides by beginner-friendly constraints. It avoids classes/OOP, lambdas, decorators, generators, and unnecessary third-party packages, keeping all logic transparent and straightforward for viva examinations.

---

## 6. Project Structure

```text
Student-Performance-Analyzer/
│
├── data/
│   └── students.csv            # Persistent student records in CSV format
│
├── src/
│   ├── __init__.py             # Package marker
│   ├── intro.py                # Welcome banners and terminal loading animation
│   ├── auth.py                 # Security passcode verification logic
│   ├── data_input.py           # User input validation and student data acquisition
│   ├── storage.py              # CSV file management and Pandas conversions
│   ├── calculator.py           # Academic metrics and statistical computations
│   ├── analyzer.py             # Performance level, gap detection, and advice engine
│   └── report.py               # Visual ASCII progress bars and report writing
│
├── tests/
│   ├── __init__.py             # Package marker
│   └── test_basic.py           # Unit assertions verifying core math & logic
│
├── reports/
│   └── .gitkeep                # Directory storing exported student reports
│
├── main.py                     # Primary execution controller and menu loop
├── requirements.txt            # Package dependencies (pandas, numpy)
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
└── USER_GUIDE.md               # Step-by-step user and setup manual
```

---

## 7. Installation Instructions

1. **Clone or Download the Repository**:
   Place the project folder onto your local machine.

2. **Open Terminal / Command Prompt**:
   Navigate to the project root directory:
   ```bash
   cd Student-Performance-Analyzer
   ```

3. **Create and Activate a Virtual Environment** (Recommended):
   - On Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - On macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

4. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 8. How to Run the Project

Run the application controller from the project root:

```bash
python main.py
```

When prompted, enter the application password:
```text
python@2026
```

---

## 9. How to Run Tests

The test suite uses pure Python `assert` statements to ensure all calculations and logic rules function accurately without external test harnesses:

```bash
python -m tests.test_basic
```

**Expected Output**:
```text
All tests passed!
```

---

## 10. Expected Application Workflow

```text
[Start Application]
       │
       ▼
[Initialize CSV Storage] ──► (Create data/students.csv if missing)
       │
       ▼
[Display Welcome Screen & Loading Animation]
       │
       ▼
[Password Authentication] ──► (3 attempts maximum; exits if failed)
       │
       ▼
[Main Menu Loop]
       ├── [1] Analyze Existing Student ──► (Calculates metrics, prints & saves report)
       ├── [2] Add New Student          ──► (Validates input, checks duplicates, saves)
       ├── [3] Class Summary            ──► (Calculates mean, median, topper, exports report)
       ├── [4] View All Students        ──► (Prints DataFrame with key columns)
       ├── [5] Search by Roll Number    ──► (Displays profile and subject marks)
       └── [6] Exit                     ──► (Terminates session gracefully)
```

---

## 11. Screenshot Placeholders

### 1. Welcome Screen
```text
+------------------------------------------------------------------+
| *         STUDENT PERFORMANCE ANALYZER SYSTEM                    |
| *             Data-Driven Academic Insights                      |
+------------------------------------------------------------------+
| Welcome to the Student Performance Analyzer!                     |
|   * Marks don't define your potential.                           |
|   * Understand your performance. Improve your future.            |
|   * TRACK YOUR PROGRESS. FIND YOUR WEAK SPOTS. LEVEL UP.         |
| [====================] 100% Completed                            |
+------------------------------------------------------------------+
```

### 2. Password Authentication
```text
+------------------------------------------------------------------+
|                 SECURITY AUTHENTICATION REQUIRED                 |
+------------------------------------------------------------------+
| Enter application password (Attempts remaining: 3): ********     |
| Access Granted! Welcome to Student Performance Analyzer.         |
+------------------------------------------------------------------+
```

### 3. Main Menu
```text
+---------------------------------------------+
|        STUDENT PERFORMANCE ANALYZER         |
+---------------------------------------------+
|  [1] Analyze Existing Student               |
|  [2] Add New Student                        |
|  [3] Class Performance Summary              |
|  [4] View All Students                      |
|  [5] Search Student by Roll Number          |
|  [6] Exit                                   |
+---------------------------------------------+
```

### 4. Student Analysis Report
```text
+------------------------------------------------------------------+
|             STUDENT ACADEMIC PERFORMANCE REPORT                  |
+------------------------------------------------------------------+
| Student Name   : Rahul                  Roll Number : 101        |
| Attendance     : 92.0%                  Class       : Sem 3      |
| Total Marks    : 385 / 500              Percentage  : 77.00%     |
| Letter Grade   : B                      Performance : Good       |
| Best Subject   : Maths (90)             Weakest     : Physics (55)|
| Target Goal    : 80.0% (Target Not Achieved)                     |
| Previous Term  : 70.0% (Improved)                                |
| Observations   : High score disparity of 35 marks.               |
| Suggestions    : Bridge the 3.0% target gap with weekly revision.|
+------------------------------------------------------------------+
```

### 5. Class Summary
```text
+------------------------------------------------------------------+
|               CLASS PERFORMANCE SUMMARY REPORT                   |
+------------------------------------------------------------------+
| Total Students Count : 6                                         |
| Class Average Score  : 69.80%                                    |
| Class Median Score   : 73.50%                                    |
| Highest Score        : 92.40%                                    |
| Lowest Score         : 48.00%                                    |
| Class Topper(s)      : Sneha                                     |
+------------------------------------------------------------------+
```

---

## 12. Future Scope

1. **Visual Analytics Export**: Generate PNG bar charts and distribution histograms using visualization libraries when constraints allow.
2. **Multi-Semester Historical Tracking**: Track a single student across consecutive semesters (Sem 1 through Sem 8) to map longitudinal learning curves.
3. **Faculty & Parent Export**: Automatically format PDF reports formatted for parent-teacher conferences.
4. **Attendance Correlation Engine**: Statistical regression between hours of attendance and examination percentile rankings.

