import pandas as pd
import os
import sqlite3
from create_database import create_connection, create_tables


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_students(conn):
    path = os.path.join(DATA_DIR, "students.csv")
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"ERROR: could not find {path}")
        return
    except pd.errors.EmptyDataError:
        print(f"ERROR: {path} is empty")
        return

    df = df.where(pd.notnull(df), None)

    cursor = conn.cursor()
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO students (student_id, first_name, last_name, major, year, email)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row.student_id, row.first_name, row.last_name, row.major, row.year, row.email))
        except sqlite3.IntegrityError as e:
            print(f"Skipped student_id={row.student_id}: {e}")

    conn.commit()
    print(f"Loaded {len(df)} students.")


def load_courses(conn):
    path = os.path.join(DATA_DIR, "courses.csv")
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"ERROR: could not find {path}")
        return
    except pd.errors.EmptyDataError:
        print(f"ERROR: {path} is empty")
        return

    df = df.where(pd.notnull(df), None)

    cursor = conn.cursor()
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO courses (course_id, course_name, credits)
                VALUES (?, ?, ?)
            """, (row.course_id, row.course_name, row.credits))
        except sqlite3.IntegrityError as e:
            print(f"Skipped course_id={row.course_id}: {e}")

    conn.commit()
    print(f"Loaded {len(df)} courses.")


def load_grades(conn):
    path = os.path.join(DATA_DIR, "grades.csv")
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"ERROR: could not find {path}")
        return
    except pd.errors.EmptyDataError:
        print(f"ERROR: {path} is empty")
        return

    df = df.where(pd.notnull(df), None)

    cursor = conn.cursor()
    inserted = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO grades (grade_id, student_id, course_id, grade)
                VALUES (?, ?, ?, ?)
            """, (row.grade_id, row.student_id, row.course_id, row.grade))
            inserted += 1
        except sqlite3.IntegrityError as e:
            print(f"Skipped grade_id={row.grade_id}: {e}")

    conn.commit()
    print(f"Loaded {inserted} of {len(df)} grades.")


if __name__ == "__main__":
    conn = create_connection()
    conn.execute("PRAGMA foreign_keys = ON;")
    create_tables(conn)

    load_students(conn)
    load_courses(conn)
    load_grades(conn)

    conn.close()
    print("All data loaded successfully.")