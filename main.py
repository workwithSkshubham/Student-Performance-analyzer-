"""Main application controller for Student Performance Analyzer."""

from src.intro import show_intro
from src.auth import authenticate
from src.data_input import get_student_from_user, read_number
from src.storage import (
    initialize_data,
    load_data,
    get_all_students,
    get_student_by_roll,
    add_student
)
from src.calculator import calculate_metrics, class_summary
from src.analyzer import analyze_student
from src.report import build_report, save_report, build_class_report


def show_analysis(student):
    """Calculate metrics, run performance analysis, display, and save report."""
    metrics = calculate_metrics(student)
    analysis = analyze_student(student, metrics)
    report_text = build_report(student, metrics, analysis)
    try:
        print("\n" + report_text)
    except UnicodeEncodeError:
        print("\n" + report_text.encode("ascii", errors="replace").decode("ascii"))
    saved_file = save_report(report_text, student["roll_no"])
    if saved_file:
        print(f"\nReport successfully saved to: {saved_file}")


def print_menu():
    """Display the primary menu options for the user."""
    print("\n" + "=" * 45)
    print("        STUDENT PERFORMANCE ANALYZER         ")
    print("=" * 45)
    print("  [1] Analyze Existing Student")
    print("  [2] Add New Student")
    print("  [3] Class Performance Summary")
    print("  [4] View All Students")
    print("  [5] Search Student by Roll Number")
    print("  [6] Exit")
    print("=" * 45)


def run_app():
    """Initialize data, authenticate user, and execute main menu loop."""
    initialize_data()
    show_intro()

    if not authenticate():
        print("\nAuthentication failed. Exiting system. Goodbye!")
        return

    # Warm load dataset
    load_data()

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            roll_val = read_number("Enter Roll Number to analyze: ", 1, 999999)
            roll_no = int(roll_val)
            student = get_student_by_roll(roll_no)
            if student:
                show_analysis(student)
            else:
                print(f"\nError: No student found with Roll Number {roll_no}.")

        elif choice == "2":
            new_student = get_student_from_user()
            if add_student(new_student):
                print(f"\nStudent '{new_student['name']}' added successfully!")
                show_analysis(new_student)

        elif choice == "3":
            students = get_all_students()
            if not students:
                print("\nNo student records available for class summary.")
            else:
                summary = class_summary(students)
                class_rep = build_class_report(summary)
                print("\n" + class_rep)
                saved_path = save_report(class_rep, "class")
                if saved_path:
                    print(f"\nClass summary report saved to: {saved_path}")

        elif choice == "4":
            df = load_data()
            if df.empty:
                print("\nNo student records found in storage.")
            else:
                display_cols = ["roll_no", "name", "class_name", "attendance"]
                available = [col for col in display_cols if col in df.columns]
                print("\n" + "=" * 55)
                print("                 ALL REGISTERED STUDENTS                 ")
                print("=" * 55)
                print(df[available].to_string(index=False))
                print("=" * 55)

        elif choice == "5":
            roll_val = read_number("Enter Roll Number to search: ", 1, 999999)
            roll_no = int(roll_val)
            student = get_student_by_roll(roll_no)
            if student:
                print("\n" + "-" * 40)
                print(f"Name           : {student['name']}")
                print(f"Roll Number    : {student['roll_no']}")
                print(f"Class/Semester : {student['class']}")
                print(f"Attendance     : {student['attendance']}%")
                print("Marks:")
                for sub, score in student["marks"].items():
                    print(f"  {sub:<12} : {score}/100")
                print(f"Target Goal    : {student['target']}%")
                print(f"Previous Term  : {student['previous']}%")
                print("-" * 40)
            else:
                print(f"\nNo student found with Roll Number {roll_no}.")

        elif choice == "6":
            print("\nThank you for using Student Performance Analyzer. Goodbye!")
            break

        else:
            print("\nInvalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    run_app()
