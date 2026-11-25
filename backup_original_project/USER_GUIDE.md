# Student Performance Analyzer — Comprehensive User Guide

Welcome to the beginner-friendly User Guide for the **Student Performance Analyzer**. This guide explains how to install, run, and operate every feature of the project step-by-step, including explanations of how data is stored, how reports are generated, and solutions to common beginner errors.

---

## Table of Contents
1. [Installing Python](#1-installing-python)
2. [Opening the Project in VS Code](#2-opening-the-project-in-vs-code)
3. [Installing Dependencies](#3-installing-dependencies)
4. [Running the Program](#4-running-the-program)
5. [Entering the Application Password](#5-entering-the-application-password)
6. [Detailed Menu Guide & Examples](#6-detailed-menu-guide--examples)
   - [Option 1: Analyze Existing Student](#option-1-analyze-existing-student)
   - [Option 2: Add New Student](#option-2-add-new-student)
   - [Option 3: Class Performance Summary](#option-3-class-performance-summary)
   - [Option 4: View All Students](#option-4-view-all-students)
   - [Option 5: Search Student by Roll Number](#option-5-search-student-by-roll-number)
   - [Option 6: Exit](#option-6-exit)
7. [How CSV Data Storage Works](#7-how-csv-data-storage-works)
8. [Where Reports Are Stored](#8-where-reports-are-stored)
9. [Running the Test Suite](#9-running-the-test-suite)
10. [Troubleshooting & Common Errors](#10-troubleshooting--common-errors)

---

## 1. Installing Python

To run this application, Python 3.10 or newer must be installed on your computer.

### Windows:
1. Visit the official Python download website: [python.org/downloads](https://www.python.org/downloads/).
2. Download the latest Python installer.
3. **CRITICAL STEP**: During installation, check the box that says:
   `☑ Add Python to PATH` (or `Add python.exe to PATH`).
4. Click **Install Now**.
5. Once complete, open your terminal (PowerShell or Command Prompt) and verify:
   ```bash
   python --version
   ```

### macOS / Linux:
- On macOS using Homebrew: `brew install python`
- On Ubuntu/Debian Linux: `sudo apt update && sudo apt install python3 python3-pip python3-venv`

---

## 2. Opening the Project in VS Code

1. Launch **Visual Studio Code**.
2. Click **File** > **Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Select the folder `Student-Performance-Analyzer`.
4. Open the integrated terminal inside VS Code by pressing `` Ctrl + ` `` (Backtick) or navigating to **Terminal** > **New Terminal**.

---

## 3. Installing Dependencies

The project requires two external libraries: `pandas` and `numpy`.

From the project root directory inside your terminal, run:

```bash
pip install -r requirements.txt
```

If you prefer using a virtual environment:

```bash
# 1. Create the virtual environment
python -m venv .venv

# 2. Activate the virtual environment
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Windows Command Prompt:
.venv\Scripts\activate.bat
# On macOS / Linux:
source .venv/bin/activate

# 3. Install the dependencies
pip install -r requirements.txt
```

---

## 4. Running the Program

To start the application, execute:

```bash
python main.py
```

The system will initialize the CSV storage, display an ASCII welcome banner, show a smooth progress animation, and present the authentication prompt.

---

## 5. Entering the Application Password

For demonstration and access control, the system requires an application password.

- **Application Password**: `python@2026`
- **Maximum Allowed Attempts**: 3

### Terminal Prompt:
```text
==================================================================
                 SECURITY AUTHENTICATION REQUIRED                 
==================================================================
Enter application password (Attempts remaining: 3): python@2026

Access Granted! Welcome to Student Performance Analyzer.
```

If an incorrect password is typed, the system decrements the remaining attempts. If all 3 attempts fail, the application gracefully exits without crashing.

---

## 6. Detailed Menu Guide & Examples

Upon successful authentication, the main menu appears:

```text
=============================================
        STUDENT PERFORMANCE ANALYZER         
=============================================
  [1] Analyze Existing Student
  [2] Add New Student
  [3] Class Performance Summary
  [4] View All Students
  [5] Search Student by Roll Number
  [6] Exit
=============================================
Enter your choice (1-6):
```

---

### Option 1: Analyze Existing Student
Allows you to enter the roll number of an existing student to produce an in-depth analytical breakdown.

**Example Execution**:
1. Type `1` and press `Enter`.
2. Input roll number: `101`.
3. The system computes total marks, percentage, average, letter grade, comparative targets, weakness observations, and study suggestions. It also saves the report to the `reports/` folder.

**Sample Output**:
```text
==================================================================
             STUDENT ACADEMIC PERFORMANCE REPORT                 
==================================================================
Generated On : 2026-11-24 22:00:00
------------------------------------------------------------------
STUDENT INFORMATION:
  Name           : Rahul
  Roll Number    : 101
  Class/Semester : Sem 3
  Attendance     : 92.0%
------------------------------------------------------------------
SUBJECT MARKS BREAKDOWN:
  Maths        :  90/100 [██████████████████  ]
  Physics      :  55/100 [███████████         ]
  Chemistry    :  75/100 [███████████████     ]
  English      :  80/100 [████████████████    ]
  CS           :  85/100 [█████████████████   ]
------------------------------------------------------------------
ACADEMIC METRICS:
  Total Marks    : 385 / 500
  Percentage     : 77.00%
  Average Score  : 77.00
  Letter Grade   : B
  Performance    : Good
------------------------------------------------------------------
COMPARATIVE BENCHMARKS:
  Target Goal    : 80.0% (Target Not Achieved)
  Previous Term  : 70.0% (Improved)
  Best Subject   : Maths (90)
  Weakest Subject: Physics (55)
  Failing/Weak   : None
------------------------------------------------------------------
PERFORMANCE OBSERVATIONS & REASONS:
  * High score disparity of 35 marks between Maths and Physics.
------------------------------------------------------------------
ACTIONABLE IMPROVEMENT SUGGESTIONS:
  * Bridge the 3.0% target gap by following a structured weekly timetable and solving sample papers.
==================================================================

Report successfully saved to: reports/report_101_20261124_220000.txt
```

---

### Option 2: Add New Student
Interactively registers a new student. All numeric inputs are validated (marks between 0 and 100, attendance between 0 and 100). The system verifies that the roll number is not already taken.

**Example Input Flow**:
```text
Enter your choice (1-6): 2

--- Enter Student Details ---
Enter Student Name: Ananya Sharma
Enter Roll Number (1 - 999999): 107
Enter Class/Semester (e.g., Sem 3): Sem 3

Enter Marks for 5 Subjects (Max Marks: 100):
  Marks in Maths (0 - 100): 88
  Marks in Physics (0 - 100): 84
  Marks in Chemistry (0 - 100): 79
  Marks in English (0 - 100): 90
  Marks in CS (0 - 100): 92

Enter Attendance and Performance Targets:
  Attendance Percentage (0 - 100): 94
  Target Percentage (0 - 100): 85
  Previous Performance Percentage (0 - 100): 82

Student 'Ananya Sharma' added successfully!
```
The new record is appended to `data/students.csv` permanently, and the student's analysis report is immediately generated and saved.

---

### Option 3: Class Performance Summary
Calculates class-wide statistics across all registered students.

**Sample Output**:
```text
==================================================================
               CLASS PERFORMANCE SUMMARY REPORT                  
==================================================================
Generated On         : 2026-11-24 22:05:00
------------------------------------------------------------------
Total Students Count : 6
Class Average Score  : 69.80%
Class Median Score   : 73.50%
Highest Score        : 92.40%
Lowest Score         : 48.00%
Class Topper(s)      : Sneha
==================================================================

Class summary report saved to: reports/report_class_20261124_220500.txt
```

---

### Option 4: View All Students
Displays a concise tabular summary of all students directly using a Pandas DataFrame.

**Sample Output**:
```text
=======================================================
                 ALL REGISTERED STUDENTS                 
=======================================================
 roll_no   name class_name  attendance
     101  Rahul      Sem 3        92.0
     102  Priya      Sem 3        85.0
     103   Amit      Sem 3        68.0
     104  Sneha      Sem 3        96.0
     105  Karan      Sem 3        72.0
     106   Neha      Sem 3        80.0
=======================================================
```

---

### Option 5: Search Student by Roll Number
Quickly looks up a student's basic profile and subject marks without creating a full report.

**Example Input Flow**:
```text
Enter your choice (1-6): 5
Enter Roll Number to search: 102

----------------------------------------
Name           : Priya
Roll Number    : 102
Class/Semester : Sem 3
Attendance     : 85.0%
Marks:
  Maths        : 78/100
  Physics      : 82/100
  Chemistry    : 70/100
  English      : 88/100
  CS           : 91/100
Target Goal    : 85.0%
Previous Term  : 80.0%
----------------------------------------
```

---

### Option 6: Exit
Safely closes the application:
```text
Enter your choice (1-6): 6

Thank you for using Student Performance Analyzer. Goodbye!
```

---

## 7. How CSV Data Storage Works

Even if you have never worked with databases, the storage mechanism in this project is simple to understand:

1. **Storage File**: All data lives in `data/students.csv`.
2. **Plain Text Format**: CSV stands for *Comma-Separated Values*. Each line represents one student, and each value is separated by a comma.
3. **No External Server**: You do not need MySQL, PostgreSQL, or Apache running.
4. **Permanent Preservation**: When you add a new student using Option 2, `src/storage.py` appends the record and saves it using `pandas.DataFrame.to_csv()`. When you restart the program tomorrow, all previously entered students are still there!
5. **Initial Records**: The project ships with 6 pre-configured students:
   - `101,Rahul`
   - `102,Priya`
   - `103,Amit`
   - `104,Sneha`
   - `105,Karan`
   - `106,Neha`

---

## 8. Where Reports Are Stored

Every time an individual analysis (Option 1 or Option 2) or a class summary (Option 3) is generated, a `.txt` file is written to the `reports/` folder.

- **Individual Report Filename**: `report_<roll_no>_<timestamp>.txt` (e.g., `reports/report_101_20261124_220000.txt`)
- **Class Report Filename**: `report_class_<timestamp>.txt` (e.g., `reports/report_class_20261124_220500.txt`)

These files can be opened in VS Code, Notepad, or emailed to teachers and parents.

---

## 9. Running the Test Suite

Before presenting the project in your practical exam or viva, you can run the built-in verification suite.

In the project root, execute:

```bash
python -m tests.test_basic
```

If all 14 unit assertions pass successfully, the terminal prints:
```text
All tests passed!
```

---


