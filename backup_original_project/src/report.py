"""Module for constructing, formatting, and saving academic reports."""

import datetime


def text_bar(value, max_value=100, width=25):
    """Generate a fixed-width visual progress bar using block characters."""
    if max_value <= 0:
        return " " * width
    clamped_val = max(0.0, min(float(value), float(max_value)))
    filled_len = int(round((clamped_val / float(max_value)) * width))
    filled_len = max(0, min(filled_len, width))
    empty_len = width - filled_len
    return "█" * filled_len + " " * empty_len


def build_report(student, metrics, analysis):
    """Format a detailed individual academic analysis report."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weak_subs_str = ", ".join(analysis["weak_subjects"]) if analysis["weak_subjects"] else "None"

    lines = [
        "=" * 66,
        "             STUDENT ACADEMIC PERFORMANCE REPORT                 ",
        "=" * 66,
        f"Generated On : {now_str}",
        "-" * 66,
        "STUDENT INFORMATION:",
        f"  Name           : {student['name']}",
        f"  Roll Number    : {student['roll_no']}",
        f"  Class/Semester : {student['class']}",
        f"  Attendance     : {student['attendance']}%",
        "-" * 66,
        "SUBJECT MARKS BREAKDOWN:",
    ]

    for sub, score in student["marks"].items():
        bar = text_bar(score, 100, 20)
        lines.append(f"  {sub:<12} : {score:>3}/100 [{bar}]")

    lines.extend([
        "-" * 66,
        "ACADEMIC METRICS:",
        f"  Total Marks    : {metrics['total']} / {metrics['max_total']}",
        f"  Percentage     : {metrics['percentage']:.2f}%",
        f"  Average Score  : {metrics['average']:.2f}",
        f"  Letter Grade   : {metrics['grade']}",
        f"  Performance    : {analysis['level']}",
        "-" * 66,
        "COMPARATIVE BENCHMARKS:",
        f"  Target Goal    : {student['target']}% ({analysis['target_result']})",
        f"  Previous Term  : {student['previous']}% ({analysis['previous_result']})",
        f"  Best Subject   : {analysis['best_subject']} ({student['marks'][analysis['best_subject']]})",
        f"  Weakest Subject: {analysis['weakest_subject']} ({student['marks'][analysis['weakest_subject']]})",
        f"  Failing/Weak   : {weak_subs_str}",
        "-" * 66,
        "PERFORMANCE OBSERVATIONS & REASONS:"
    ])

    for reason in analysis["reasons"]:
        lines.append(f"  * {reason}")

    lines.extend([
        "-" * 66,
        "ACTIONABLE IMPROVEMENT SUGGESTIONS:"
    ])

    for suggestion in analysis["suggestions"]:
        lines.append(f"  * {suggestion}")

    lines.append("=" * 66)
    return "\n".join(lines)


def save_report(report_text, roll_no):
    """Save the generated report text into the reports directory."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/report_{roll_no}_{timestamp}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as file_handle:
            file_handle.write(report_text)
        return filename
    except Exception as err:
        print(f"Error saving report to file: {err}")
        return None


def build_class_report(summary):
    """Format class-wide aggregate metrics into a readable summary report."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "=" * 66,
        "               CLASS PERFORMANCE SUMMARY REPORT                  ",
        "=" * 66,
        f"Generated On         : {now_str}",
        "-" * 66,
        f"Total Students Count : {summary['students']}",
        f"Class Average Score  : {summary['average']:.2f}%",
        f"Class Median Score   : {summary['median']:.2f}%",
        f"Highest Score        : {summary['highest']:.2f}%",
        f"Lowest Score         : {summary['lowest']:.2f}%",
        f"Class Topper(s)      : {summary['topper']}",
        "=" * 66
    ]
    return "\n".join(lines)

