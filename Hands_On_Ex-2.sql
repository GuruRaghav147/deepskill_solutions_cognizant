-- TASK 1
use college_db;
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Hari','Krishna','hari.krishna@college.edu','2004-12-26',2,2021);
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Ram','Raja','ram.raja@college.edu','2003-01-12',2,2022);
UPDATE enrollments set grade='B' where student_id=5 and course_id=1;
DELETE FROM enrollments where GRADE IS NULL;
select count(*) from enrollments;
select count(*) students;
select count(*) from enrollments;
SELECT * FROM enrollments WHERE grade IS NULL;
-- TASK 2
use college_db;
select * FROM students where enrollment_year=2022 order by last_name;
select * from courses where credits>3 order by credits desc;
select prof_name from professors where salary between 80000 and 95000;
select first_name,last_name from students where email like '%@college.edu';
select enrollment_year, count(*) as total_students from students group by enrollment_year;
-- TASK 3
select CONCAT(s.first_name,'',s.last_name) as fullname, d.dept_name from students s join departments d 
on s.department_id=d.department_id;
select CONCAT(s.first_name,'',s.last_name) as fullname, c.course_name, s.enrollment_year from students s join courses c on s.department_id=c.department_id
join enrollments e on s.student_id=e.student_id;
SELECT s.*
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.student_id IS NULL;
SELECT c.course_id, c.course_name, COUNT(e.student_id) AS total_students
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;
SELECT d.dept_name, p.prof_name, p.salary
FROM departments d
LEFT JOIN professors p ON d.department_id = p.department_id;
-- TASK 4
use college_db;
SELECT 
    c.course_name, 
    COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
JOIN enrollments e ON c.course_id = e.course_id
GROUP BY course_name;
select d.dept_name ,round(avg(p.salary),2) as avg_salary 
from professors p join departments d group by d.dept_name;
SELECT dept_name
FROM departments
WHERE budget > 600000;
SELECT 
    e.grade, 
    COUNT(*) AS grade_count
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade;
SELECT dept_name
FROM departments
JOIN enrollments ON .course_id = enrollments.course_id
GROUP BY department_name
HAVING COUNT(DISTINCT enrollments.student_id) > 2;
SELECT d.dept_name
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
JOIN departments d ON c.department_id = d.department_id
GROUP BY d.department_id, d.dept_name
HAVING COUNT(DISTINCT e.student_id) > 2;