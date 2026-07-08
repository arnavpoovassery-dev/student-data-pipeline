# Student Performance Data Pipeline

A Python + SQL ETL pipeline that loads student, course, and grade data from CSV files into a relational SQLite database, runs SQL queries to analyze academic performance, and automatically generates report files.

## What it does

- Imports CSV files (students, courses, grades) into a SQLite database
- Cleans missing values during import
- Runs SQL queries using JOIN, GROUP BY, HAVING, and aggregate functions
- Automatically generates CSV reports: honor roll, at-risk students, and course statistics
- Handles missing files and bad data (e.g. a grade referencing a student that doesn't exist) without crashing

## Tech stack

Python, SQLite, Pandas, Git

## Project structure
```
student-data-pipeline/
├── data/               # input CSV files
├── database/           # generated SQLite database (not tracked in git)
├── reports/            # generated report CSVs (not tracked in git)
├── src/
│   ├── create_database.py   # defines schema (tables, primary/foreign keys)
│   ├── load_data.py         # reads CSVs, cleans data, inserts into SQLite
│   ├── queries.py           # SQL queries: SELECT, JOIN, GROUP BY, HAVING, UPDATE, DELETE
│   └── reports.py           # runs queries, writes results to CSV reports
├── requirements.txt
└── README.md
```

## How to run it
```
pip install -r requirements.txt
py src/create_database.py
py src/load_data.py
py src/queries.py
py src/reports.py
```

This will create `database/school.db`, load the sample CSVs into it, print query results to the terminal, and generate report files in `reports/`.

## Database schema

**students** — student_id (PK), first_name, last_name, major, year, email
**courses** — course_id (PK), course_name, credits
**grades** — grade_id (PK), student_id (FK), course_id (FK), grade

`grades` connects `students` and `courses` through foreign keys, which is what makes JOIN queries possible.

## Example queries

- Average GPA across all students
- Top students by grade
- Students at risk of failing (grade below 70)
- Average grade per course, sorted hardest to easiest
- Honor roll and at-risk reports generated automatically as CSVs

## What I learned

This was my first real project using SQL beyond just reading about syntax. Working through it, I got comfortable with:
- Designing a normalized schema with primary and foreign keys
- Writing SELECT, INSERT, UPDATE, DELETE, and JOIN queries
- The difference between WHERE and HAVING (WHERE filters rows before grouping, HAVING filters after)
- Why parameterized queries (`?` placeholders) matter for security, not just convenience
- Handling messy real-world data (missing values, bad foreign keys) without letting the whole pipeline crash