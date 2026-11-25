"""Authentication module to verify application access."""

APP_PASSWORD = "python@2026"
MAX_ATTEMPTS = 3


def check_password(entered_password):
    """Check whether the provided password matches the application password."""
    return entered_password == APP_PASSWORD


def authenticate():
    """Prompt the user for password authentication with up to three attempts."""
    print("=" * 66)
    print("                 SECURITY AUTHENTICATION REQUIRED                 ")
    print("=" * 66)

    attempts = 0
    while attempts < MAX_ATTEMPTS:
        remaining = MAX_ATTEMPTS - attempts
        user_pass = input(f"Enter application password (Attempts remaining: {remaining}): ").strip()

        if check_password(user_pass):
            print("\nAccess Granted! Welcome to Student Performance Analyzer.\n")
            return True

        attempts = attempts + 1
        if attempts < MAX_ATTEMPTS:
            print("Incorrect password. Please try again.\n")
        else:
            print("\nMaximum authentication attempts exceeded. Access Denied.")
            return False

    return False

