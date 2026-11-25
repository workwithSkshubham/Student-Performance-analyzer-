"""End-to-End Integration and Regression Test Suite for Web Application."""

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
from app import app
from tests.test_basic import run_all_tests as run_original_tests
import src.storage as storage

def run_integration_tests():
    print("==================================================")
    print("  RUNNING REGRESSION & INTEGRATION TESTS          ")
    print("==================================================")

    # 1. Verify original unit tests still pass
    print("[1/10] Verifying original Python unit tests...")
    run_original_tests()
    print("  -> Original unit tests PASSED.")

    client = app.test_client()

    # 2. Test Frontend Index Route
    print("[2/10] Testing Frontend Index Page Route (/)...")
    res = client.get("/")
    assert res.status_code == 200, f"Index failed: {res.status_code}"
    assert b"Student Performance Analyzer" in res.data, "Index missing title"
    print("  -> Frontend route PASSED.")

    # 3. Test Dashboard API
    print("[3/10] Testing /api/dashboard endpoint...")
    res = client.get("/api/dashboard")
    assert res.status_code == 200, f"Dashboard failed: {res.status_code}"
    dash_data = res.get_json()["data"]
    assert dash_data["total_students"] >= 6, "Expected at least 6 students"
    assert dash_data["class_average"] > 0, "Expected non-zero class average"
    assert "topper" in dash_data, "Missing topper info"
    print(f"  -> Dashboard API PASSED (Total Students: {dash_data['total_students']}, Avg: {dash_data['class_average']}%).")

    # 4. Test Student Retrieval & Search
    print("[4/10] Testing /api/students retrieval and filtering...")
    res = client.get("/api/students")
    assert res.status_code == 200, f"Students failed: {res.status_code}"
    students = res.get_json()["students"]
    assert len(students) >= 6, "Expected student records"
    assert "metrics" in students[0], "Missing calculated metrics"
    assert "analysis" in students[0], "Missing calculated analysis"
    
    # Test search
    res_search = client.get("/api/students?search=Rahul")
    assert res_search.status_code == 200
    assert any(s["name"] == "Rahul" for s in res_search.get_json()["students"])
    print("  -> Student retrieval & search PASSED.")

    # 5. Test Student Creation, Validation & Duplicate Prevention
    print("[5/10] Testing /api/students POST creation and duplicate prevention...")
    test_student = {
        "roll_no": 999,
        "name": "Integration Test Student",
        "class": "Sem 3",
        "marks": {
            "Maths": 85,
            "Physics": 78,
            "Chemistry": 92,
            "English": 88,
            "CS": 95
        },
        "attendance": 90.0,
        "target": 85.0,
        "previous": 80.0
    }
    # Add new
    res_add = client.post("/api/students", json=test_student)
    assert res_add.status_code == 201, f"Student addition failed: {res_add.get_json()}"
    
    # Try duplicate
    res_dup = client.post("/api/students", json=test_student)
    assert res_dup.status_code == 409, f"Duplicate roll number not rejected: {res_dup.status_code}"
    
    # Try invalid marks
    invalid_student = {**test_student, "roll_no": 998, "marks": {**test_student["marks"], "Maths": 150}}
    res_inv = client.post("/api/students", json=invalid_student)
    assert res_inv.status_code == 400, "Invalid marks not rejected"
    print("  -> Student creation, validation & duplicate checks PASSED.")

    # 6. Test Student Update & Deletion
    print("[6/10] Testing student PUT update and DELETE...")
    updated_student = {
        **test_student,
        "name": "Integration Test Student (Updated)",
        "attendance": 95.0
    }
    res_upd = client.put("/api/students/999", json=updated_student)
    assert res_upd.status_code == 200, f"Update failed: {res_upd.get_json()}"
    assert res_upd.get_json()["student"]["attendance"] == 95.0

    # Delete test record to keep CSV clean
    res_del = client.delete("/api/students/999")
    assert res_del.status_code == 200, f"Delete failed: {res_del.get_json()}"
    print("  -> Student update & deletion PASSED.")

    # 7. Test Student Analysis & Class Summary
    print("[7/10] Testing /api/students/101/analysis & /api/class-summary...")
    res_ana = client.get("/api/students/101/analysis")
    assert res_ana.status_code == 200, "Analysis failed"
    ana_data = res_ana.get_json()
    assert ana_data["metrics"]["total"] == 385, "Rahul total mismatch"
    assert ana_data["analysis"]["best_subject"] == "Maths", "Rahul best subject mismatch"

    res_cls = client.get("/api/class-summary")
    assert res_cls.status_code == 200, "Class summary failed"
    assert "subject_stats" in res_cls.get_json()["data"]
    print("  -> Student analysis & Class summary PASSED.")

    # 8. Test CSV Operations & Download
    print("[8/10] Testing /api/csv, /api/csv/download, direct CSV add and delete...")
    res_csv = client.get("/api/csv")
    assert res_csv.status_code == 200
    assert len(res_csv.get_json()["columns"]) == 11
    
    # Test POST /api/csv to directly add a record
    csv_add_student = {
        "roll_no": 997,
        "name": "Direct CSV Student",
        "class_name": "Sem 3",
        "maths": 80,
        "physics": 80,
        "chemistry": 80,
        "english": 80,
        "cs": 80,
        "attendance": 85.0,
        "target": 80.0,
        "previous": 75.0
    }
    res_csv_add = client.post("/api/csv", json=csv_add_student)
    assert res_csv_add.status_code == 201, f"Direct CSV add failed: {res_csv_add.get_json()}"

    # Verify student is in CSV
    res_check = client.get("/api/students/997")
    assert res_check.status_code == 200, "Direct CSV added student not found"

    # Test DELETE /api/csv/<roll_no> to directly delete a record from CSV
    res_csv_del = client.delete("/api/csv/997")
    assert res_csv_del.status_code == 200, f"Direct CSV delete failed: {res_csv_del.get_json()}"

    # Verify student is removed from CSV
    res_check_del = client.get("/api/students/997")
    assert res_check_del.status_code == 404, "Deleted student still exists in CSV"
    
    res_dl = client.get("/api/csv/download")
    assert res_dl.status_code == 200
    assert "text/csv" in res_dl.content_type
    assert b"roll_no,name,class_name" in res_dl.data

    # Test Health Check Endpoint for Deployment
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.get_json()["status"] == "healthy"
    print("  -> CSV endpoints, direct add/delete, and health check PASSED.")

    # 9. Test Report Generation
    print("[9/10] Testing report generation endpoints...")
    res_rep_s = client.post("/api/reports/student", json={"roll_no": 101})
    assert res_rep_s.status_code == 200, f"Student report failed: {res_rep_s.get_json()}"
    assert "report_text" in res_rep_s.get_json()

    res_rep_c = client.post("/api/reports/class")
    assert res_rep_c.status_code == 200, f"Class report failed: {res_rep_c.get_json()}"

    res_rep_list = client.get("/api/reports")
    assert res_rep_list.status_code == 200
    assert len(res_rep_list.get_json()["reports"]) > 0
    print("  -> Report generation & archiving PASSED.")

    # 10. Test Secure Python Terminal Execution
    print("[10/10] Testing Python terminal sandboxing & safety rules...")
    # Safe snippet
    res_term_safe = client.post("/api/terminal/run", json={"code": "marks = [80, 90]\nprint('Average:', sum(marks)/len(marks))"})
    assert res_term_safe.status_code == 200
    assert res_term_safe.get_json()["success"] is True
    assert "Average: 85.0" in res_term_safe.get_json()["stdout"]

    # Syntax error snippet
    res_term_syn = client.post("/api/terminal/run", json={"code": "def bad_syntax(:"})
    assert res_term_syn.status_code == 200
    assert res_term_syn.get_json()["success"] is False
    assert "Syntax Error" in res_term_syn.get_json()["stderr"]

    # Blocked dangerous import
    res_term_block = client.post("/api/terminal/run", json={"code": "import os\nos.listdir('.')"})
    assert res_term_block.status_code == 200
    assert res_term_block.get_json()["success"] is False
    assert "Security Policy Violation" in res_term_block.get_json()["stderr"]

    # Blocked open call
    res_term_open = client.post("/api/terminal/run", json={"code": "f = open('data/students.csv')"})
    assert res_term_open.status_code == 200
    assert res_term_open.get_json()["success"] is False
    assert "Security Policy Violation" in res_term_open.get_json()["stderr"]

    # Timeout handling
    res_term_timeout = client.post("/api/terminal/run", json={"code": "while True: pass"})
    assert res_term_timeout.status_code == 200
    assert res_term_timeout.get_json()["success"] is False
    assert "Timeout" in res_term_timeout.get_json()["stderr"]

    print("  -> Python terminal sandboxing & security PASSED.")

    print("\n==================================================")
    print("  ALL 10 INTEGRATION TESTS COMPLETED SUCCESSFULLY ")
    print("==================================================")

if __name__ == "__main__":
    run_integration_tests()
