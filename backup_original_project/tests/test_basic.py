"""Basic unit verification tests using pure assert statements."""

from src.calculator import get_grade, calculate_metrics, class_summary
from src.analyzer import (
    get_performance_level,
    compare_with_target,
    compare_with_previous,
    find_strong_weak
)
from src.report import text_bar


def run_all_tests():
    """Execute basic test verification assertions."""
    # Test dataset for Rahul
    rahul = {
        "name": "Rahul",
        "roll_no": 101,
        "class": "Sem 3",
        "marks": {
            "Maths": 90,
            "Physics": 55,
            "Chemistry": 75,
            "English": 80,
            "CS": 85
        },
        "attendance": 92.0,
        "target": 80.0,
        "previous": 70.0
    }

    metrics = calculate_metrics(rahul)

    # 1. Rahul's total = 385
    assert metrics["total"] == 385, f"Test 1 Failed: Expected 385, got {metrics['total']}"

    # 2. Rahul's percentage = 77.00
    assert metrics["percentage"] == 77.00, f"Test 2 Failed: Expected 77.00, got {metrics['percentage']}"

    # 3. Rahul's average = 77.00
    assert metrics["average"] == 77.00, f"Test 3 Failed: Expected 77.00, got {metrics['average']}"

    # 4. Rahul's grade = B
    assert metrics["grade"] == "B", f"Test 4 Failed: Expected B, got {metrics['grade']}"

    # 5. get_grade(95) == "A+"
    assert get_grade(95) == "A+", f"Test 5 Failed: Expected A+, got {get_grade(95)}"

    # 6. get_grade(30) == "F"
    assert get_grade(30) == "F", f"Test 6 Failed: Expected F, got {get_grade(30)}"

    # 7. Performance levels for Good, Average and Needs Improvement
    assert get_performance_level(85) == "Good", "Test 7a Failed: Expected Good"
    assert get_performance_level(65) == "Average", "Test 7b Failed: Expected Average"
    assert get_performance_level(35) == "Needs Improvement", "Test 7c Failed: Expected Needs Improvement"

    # 8. Target comparison for Rahul
    target_res = compare_with_target(rahul, metrics)
    assert target_res == "Target Not Achieved", f"Test 8 Failed: Expected Target Not Achieved, got {target_res}"

    # 9. Previous performance comparison for Rahul
    prev_res = compare_with_previous(rahul, metrics)
    assert prev_res == "Improved", f"Test 9 Failed: Expected Improved, got {prev_res}"

    # 10. Strongest subject = Maths
    best_sub, worst_sub, _ = find_strong_weak(rahul["marks"])
    assert best_sub == "Maths", f"Test 10 Failed: Expected Maths, got {best_sub}"

    # 11. Weakest subject = Physics
    assert worst_sub == "Physics", f"Test 11 Failed: Expected Physics, got {worst_sub}"

    # 12. Class summary using two student dictionaries
    sneha = {
        "name": "Sneha",
        "roll_no": 104,
        "class": "Sem 3",
        "marks": {
            "Maths": 95,
            "Physics": 90,
            "Chemistry": 88,
            "English": 92,
            "CS": 97
        },
        "attendance": 96.0,
        "target": 90.0,
        "previous": 88.0
    }
    two_students_summary = class_summary([rahul, sneha])
    assert two_students_summary["students"] == 2, "Test 12a Failed"
    assert two_students_summary["highest"] == 92.4, "Test 12b Failed"
    assert two_students_summary["lowest"] == 77.0, "Test 12c Failed"
    assert two_students_summary["topper"] == "Sneha", "Test 12d Failed"

    # 13. Text bar length equals the requested width
    bar_25 = text_bar(50, 100, 25)
    assert len(bar_25) == 25, f"Test 13 Failed: Expected width 25, got {len(bar_25)}"

    # 14. Empty class summary is handled correctly
    empty_res = class_summary([])
    assert empty_res["students"] == 0, "Test 14a Failed: Student count should be 0"
    assert empty_res["average"] == 0.0, "Test 14b Failed: Average should be 0.0"
    assert empty_res["topper"] == "N/A", "Test 14c Failed: Topper should be N/A"

    print("All tests passed!")


if __name__ == "__main__":
    run_all_tests()

