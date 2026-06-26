from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import declarative_base, relationship

#Task 1
# 76.
# Using 'college_db_orm' as requested to keep it separate from the raw SQL schema
DATABASE_URL = "postgresql://username:password@localhost:5532/college_db_orm"
# For MySQL, use: "mysql+pymysql://username:password@localhost:3306/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# 77&78. Defining ORM Model Classes & Relationships

class Department(Base):
    __tablename__ = 'departments'
    
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(100), nullable=False)
    building = Column(String(50))
    
    # Relationship: One department can have many students
    students = relationship("Student", back_populates="department")


class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    enrollment_date = Column(Date)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    
    # 78. Relationship: Many-to-One to Department
    department = relationship("Department", back_populates="students")
    # Relationship: One student can have many enrollments
    enrollments = relationship("Enrollment", back_populates="student")


class Course(Base):
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(10), unique=True, nullable=False)
    course_name = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False)
    
    # Relationship: One course can have many enrollments
    enrollments = relationship("Enrollment", back_populates="course")


class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    semester = Column(String(10), nullable=False)
    grade = Column(String(2))  # e.g., 'A', 'B+', etc.
    
    # 78. Relationships: Many-to-One to both Student and Course
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Professor(Base):
    __tablename__ = 'professors'
    
    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'))


# 79. Auto-create tables in the database
if __name__ == "__main__":
    print("Creating tables in college_db_orm...")
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
