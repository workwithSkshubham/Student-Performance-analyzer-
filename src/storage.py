"""Module for managing CSV data storage using pandas."""

import os
import pandas as pd

_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SRC_DIR)
CSV_FILE_PATH = os.path.join(_PROJECT_ROOT, "data", "students.csv")
CSV_COLUMNS = [
    "roll_no", "name", "class_name", "maths", "physics",
    "chemistry", "english", "cs", "attendance", "target", "previous"
]


def save_data(df):
    """Save the pandas DataFrame to the CSV storage file."""
    try:
        os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)
        df.to_csv(CSV_FILE_PATH, index=False)
        return True
    except Exception as err:
        print(f"Error saving data to CSV: {err}")
        return False


def initialize_data():
    """Initialize the CSV file with original records if not present."""
    try:
        with open(CSV_FILE_PATH, "r", encoding="utf-8") as file_handle:
            content = file_handle.read().strip()
            if not content:
                raise FileNotFoundError
    except (FileNotFoundError, OSError):
        initial_data = {
            "roll_no": [101, 102, 103, 104, 105, 106],
            "name": ["Rahul", "Priya", "Amit", "Sneha", "Karan", "Neha"],
            "class_name": ["Sem 3", "Sem 3", "Sem 3", "Sem 3", "Sem 3", "Sem 3"],
            "maths": [90, 78, 45, 95, 60, 70],
            "physics": [55, 82, 38, 90, 35, 65],
            "chemistry": [75, 70, 50, 88, 42, 72],
            "english": [80, 88, 60, 92, 55, 75],
            "cs": [85, 91, 55, 97, 48, 68],
            "attendance": [92.0, 85.0, 68.0, 96.0, 72.0, 80.0],
            "target": [80.0, 85.0, 65.0, 90.0, 60.0, 75.0],
            "previous": [70.0, 80.0, 58.0, 88.0, 62.0, 70.0]
        }
        df = pd.DataFrame(initial_data)
        save_data(df)


def load_data():
    """Load student records from the CSV file into a pandas DataFrame."""
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        initialize_data()
        try:
            return pd.read_csv(CSV_FILE_PATH)
        except Exception:
            return pd.DataFrame(columns=CSV_COLUMNS)
    except Exception as err:
        print(f"Error reading CSV data: {err}")
        return pd.DataFrame(columns=CSV_COLUMNS)


def row_to_student(row):
    """Convert a single CSV row series into a structured student dictionary."""
    maths_val = float(row["maths"])
    phys_val = float(row["physics"])
    chem_val = float(row["chemistry"])
    eng_val = float(row["english"])
    cs_val = float(row["cs"])

    student = {
        "name": str(row["name"]),
        "roll_no": int(row["roll_no"]),
        "class": str(row["class_name"]),
        "marks": {
            "Maths": int(maths_val) if maths_val.is_integer() else maths_val,
            "Physics": int(phys_val) if phys_val.is_integer() else phys_val,
            "Chemistry": int(chem_val) if chem_val.is_integer() else chem_val,
            "English": int(eng_val) if eng_val.is_integer() else eng_val,
            "CS": int(cs_val) if cs_val.is_integer() else cs_val
        },
        "attendance": float(row["attendance"]),
        "target": float(row["target"]),
        "previous": float(row["previous"])
    }
    return student


def get_all_students():
    """Retrieve all student records as a list of structured dictionaries."""
    df = load_data()
    if df.empty:
        return []
    students = []
    for _, row in df.iterrows():
        students.append(row_to_student(row))
    return students


def get_student_by_roll(roll_no):
    """Find and return a student dictionary matching the roll number, or None."""
    df = load_data()
    if df.empty or "roll_no" not in df.columns:
        return None
    try:
        target_roll = int(roll_no)
        matches = df[df["roll_no"].astype(int) == target_roll]
    except Exception:
        matches = df[df["roll_no"] == roll_no]
    if matches.empty:
        return None
    row = matches.iloc[0]
    return row_to_student(row)


def add_student(student):
    """Add a new student record to CSV if roll number is unique."""
    df = load_data()
    roll_val = int(student["roll_no"])
    if not df.empty and "roll_no" in df.columns:
        try:
            if roll_val in df["roll_no"].astype(int).values:
                print(f"Error: Roll number {roll_val} already exists.")
                return False
        except Exception:
            if roll_val in df["roll_no"].values:
                print(f"Error: Roll number {roll_val} already exists.")
                return False

    marks = student.get("marks", {})
    new_row = {
        "roll_no": roll_val,
        "name": str(student["name"]),
        "class_name": str(student.get("class", student.get("class_name", ""))),
        "maths": marks.get("Maths", marks.get("maths", student.get("maths", 0))),
        "physics": marks.get("Physics", marks.get("physics", student.get("physics", 0))),
        "chemistry": marks.get("Chemistry", marks.get("chemistry", student.get("chemistry", 0))),
        "english": marks.get("English", marks.get("english", student.get("english", 0))),
        "cs": marks.get("CS", marks.get("cs", student.get("cs", 0))),
        "attendance": float(student["attendance"]),
        "target": float(student["target"]),
        "previous": float(student["previous"])
    }
    new_df = pd.DataFrame([new_row])
    updated_df = pd.concat([df, new_df], ignore_index=True)
    return save_data(updated_df)


def update_student(roll_no, student):
    """Update an existing student record in the CSV file."""
    df = load_data()
    if df.empty or "roll_no" not in df.columns:
        return False

    try:
        target_roll = int(roll_no)
        matches = df[df["roll_no"].astype(int) == target_roll]
    except Exception:
        matches = df[df["roll_no"] == roll_no]

    if matches.empty:
        return False

    idx = matches.index[0]
    df.at[idx, "name"] = str(student["name"])
    df.at[idx, "class_name"] = str(student.get("class", student.get("class_name", df.at[idx, "class_name"])))

    marks = student.get("marks", {})
    for sub in ["Maths", "Physics", "Chemistry", "English", "CS"]:
        col = sub.lower()
        val = marks.get(sub, marks.get(col, student.get(col, df.at[idx, col])))
        df.at[idx, col] = val

    df.at[idx, "attendance"] = float(student["attendance"])
    df.at[idx, "target"] = float(student["target"])
    df.at[idx, "previous"] = float(student["previous"])
    return save_data(df)


def delete_student(roll_no):
    """Delete a student record from the CSV file by roll number."""
    df = load_data()
    if df.empty or "roll_no" not in df.columns:
        return False

    try:
        target_roll = int(roll_no)
        matches = df[df["roll_no"].astype(int) == target_roll]
        if matches.empty:
            return False
        df = df[df["roll_no"].astype(int) != target_roll]
        return save_data(df)
    except Exception:
        matches = df[df["roll_no"] == roll_no]
        if matches.empty:
            return False
        df = df[df["roll_no"] != roll_no]
        return save_data(df)


