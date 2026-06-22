# =================================================================================
# TASK 3 DOCUMENTATION: ORM N+1 RESOLUTION VIA EAGER LOADING
# =================================================================================
# 87. Baseline Analysis (Step 84 without modifications):
#     * When executing `session.query(Enrollment).all()`, SQLAlchemy issues 1 initial 
#       query to fetch all enrollment rows.
#     * As the code loops through the rows and touches `e.student.first_name` and 
#       `e.course.course_name`, SQLAlchemy lazily issues a separate SELECT query 
#       for EVERY individual row to pull the related student and course details.
#     * Total Baseline SQL Log Lines: 1 + (2 * N) queries. (9 queries for 4 enrollments).
#
# 89 & 90. Eager Loaded Analysis (With joinedload):
#     * After adding `.options(joinedload(...))`, the ORM modifies the backend SQL execution 
#       to automatically inject LEFT OUTER JOIN statements into the primary query.
#     * Total Eager Loaded SQL Log Lines: Exactly 1 single, optimized SQL query.
#     * Performance Gains: Drastically cuts application latency and eliminates 
#       excessive database round-trips.
# =================================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,joinedload
from datetime import date
# Import the classes and Base from your models.py file
from models import engine, Department, Student, Course, Enrollment

# 80. Open a Session using sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

try:
    print("\n--Running CRUD Operations--\n")

    # 81.INSERT: Adding 3 Departments and 5 Students
    cs_dept = Department(department_name="Computer Science", building="Engineering Hall")
    math_dept = Department(department_name="Mathematics", building="Science Center")
    bio_dept = Department(department_name="Biology", building="Darwin Lab")
    
    session.add_all([cs_dept, math_dept, bio_dept])
    session.flush()

    # Creating Students
    s1 = Student(first_name="Alice", last_name="Smith", email="alice@example.com", enrollment_date=date(2022, 9, 1), department=cs_dept)
    s2 = Student(first_name="Bob", last_name="Jones", email="bob@example.com", enrollment_date=date(2022, 9, 1), department=cs_dept)
    s3 = Student(first_name="Charlie", last_name="Brown", email="charlie@example.com", enrollment_date=date(2023, 9, 1), department=math_dept)
    s4 = Student(first_name="Diana", last_name="Prince", email="diana@example.com", enrollment_date=date(2023, 9, 1), department=bio_dept)
    s5 = Student(first_name="Evan", last_name="Wright", email="evan@example.com", enrollment_date=date(2024, 9, 1), department=cs_dept)

    session.add_all([s1, s2, s3, s4, s5])
    session.commit()
    print("Step 81: 3 Departments and 5 Students inserted successfully.")

    # 82. INSERT: Add 3 Courses and 4 Enrollments
    python_course = Course(course_code="CS101", course_name="Intro to Python", credits=4)
    calculus_course = Course(course_code="MATH201", course_name="Calculus I", credits=4)
    genetics_course = Course(course_code="BIO301", course_name="Genetics", credits=3)

    session.add_all([python_course, calculus_course, genetics_course])
    session.flush()

    # Create Enrollments
    e1 = Enrollment(student=s1, course=python_course, semester="Fall 2026", grade="A")
    e2 = Enrollment(student=s2, course=python_course, semester="Fall 2026", grade="B")
    e3 = Enrollment(student=s3, course=calculus_course, semester="Fall 2026", grade="A")
    e4 = Enrollment(student=s4, course=genetics_course, semester="Fall 2026", grade="C")

    session.add_all([e1, e2, e3, e4])
    session.commit()
    print("3 Courses and 4 Enrollments inserted successfully.")

    # 83. READ: Query all students in department 'Computer Science'
    print("\n Students in Computer Science:")
    cs_students = (
        session.query(Student)
        .join(Department)
        .filter(Department.department_name == "Computer Science")
        .all()
    )
    for student in cs_students:
        print(f"- {student.first_name} {student.last_name} ({student.email})")

    # 84. READ: Query all enrollments and print student + course name
    # Steps 88 & 89: Optimized Enrollment Records (Using joinedload to fix N+1)
    print("\nStep 84 (Optimized via 88 & 89): All Enrollment Records:")
    
    # This forces SQLAlchemy to fetch everything in ONE unified SQL query using JOINs
    enrollments = (
        session.query(Enrollment)
        .options(
            joinedload(Enrollment.student), 
            joinedload(Enrollment.course)
        )
        .all()
    )

    for e in enrollments:
        # No extra hidden background queries are fired during this loop!
        print(f"Student: {e.student.first_name} {e.student.last_name} | Course: {e.course.course_name} | Grade: {e.grade}")
    print("\n All Enrollment Records:")
    enrollments = session.query(Enrollment).all()
    for e in enrollments:
        print(f"Student: {e.student.first_name} {e.student.last_name} | Course: {e.course.course_name} | Grade: {e.grade}")

    # 85. UPDATE: Find a specific student by email and update registration data
    print("\n: Updating student record...")
    student_to_update = session.query(Student).filter(Student.email == "alice@example.com").first()
    if student_to_update:
        # Note: Your model has enrollment_date, updating it to a new date object
        student_to_update.enrollment_date = date(2022, 10, 1)
        session.commit()
        print(f"Successfully updated enrollment date for {student_to_update.first_name}.")

    # 86. DELETE: Remove an enrollment record and verify

    print("\n Deleting an enrollment record...")
    enrollment_to_delete = session.query(Enrollment).filter(Enrollment.student_id == s2.student_id).first()
    
    if enrollment_to_delete:
        session.delete(enrollment_to_delete)
        session.commit()
        print("Enrollment record deleted.")

    # Verification Query
    verification = session.query(Enrollment).filter(Enrollment.student_id == s2.student_id).first()
    if verification is None:
        print("Verification: Record is verified deleted from the database.")
    else:
        print("Verification Failed: Record still exists.")

except Exception as ex:
    session.rollback()
    print(f"An error occurred: {ex}")

finally:
    session.close()
    print("\nSession closed safely.")

# 91. BONUS: Django ORM Equivalent (Theoretical Reference)
# If this project were built using Django ORM instead of SQLAlchemy,
# the exact same N+1 optimization would be achieved using this syntax:
"""
from myapp.models import Enrollment

# select_related forces an immediate SQL JOIN on foreign key fields
enrollments = Enrollment.objects.select_related('student', 'course').all()

for e in enrollments:
    print(f"Student: {e.student.first_name} {e.student.last_name} | Course: {e.course.course_name}")
"""
