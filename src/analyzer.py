"""Module for evaluating academic performance and providing recommendations."""

WEAK_MARKS_LIMIT = 40
LOW_ATTENDANCE_LIMIT = 75


def get_performance_level(percentage):
    """Categorize performance level into Good, Average, or Needs Improvement."""
    if percentage >= 75:
        return "Good"
    elif percentage >= 50:
        return "Average"
    else:
        return "Needs Improvement"


def compare_with_target(student, metrics):
    """Compare current percentage with target percentage."""
    if metrics["percentage"] >= student["target"]:
        return "Target Achieved"
    return "Target Not Achieved"


def compare_with_previous(student, metrics):
    """Compare current percentage with previous examination score."""
    if metrics["percentage"] > student["previous"]:
        return "Improved"
    elif metrics["percentage"] < student["previous"]:
        return "Declined"
    else:
        return "Maintained"


def find_strong_weak(marks):
    """Identify the strongest, weakest, and failing subjects from marks."""
    best_subject = max(marks, key=marks.get)
    weakest_subject = min(marks, key=marks.get)
    weak_subjects = [sub for sub, score in marks.items() if score < WEAK_MARKS_LIMIT]
    return best_subject, weakest_subject, weak_subjects


def find_reasons(student, metrics):
    """Identify analytical reasons influencing student performance."""
    reasons = []
    marks = student["marks"]
    best_sub, worst_sub, weak_subs = find_strong_weak(marks)

    if student["attendance"] < LOW_ATTENDANCE_LIMIT:
        reasons.append(f"Low attendance ({student['attendance']}%) has impacted conceptual consistency.")

    if metrics["percentage"] < student["previous"]:
        diff_prev = round(student["previous"] - metrics["percentage"], 2)
        reasons.append(f"Academic score declined by {diff_prev}% compared to previous term.")

    if len(weak_subs) > 0:
        reasons.append(f"Scored below passing threshold in: {', '.join(weak_subs)}.")

    diff_score = marks[best_sub] - marks[worst_sub]
    if diff_score > 30:
        reasons.append(f"High score disparity of {diff_score} marks between {best_sub} and {worst_sub}.")

    if len(reasons) == 0:
        reasons.append("Maintained consistent academic performance and regular attendance.")

    return reasons


def generate_suggestions(student, metrics):
    """Generate personalized recommendations for academic growth."""
    suggestions = []
    marks = student["marks"]
    best_sub, worst_sub, weak_subs = find_strong_weak(marks)

    if student["attendance"] < LOW_ATTENDANCE_LIMIT:
        suggestions.append("Prioritize attending daily lectures to clear fundamentals and maintain eligibility.")

    if len(weak_subs) > 0:
        suggestions.append(f"Dedicate 45 minutes daily to revision and practice problems in {', '.join(weak_subs)}.")

    if metrics["percentage"] < student["previous"]:
        suggestions.append("Analyze recent exam errors, revise older notes, and consult teachers to reverse the decline.")

    if metrics["percentage"] < student["target"]:
        gap = round(student["target"] - metrics["percentage"], 2)
        suggestions.append(f"Bridge the {gap}% target gap by following a structured weekly timetable and solving sample papers.")

    if len(suggestions) == 0:
        suggestions.append("Continue current disciplined revision routines and peer study to sustain high performance.")

    return suggestions


def analyze_student(student, metrics):
    """Produce comprehensive performance evaluation combining all analytical metrics."""
    level = get_performance_level(metrics["percentage"])
    target_res = compare_with_target(student, metrics)
    prev_res = compare_with_previous(student, metrics)
    best_sub, worst_sub, weak_subs = find_strong_weak(student["marks"])
    reasons = find_reasons(student, metrics)
    suggestions = generate_suggestions(student, metrics)

    return {
        "level": level,
        "target_result": target_res,
        "previous_result": prev_res,
        "best_subject": best_sub,
        "weakest_subject": worst_sub,
        "weak_subjects": weak_subs,
        "reasons": reasons,
        "suggestions": suggestions
    }

