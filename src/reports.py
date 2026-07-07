import os
import pandas as pd
from create_database import create_connection

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


def honor_roll(conn, threshold=90):
    """Students with any grade at or above the threshold."""
    query = """
        SELECT students.first_name, students.last_name, courses.course_name, grades.grade
        FROM students
        JOIN grades ON students.student_id = grades.student_id
        JOIN courses ON grades.course_id = courses.course_id
        WHERE grades.grade >= ?
        ORDER BY grades.grade DESC;
    """
    df = pd.read_sql_query(query, conn, params=(threshold,))
    df.to_csv(os.path.join(REPORTS_DIR, "honor_roll.csv"), index=False)
    print(f"Wrote honor_roll.csv ({len(df)} rows)")


def at_risk(conn, threshold=70):
    """Students with any grade below the threshold."""
    query = """
        SELECT students.first_name, students.last_name, courses.course_name, grades.grade
        FROM students
        JOIN grades ON students.student_id = grades.student_id
        JOIN courses ON grades.course_id = courses.course_id
        WHERE grades.grade < ?
        ORDER BY grades.grade ASC;
    """
    df = pd.read_sql_query(query, conn, params=(threshold,))
    df.to_csv(os.path.join(REPORTS_DIR, "at_risk.csv"), index=False)
    print(f"Wrote at_risk.csv ({len(df)} rows)")


def course_statistics(conn):
    """Average grade, count, min, and max per course."""
    query = """
        SELECT
            courses.course_name,
            COUNT(grades.grade) AS num_grades,
            AVG(grades.grade) AS avg_grade,
            MIN(grades.grade) AS min_grade,
            MAX(grades.grade) AS max_grade
        FROM courses
        LEFT JOIN grades ON grades.course_id = courses.course_id
        GROUP BY courses.course_name
        ORDER BY avg_grade ASC;
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv(os.path.join(REPORTS_DIR, "course_statistics.csv"), index=False)
    print(f"Wrote course_statistics.csv ({len(df)} rows)")


if __name__ == "__main__":
    conn = create_connection()

    honor_roll(conn)
    at_risk(conn)
    course_statistics(conn)

    conn.close()
    print("All reports generated successfully.")