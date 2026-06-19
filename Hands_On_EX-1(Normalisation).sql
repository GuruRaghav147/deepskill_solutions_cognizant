-- 1NF Normalisation check (6)
SELECT student_id, first_name, email 
FROM students 
WHERE email LIKE '%,%' 
   OR first_name LIKE '%,%';
   
-- 2NF Normalisation check(7)
SELECT student_id, course_id, COUNT(*) as enrollment_count
FROM enrollments
GROUP BY student_id, course_id
HAVING COUNT(*) > 1;

-- 3NF Normalisation check(8)
SELECT student_id, count(distinct department_id) as structural_anomalies
FROM students
GROUP BY student_id
HAVING count(distinct department_id) > 1;
-- 9
-- 3NF ANALYSIS: The 'enrollments' table is in 3NF.
-- 1. It satisfies 2NF because it uses a single-column primary key (enrollment_id), eliminating partial dependencies.
-- 2. Non-key attributes (student_id, course_id, enrollment_date, grade) depend strictly on enrollment_id.
-- 3. There are no transitive dependencies, as no non-key attribute determines another non-key attribute.
-- Conclusion: The structure is optimal and free of 3NF structural anomalies.

-- ALTER COMMANDS
-- 10
ALTER TABLE STUDENTS
ADD COLUMN phone_number varchar(15);
-- 11
ALTER TABLE courses
ADD COLUMN max_seats int default 60;
-- 12
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade CHECK(grade in ('A','B','C','D','E','F') 
OR grade is NULL);
-- 13
ALTER TABLE departments
CHANGE column hod_name head_of_dept varchar(100);
-- 14
ALTER TABLE students
drop column phone_number;
select * from departments;

