"""Introduction screen and welcome banner for the application."""


def show_loading():
    """Display a simple terminal loading bar using loops."""
    print("\nInitializing System Components:")
    for step in range(1, 21):
        bar = "=" * step + " " * (20 - step)
        percent = step * 5
        print(f"\r[{bar}] {percent}% Completed", end="")
    print("\n")


def show_intro():
    """Display the welcome banner, project purpose, and motivational messages."""
    print("=" * 66)
    print("*" + " " * 64 + "*")
    print("*           STUDENT PERFORMANCE ANALYZER SYSTEM               *")
    print("*               Data-Driven Academic Insights                  *")
    print("*" + " " * 64 + "*")
    print("=" * 66)
    print("\nWelcome to the Student Performance Analyzer!")
    print("Designed to help students and mentors evaluate academic progress,")
    print("uncover hidden strengths, and build actionable improvement plans.\n")
    print("-" * 66)
    print("  * Marks don't define your potential.")
    print("  * Understand your performance. Improve your future.")
    print("  * No random guessing. Just data-driven improvement.")
    print("  * TRACK YOUR PROGRESS. FIND YOUR WEAK SPOTS. LEVEL UP.")
    print("-" * 66)
    show_loading()

