from create_database import create_connection


def average_gpa(conn):
    """Overall average grade across all students and courses."""
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(grade) FROM grades;")
    return cursor.fetchone()[0]


def top_students(conn, limit=3):
    """Students with the highest individual grades."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT students.first_name, students.last_name, grades.grade
        FROM students
        JOIN grades ON students.student_id = grades.student_id
        ORDER BY grades.grade DESC
        LIMIT ?;
    """, (limit,))
    return cursor.fetchall()


def students_at_risk(conn, threshold=70):
    """Students with any grade below the threshold."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT students.first_name, students.last_name, courses.course_name, grades.grade
        FROM students
        JOIN grades ON students.student_id = grades.student_id
        JOIN courses ON grades.course_id = courses.course_id
        WHERE grades.grade < ?;
    """, (threshold,))
    return cursor.fetchall()


def average_by_course(conn):
    """Average grade per course, sorted hardest to easiest."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT courses.course_name, AVG(grades.grade) AS avg_grade, COUNT(grades.grade) AS num_grades
        FROM grades
        JOIN courses ON grades.course_id = courses.course_id
        GROUP BY courses.course_name
        ORDER BY avg_grade ASC;
    """)
    return cursor.fetchall()


def hardest_course(conn):
    """The single course with the lowest average grade."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT courses.course_name, AVG(grades.grade) AS avg_grade
        FROM grades
        JOIN courses ON grades.course_id = courses.course_id
        GROUP BY courses.course_name
        HAVING avg_grade IS NOT NULL
        ORDER BY avg_grade ASC
        LIMIT 1;
    """)
    return cursor.fetchone()


if __name__ == "__main__":
    conn = create_connection()

    print("Average GPA:", average_gpa(conn))
    print("\nTop students:")
    for row in top_students(conn):
        print(row)

    print("\nStudents at risk (grade < 70):")
    for row in students_at_risk(conn):
        print(row)

    print("\nAverage grade by course:")
    for row in average_by_course(conn):
        print(row)

    print("\nHardest course:", hardest_course(conn))

    conn.close()