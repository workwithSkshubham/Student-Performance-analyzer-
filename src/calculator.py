"""Module for academic metrics and statistical calculations."""

import numpy as np
import statistics


def get_grade(percentage):
    """Determine the letter grade based on percentage score."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


def calculate_metrics(student):
    """Calculate total marks, percentage, average, and grade for a student."""
    marks_list = list(student["marks"].values())
    total_val = int(np.sum(marks_list))
    max_total = 500
    percentage_val = round((total_val / max_total) * 100, 2)
    average_val = round(float(np.mean(marks_list)), 2)
    grade_val = get_grade(percentage_val)

    return {
        "total": total_val,
        "max_total": max_total,
        "percentage": percentage_val,
        "average": average_val,
        "grade": grade_val
    }


def class_summary(students):
    """Compute aggregate statistical summary for a list of student records."""
    if not students:
        return {
            "students": 0,
            "average": 0.0,
            "median": 0.0,
            "highest": 0.0,
            "lowest": 0.0,
            "topper": "N/A"
        }

    percentages = []
    pairs = []
    for s in students:
        m = calculate_metrics(s)
        pct = m["percentage"]
        percentages.append(pct)
        pairs.append((s["name"], pct))

    student_count = len(students)
    avg_pct = round(statistics.mean(percentages), 2)
    med_pct = round(statistics.median(percentages), 2)
    high_pct = max(percentages)
    low_pct = min(percentages)

    top_students = [name for name, pct in pairs if pct == high_pct]
    topper_name = ", ".join(top_students)

    return {
        "students": student_count,
        "average": avg_pct,
        "median": med_pct,
        "highest": high_pct,
        "lowest": low_pct,
        "topper": topper_name
    }

