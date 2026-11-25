"""Flask Web Application for Student Performance Analyzer.

Integrates the existing Python analytics modules, CSV storage, and report generators
into a modern, RESTful API and developer-workspace web interface.
"""

import os
import sys
import time
import shutil
import threading
import subprocess
import datetime
import tempfile
import ast
from flask import Flask, jsonify, request, send_file, send_from_directory

# Ensure project root is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.storage import (
    initialize_data,
    load_data,
    save_data,
    get_all_students,
    get_student_by_roll,
    add_student,
    update_student,
    delete_student,
    CSV_FILE_PATH,
    CSV_COLUMNS
)
from src.calculator import calculate_metrics, class_summary, get_grade
from src.analyzer import analyze_student
from src.report import build_report, save_report, build_class_report
from src.data_input import SUBJECTS, MAX_MARKS

# Initialize Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "frontend"),
    static_url_path="/static"
)
app.config["JSON_SORT_KEYS"] = False

# Thread lock for CSV file write coordination
csv_lock = threading.Lock()

# Backup directory
BACKUP_DIR = os.path.join(BASE_DIR, "data", "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)


def backup_csv():
    """Create a timestamped backup copy of students.csv."""
    if os.path.exists(CSV_FILE_PATH):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"students_backup_{ts}.csv")
        try:
            shutil.copy2(CSV_FILE_PATH, backup_path)
            return backup_path
        except Exception as e:
            print(f"Warning: Failed to create CSV backup: {e}")
    return None


def validate_student_payload(data, is_update=False):
    """Validate student input dictionary before saving.
    Returns (cleaned_dict, error_message).
    """
    if not isinstance(data, dict):
        return None, "Request payload must be a JSON object."

    name = str(data.get("name", "")).strip()
    if not name:
        return None, "Student name is required and cannot be empty."

    try:
        roll_no = int(data.get("roll_no"))
        if roll_no < 1 or roll_no > 999999:
            return None, "Roll number must be between 1 and 999999."
    except (TypeError, ValueError):
        return None, "Valid integer roll number is required."

    class_name = str(data.get("class", data.get("class_name", ""))).strip()
    if not class_name:
        return None, "Class / Semester is required."

    # Validate marks
    marks_raw = data.get("marks")
    if not isinstance(marks_raw, dict):
        # Maybe marks passed directly as subject fields
        marks_raw = {
            sub: data.get(sub.lower(), data.get(sub))
            for sub in SUBJECTS
        }

    clean_marks = {}
    for sub in SUBJECTS:
        score_val = marks_raw.get(sub)
        if score_val is None:
            # check lowercase
            score_val = marks_raw.get(sub.lower())
        if score_val is None:
            return None, f"Marks for '{sub}' are required."
        try:
            score = float(score_val)
            if score < 0 or score > MAX_MARKS:
                return None, f"Marks for '{sub}' must be between 0 and {MAX_MARKS}."
            clean_marks[sub] = int(score) if score.is_integer() else round(score, 2)
        except (TypeError, ValueError):
            return None, f"Invalid numeric score for '{sub}'."

    # Validate attendance, target, previous
    def parse_bounded_float(field_name):
        val = data.get(field_name)
        if val is None:
            return None, f"Field '{field_name}' is required."
        try:
            fval = float(val)
            if fval < 0 or fval > 100:
                return None, f"Field '{field_name}' must be between 0 and 100."
            return round(fval, 2), None
        except (TypeError, ValueError):
            return None, f"Field '{field_name}' must be a valid percentage (0-100)."

    attendance, err = parse_bounded_float("attendance")
    if err:
        return None, err

    target, err = parse_bounded_float("target")
    if err:
        return None, err

    previous, err = parse_bounded_float("previous")
    if err:
        return None, err

    student = {
        "name": name,
        "roll_no": roll_no,
        "class": class_name,
        "marks": clean_marks,
        "attendance": attendance,
        "target": target,
        "previous": previous
    }
    return student, None


# ---------------------------------------------------------
# Static & HTML Frontend Serving
# ---------------------------------------------------------

@app.route("/")
def index():
    """Serve the single-page application frontend."""
    return send_file(os.path.join(BASE_DIR, "frontend", "index.html"))


@app.route("/<path:path>")
def serve_static(path):
    """Serve frontend static files or fallback to index.html."""
    file_path = os.path.join(BASE_DIR, "frontend", path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return send_file(file_path)
    return send_file(os.path.join(BASE_DIR, "frontend", "index.html"))


# ---------------------------------------------------------
# REST API Endpoints
# ---------------------------------------------------------

@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    """Retrieve aggregate dashboard metrics and recent students."""
    with csv_lock:
        students = get_all_students()

    total_students = len(students)
    if total_students == 0:
        return jsonify({
            "success": True,
            "data": {
                "total_students": 0,
                "class_average": 0.0,
                "class_median": 0.0,
                "highest_percentage": 0.0,
                "lowest_percentage": 0.0,
                "topper": "N/A",
                "average_attendance": 0.0,
                "performance_breakdown": {"Good": 0, "Average": 0, "Needs Improvement": 0},
                "grade_breakdown": {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0},
                "recent_students": []
            }
        })

    summary = class_summary(students)

    performance_counts = {"Good": 0, "Average": 0, "Needs Improvement": 0}
    grade_counts = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    total_attendance = 0.0

    enhanced_students = []
    for s in students:
        m = calculate_metrics(s)
        a = analyze_student(s, m)
        performance_counts[a["level"]] = performance_counts.get(a["level"], 0) + 1
        grade_counts[m["grade"]] = grade_counts.get(m["grade"], 0) + 1
        total_attendance += s["attendance"]
        enhanced_students.append({
            "roll_no": s["roll_no"],
            "name": s["name"],
            "class": s["class"],
            "attendance": s["attendance"],
            "percentage": m["percentage"],
            "grade": m["grade"],
            "level": a["level"],
            "target": s["target"],
            "previous": s["previous"],
            "target_result": a["target_result"],
            "previous_result": a["previous_result"]
        })

    avg_attendance = round(total_attendance / total_students, 2)
    recent_students = list(reversed(enhanced_students))[:6]

    return jsonify({
        "success": True,
        "data": {
            "total_students": total_students,
            "class_average": summary["average"],
            "class_median": summary["median"],
            "highest_percentage": summary["highest"],
            "lowest_percentage": summary["lowest"],
            "topper": summary["topper"],
            "average_attendance": avg_attendance,
            "performance_breakdown": performance_counts,
            "grade_breakdown": grade_counts,
            "recent_students": recent_students
        }
    })


@app.route("/api/students", methods=["GET"])
def get_students():
    """Retrieve all student records with computed metrics and analysis."""
    search_query = request.args.get("search", "").strip().lower()
    sort_by = request.args.get("sort", "roll_no")
    order = request.args.get("order", "asc")

    with csv_lock:
        students = get_all_students()

    result = []
    for s in students:
        m = calculate_metrics(s)
        a = analyze_student(s, m)
        record = {
            **s,
            "metrics": m,
            "analysis": a
        }
        if search_query:
            roll_str = str(s["roll_no"]).lower()
            name_str = s["name"].lower()
            class_str = s["class"].lower()
            if search_query not in roll_str and search_query not in name_str and search_query not in class_str:
                continue
        result.append(record)

    # Sorting
    reverse = (order.lower() == "desc")
    if sort_by == "name":
        result.sort(key=lambda x: x["name"].lower(), reverse=reverse)
    elif sort_by == "percentage":
        result.sort(key=lambda x: x["metrics"]["percentage"], reverse=reverse)
    elif sort_by == "attendance":
        result.sort(key=lambda x: x["attendance"], reverse=reverse)
    else:  # default roll_no
        result.sort(key=lambda x: x["roll_no"], reverse=reverse)

    return jsonify({
        "success": True,
        "count": len(result),
        "students": result
    })


@app.route("/api/students", methods=["POST"])
def create_student():
    """Add a new student record to the CSV storage."""
    payload = request.get_json(silent=True)
    student, err = validate_student_payload(payload)
    if err:
        return jsonify({"success": False, "error": err}), 400

    with csv_lock:
        existing = get_student_by_roll(student["roll_no"])
        if existing:
            return jsonify({
                "success": False,
                "error": f"Student with Roll Number {student['roll_no']} already exists."
            }), 409

        backup_csv()
        saved = add_student(student)
        if not saved:
            return jsonify({"success": False, "error": "Failed to save student record to CSV."}), 500

    metrics = calculate_metrics(student)
    analysis = analyze_student(student, metrics)
    return jsonify({
        "success": True,
        "message": f"Student '{student['name']}' added successfully.",
        "student": {**student, "metrics": metrics, "analysis": analysis}
    }), 201


@app.route("/api/students/<int:roll_no>", methods=["GET"])
def get_student(roll_no):
    """Retrieve a single student record with metrics and analysis."""
    with csv_lock:
        student = get_student_by_roll(roll_no)
    if not student:
        return jsonify({"success": False, "error": f"No student found with Roll Number {roll_no}."}), 404

    metrics = calculate_metrics(student)
    analysis = analyze_student(student, metrics)
    return jsonify({
        "success": True,
        "student": {
            **student,
            "metrics": metrics,
            "analysis": analysis
        }
    })


@app.route("/api/students/<int:roll_no>", methods=["PUT"])
def modify_student(roll_no):
    """Update an existing student record."""
    payload = request.get_json(silent=True)
    student, err = validate_student_payload(payload, is_update=True)
    if err:
        return jsonify({"success": False, "error": err}), 400

    # Ensure roll number matches route or doesn't collide
    if student["roll_no"] != roll_no:
        return jsonify({"success": False, "error": "Cannot change the Roll Number of an existing record."}), 400

    with csv_lock:
        existing = get_student_by_roll(roll_no)
        if not existing:
            return jsonify({"success": False, "error": f"No student found with Roll Number {roll_no}."}), 404

        backup_csv()
        updated = update_student(roll_no, student)
        if not updated:
            return jsonify({"success": False, "error": "Failed to update student record in CSV."}), 500

    metrics = calculate_metrics(student)
    analysis = analyze_student(student, metrics)
    return jsonify({
        "success": True,
        "message": f"Student '{student['name']}' updated successfully.",
        "student": {**student, "metrics": metrics, "analysis": analysis}
    })


@app.route("/api/students/<int:roll_no>", methods=["DELETE"])
def remove_student(roll_no):
    """Delete a student record by roll number."""
    with csv_lock:
        existing = get_student_by_roll(roll_no)
        if not existing:
            return jsonify({"success": False, "error": f"No student found with Roll Number {roll_no}."}), 404

        backup_csv()
        deleted = delete_student(roll_no)
        if not deleted:
            return jsonify({"success": False, "error": "Failed to delete student record from CSV."}), 500

    return jsonify({
        "success": True,
        "message": f"Student {existing['name']} (Roll #{roll_no}) deleted successfully."
    })


@app.route("/api/students/<int:roll_no>/analysis", methods=["GET"])
def get_student_analysis(roll_no):
    """Generate and return individual student performance analysis."""
    with csv_lock:
        student = get_student_by_roll(roll_no)
    if not student:
        return jsonify({"success": False, "error": f"No student found with Roll Number {roll_no}."}), 404

    metrics = calculate_metrics(student)
    analysis = analyze_student(student, metrics)
    report_text = build_report(student, metrics, analysis)

    return jsonify({
        "success": True,
        "student": student,
        "metrics": metrics,
        "analysis": analysis,
        "report_text": report_text
    })


@app.route("/api/class-summary", methods=["GET"])
def get_class_summary():
    """Compute and return class-wide performance metrics, subject analytics, and topper."""
    with csv_lock:
        students = get_all_students()

    if not students:
        return jsonify({
            "success": True,
            "data": {
                "summary": class_summary([]),
                "subject_stats": {},
                "grade_distribution": {},
                "attendance_stats": {"average": 0.0, "below_75_count": 0},
                "report_text": build_class_report(class_summary([]))
            }
        })

    summary = class_summary(students)

    # Subject-wise statistics
    subject_stats = {}
    for sub in SUBJECTS:
        scores = [s["marks"][sub] for s in students]
        subject_stats[sub] = {
            "average": round(sum(scores) / len(scores), 2),
            "highest": max(scores),
            "lowest": min(scores),
            "failing_count": sum(1 for sc in scores if sc < 40)
        }

    # Attendance stats
    attendance_scores = [s["attendance"] for s in students]
    low_att_count = sum(1 for a in attendance_scores if a < 75)
    att_stats = {
        "average": round(sum(attendance_scores) / len(attendance_scores), 2),
        "highest": max(attendance_scores),
        "lowest": min(attendance_scores),
        "below_75_count": low_att_count
    }

    # Grade distribution
    grades = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for s in students:
        m = calculate_metrics(s)
        grades[m["grade"]] = grades.get(m["grade"], 0) + 1

    report_text = build_class_report(summary)

    return jsonify({
        "success": True,
        "data": {
            "summary": summary,
            "subject_stats": subject_stats,
            "grade_distribution": grades,
            "attendance_stats": att_stats,
            "report_text": report_text
        }
    })


# ---------------------------------------------------------
# CSV Data Management Endpoints
# ---------------------------------------------------------

@app.route("/api/csv", methods=["GET"])
def get_csv_data():
    """Retrieve raw CSV records for the spreadsheet editor."""
    with csv_lock:
        df = load_data()

    records = df.to_dict(orient="records")
    file_info = {}
    if os.path.exists(CSV_FILE_PATH):
        stat = os.stat(CSV_FILE_PATH)
        file_info = {
            "path": CSV_FILE_PATH,
            "size_bytes": stat.st_size,
            "last_modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }

    return jsonify({
        "success": True,
        "columns": CSV_COLUMNS,
        "records": records,
        "total_records": len(records),
        "file_info": file_info
    })


@app.route("/api/csv", methods=["PUT"])
def save_csv_data():
    """Save updated spreadsheet records to students.csv with validation and auto-backup."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or "records" not in payload:
        return jsonify({"success": False, "error": "Expected JSON payload with 'records' list."}), 400

    records = payload["records"]
    if not isinstance(records, list):
        return jsonify({"success": False, "error": "'records' must be an array."}), 400

    # Validate all records before saving
    seen_rolls = set()
    cleaned_rows = []
    import pandas as pd

    for idx, row in enumerate(records):
        try:
            roll_no = int(row.get("roll_no"))
            if roll_no < 1 or roll_no > 999999:
                return jsonify({"success": False, "error": f"Row {idx+1}: Roll number out of range (1-999999)."}), 400
            if roll_no in seen_rolls:
                return jsonify({"success": False, "error": f"Row {idx+1}: Duplicate roll number {roll_no} detected."}), 400
            seen_rolls.add(roll_no)
        except (TypeError, ValueError):
            return jsonify({"success": False, "error": f"Row {idx+1}: Invalid roll number."}), 400

        name = str(row.get("name", "")).strip()
        if not name:
            return jsonify({"success": False, "error": f"Row {idx+1}: Name cannot be empty."}), 400

        class_name = str(row.get("class_name", "")).strip()
        if not class_name:
            return jsonify({"success": False, "error": f"Row {idx+1}: Class name cannot be empty."}), 400

        cleaned_row = {
            "roll_no": roll_no,
            "name": name,
            "class_name": class_name
        }

        # Validate subject marks
        for sub in ["maths", "physics", "chemistry", "english", "cs"]:
            try:
                score = float(row.get(sub, 0))
                if score < 0 or score > 100:
                    return jsonify({"success": False, "error": f"Row {idx+1}: {sub.title()} score must be 0-100."}), 400
                cleaned_row[sub] = int(score) if score.is_integer() else round(score, 2)
            except (TypeError, ValueError):
                return jsonify({"success": False, "error": f"Row {idx+1}: Invalid score for {sub}."}), 400

        # Validate attendance, target, previous
        for metric in ["attendance", "target", "previous"]:
            try:
                val = float(row.get(metric, 0))
                if val < 0 or val > 100:
                    return jsonify({"success": False, "error": f"Row {idx+1}: {metric.title()} must be 0-100."}), 400
                cleaned_row[metric] = round(val, 2)
            except (TypeError, ValueError):
                return jsonify({"success": False, "error": f"Row {idx+1}: Invalid value for {metric}."}), 400

        cleaned_rows.append(cleaned_row)

    # Perform atomic backup and save
    with csv_lock:
        backup_csv()
        new_df = pd.DataFrame(cleaned_rows, columns=CSV_COLUMNS)
        saved = save_data(new_df)
        if not saved:
            return jsonify({"success": False, "error": "Failed to write data to CSV file."}), 500

    return jsonify({
        "success": True,
        "message": f"Successfully updated CSV with {len(cleaned_rows)} records.",
        "total_records": len(cleaned_rows)
    })


@app.route("/api/csv/download", methods=["GET"])
def download_csv():
    """Download current saved CSV file."""
    with csv_lock:
        if not os.path.exists(CSV_FILE_PATH):
            initialize_data()
        return send_file(
            CSV_FILE_PATH,
            as_attachment=True,
            download_name="students.csv",
            mimetype="text/csv"
        )


# ---------------------------------------------------------
# Report Generation & Viewer Endpoints
# ---------------------------------------------------------

@app.route("/api/reports/student", methods=["POST"])
def generate_student_report():
    """Generate and save an individual student academic report."""
    payload = request.get_json(silent=True) or {}
    roll_no = payload.get("roll_no")
    if not roll_no:
        return jsonify({"success": False, "error": "Roll number is required."}), 400

    try:
        roll_no = int(roll_no)
    except ValueError:
        return jsonify({"success": False, "error": "Roll number must be an integer."}), 400

    with csv_lock:
        student = get_student_by_roll(roll_no)
    if not student:
        return jsonify({"success": False, "error": f"No student found with Roll Number {roll_no}."}), 404

    metrics = calculate_metrics(student)
    analysis = analyze_student(student, metrics)
    report_text = build_report(student, metrics, analysis)
    filename = save_report(report_text, student["roll_no"])

    return jsonify({
        "success": True,
        "message": f"Report generated and saved to {filename}",
        "filename": filename,
        "report_text": report_text,
        "student_name": student["name"],
        "roll_no": student["roll_no"]
    })


@app.route("/api/reports/class", methods=["POST"])
def generate_class_report():
    """Generate and save a class summary report."""
    with csv_lock:
        students = get_all_students()

    summary = class_summary(students)
    report_text = build_class_report(summary)
    filename = save_report(report_text, "class")

    return jsonify({
        "success": True,
        "message": f"Class report generated and saved to {filename}",
        "filename": filename,
        "report_text": report_text,
        "students_count": summary["students"]
    })


@app.route("/api/reports", methods=["GET"])
def list_reports():
    """List all saved reports in the reports directory."""
    reports_dir = os.path.join(BASE_DIR, "reports")
    files = []
    if os.path.exists(reports_dir):
        for fname in os.listdir(reports_dir):
            if fname.endswith(".txt"):
                fpath = os.path.join(reports_dir, fname)
                stat = os.stat(fpath)
                report_type = "Class Summary" if "class" in fname else "Student Report"
                files.append({
                    "filename": fname,
                    "type": report_type,
                    "size_bytes": stat.st_size,
                    "created_at": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })
    files.sort(key=lambda x: x["created_at"], reverse=True)
    return jsonify({"success": True, "reports": files})


@app.route("/api/reports/<filename>", methods=["GET"])
def get_report_content(filename):
    """View content of a specific saved report."""
    # Sanitization
    safe_name = os.path.basename(filename)
    if not safe_name.endswith(".txt"):
        return jsonify({"success": False, "error": "Invalid report file format."}), 400

    report_path = os.path.join(BASE_DIR, "reports", safe_name)
    if not os.path.exists(report_path):
        return jsonify({"success": False, "error": "Report file not found."}), 404

    as_download = request.args.get("download", "0") == "1"
    if as_download:
        return send_file(report_path, as_attachment=True, download_name=safe_name, mimetype="text/plain")

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify({
        "success": True,
        "filename": safe_name,
        "content": content
    })


# ---------------------------------------------------------
# Secure Python Terminal Execution Workspace
# ---------------------------------------------------------

BLOCKED_MODULES = {
    "os", "sys", "subprocess", "socket", "urllib", "requests",
    "http", "shutil", "pathlib", "ctypes", "multiprocessing",
    "pty", "commands", "posix", "nt", "_winapi", "winreg"
}

BLOCKED_CALLS = {
    "eval", "exec", "compile", "__import__", "open", "input",
    "getattr", "setattr", "delattr", "breakpoint"
}


def sanitize_code_ast(code_str):
    """Check Python AST for dangerous module imports or system calls.
    Returns (is_safe, error_message).
    """
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return False, f"Syntax Error on line {e.lineno}: {e.msg}"

    for node in ast.walk(tree):
        # Check imports: import os, sys
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_pkg = alias.name.split(".")[0]
                if root_pkg in BLOCKED_MODULES:
                    return False, f"Security Warning: Direct import of module '{root_pkg}' is restricted in terminal."

        # Check from X import Y
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root_pkg = node.module.split(".")[0]
                if root_pkg in BLOCKED_MODULES:
                    return False, f"Security Warning: Direct import from module '{root_pkg}' is restricted in terminal."

        # Check function calls
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in BLOCKED_CALLS:
                    return False, f"Security Warning: Function '{node.func.id}()' is restricted in terminal."

    return True, None


@app.route("/api/terminal/run", methods=["POST"])
def run_terminal_code():
    """Execute Python code in an isolated subprocess with AST safety checks and timeout."""
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "").strip()

    if not code:
        return jsonify({
            "success": False,
            "stdout": "",
            "stderr": "Error: No Python code provided to execute.",
            "execution_time_ms": 0.0
        }), 400

    # AST Static Security Analysis
    is_safe, sec_err = sanitize_code_ast(code)
    if not is_safe:
        return jsonify({
            "success": False,
            "stdout": "",
            "stderr": f"Security Policy Violation:\n{sec_err}\n\nNotice: System operations, shell calls, and unrestricted filesystem access are disabled in this environment.",
            "execution_time_ms": 0.0
        })

    # Prepare isolated execution environment
    temp_dir = tempfile.mkdtemp(prefix="spa_terminal_")
    script_path = os.path.join(temp_dir, "script.py")

    # Add safe student data access utility if user wants to examine loaded data
    prelude = (
        "# --- Safe Terminal Environment Prelude ---\n"
        "import numpy as np\n"
        "import statistics as stats\n"
        "# ----------------------------------------\n\n"
    )

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(prelude + code)

    start_time = time.time()
    try:
        sub_env = os.environ.copy()
        sub_env["PYTHONIOENCODING"] = "utf-8"
        sub_env["PYTHONPATH"] = os.pathsep.join([p for p in sys.path if os.path.exists(p)])

        # Run in separate subprocess with 5s timeout and isolated cwd
        proc = subprocess.run(
            [sys.executable, script_path],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=5.0,
            env=sub_env
        )
        elapsed = round((time.time() - start_time) * 1000, 2)
        stdout = proc.stdout
        stderr = proc.stderr
        success = (proc.returncode == 0)
    except subprocess.TimeoutExpired:
        elapsed = round((time.time() - start_time) * 1000, 2)
        stdout = ""
        stderr = "Execution Timeout Error: Code took longer than 5.0 seconds to finish. Infinite loops are terminated."
        success = False
    except Exception as e:
        elapsed = round((time.time() - start_time) * 1000, 2)
        stdout = ""
        stderr = f"Execution Error: {str(e)}"
        success = False
    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

    return jsonify({
        "success": success,
        "stdout": stdout,
        "stderr": stderr,
        "execution_time_ms": elapsed
    })


# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    initialize_data()
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f"   STUDENT PERFORMANCE ANALYZER — FLASK SERVER        ")
    print(f"=======================================================")
    print(f" * Server running on: http://127.0.0.1:{port}")
    print(f" * CSV Storage Path : {CSV_FILE_PATH}")
    print(f" * Terminal CLI Mode: Run 'python main.py' in terminal")
    print(f"=======================================================\n")
    app.run(host="127.0.0.1", port=port, debug=False)
