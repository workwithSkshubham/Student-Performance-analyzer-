"""Module for handling user input and student data validation."""

SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "CS"]
MAX_MARKS = 100


def read_number(message, low, high):
    """Prompt the user for a numeric value within a specific range."""
    while True:
        user_input = input(message).strip()
        try:
            val = float(user_input)
            if low <= val <= high:
                return val
            print(f"Error: Value must be between {low} and {high}.")
        except ValueError:
            print("Error: Invalid numeric input. Please enter a valid number.")


def get_student_from_user():
    """Collect student details from user input and return a structured dictionary."""
    print("\n--- Enter Student Details ---")
    name = ""
    while not name:
        name = input("Enter Student Name: ").strip()
        if not name:
            print("Error: Student name cannot be empty.")

    roll_val = read_number("Enter Roll Number (1 - 999999): ", 1, 999999)
    roll_no = int(roll_val)

    class_name = ""
    while not class_name:
        class_name = input("Enter Class/Semester (e.g., Sem 3): ").strip()
        if not class_name:
            print("Error: Class cannot be empty.")

    print(f"\nEnter Marks for 5 Subjects (Max Marks: {MAX_MARKS}):")
    marks = {}
    for subject in SUBJECTS:
        score_val = read_number(f"  Marks in {subject} (0 - {MAX_MARKS}): ", 0, MAX_MARKS)
        marks[subject] = int(score_val) if score_val.is_integer() else round(score_val, 2)

    print("\nEnter Attendance and Performance Targets:")
    attendance = round(read_number("  Attendance Percentage (0 - 100): ", 0, 100), 2)
    target = round(read_number("  Target Percentage (0 - 100): ", 0, 100), 2)
    previous = round(read_number("  Previous Performance Percentage (0 - 100): ", 0, 100), 2)

    student = {
        "name": name,
        "roll_no": roll_no,
        "class": class_name,
        "marks": marks,
        "attendance": attendance,
        "target": target,
        "previous": previous
    }
    return student

