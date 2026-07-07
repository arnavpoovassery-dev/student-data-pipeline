import pandas as pd
import os
from create_database import create_connection, create_tables


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_students(conn):
    df = pd.read_csv(os.path.join(DATA_DIR, "students.csv"))
    df = df.where(pd.notnull(df), None)  # convert NaN -> None

    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO students (student_id, first_name, last_name, major, year, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (row.student_id, row.first_name, row.last_name, row.major, row.year, row.email))
    conn.commit()
    print(f"Loaded {len(df)} students.")


def load_courses(conn):
    df = pd.read_csv(os.path.join(DATA_DIR, "courses.csv"))
    df = df.where(pd.notnull(df), None)

    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO courses (course_id, course_name, credits)
            VALUES (?, ?, ?)
        """, (row.course_id, row.course_name, row.credits))
    conn.commit()
    print(f"Loaded {len(df)} courses.")


def load_grades(conn):
    df = pd.read_csv(os.path.join(DATA_DIR, "grades.csv"))
    df = df.where(pd.notnull(df), None)

    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO grades (grade_id, student_id, course_id, grade)
            VALUES (?, ?, ?, ?)
        """, (row.grade_id, row.student_id, row.course_id, row.grade))
    conn.commit()
    print(f"Loaded {len(df)} grades.")


if __name__ == "__main__":
    conn = create_connection()
    conn.execute("PRAGMA foreign_keys = ON;")
    create_tables(conn)

    load_students(conn)
    load_courses(conn)
    load_grades(conn)

    conn.close()
    print("All data loaded successfully.")