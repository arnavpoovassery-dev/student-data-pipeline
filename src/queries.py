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

def update_grade(conn, grade_id, new_grade):
    """Correct a specific grade, e.g. after a regrade request."""
    cursor = conn.cursor()

    cursor.execute("SELECT grade FROM grades WHERE grade_id = ?;", (grade_id,))
    existing = cursor.fetchone()
    if existing is None:
        print(f"No grade found with grade_id={grade_id}")
        return

    cursor.execute("""
        UPDATE grades
        SET grade = ?
        WHERE grade_id = ?;
    """, (new_grade, grade_id))
    conn.commit()
    print(f"Updated grade_id={grade_id}: {existing[0]} -> {new_grade}")


def remove_grade(conn, grade_id):
    """Remove a grade entry, e.g. a student withdrew from the course."""
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM grades WHERE grade_id = ?;", (grade_id,))
    existing = cursor.fetchone()
    if existing is None:
        print(f"No grade found with grade_id={grade_id}")
        return

    cursor.execute("DELETE FROM grades WHERE grade_id = ?;", (grade_id,))
    conn.commit()
    print(f"Deleted grade_id={grade_id}: {existing}")


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

    print("\n--- UPDATE example ---")
    update_grade(conn, grade_id=5, new_grade=65)  # Carlos's CS101 grade, regraded from 58 to 65

    print("\n--- DELETE example ---")
    remove_grade(conn, grade_id=10)  # Frank withdrew from MATH19

    conn.close()