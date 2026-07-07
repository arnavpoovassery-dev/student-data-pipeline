import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "school.db")


def create_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables(conn):
    """Create the students, courses, and grades tables if they don't exist."""
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            major TEXT,
            year INTEGER,
            email TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            credits INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            course_id TEXT NOT NULL,
            grade REAL,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        );
    """)

    conn.commit()
    print("Tables created successfully.")


if __name__ == "__main__":
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    create_tables(conn)
    conn.close()