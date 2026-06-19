-- TASK 1
use college_db;
-- 35
SELECT s.student_id, s.first_name, s.last_name, COUNT(e.course_id) AS enrollment_count
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) > (
    -- Non-correlated subquery: Calculates the overall avrg enrollments per student
    SELECT AVG(student_enrollment_counts.course_count)
    FROM (
        SELECT COUNT(course_id) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) AS student_enrollment_counts
);
-- 36
SELECT c.course_id, c.course_name, c.course_code
FROM courses c
WHERE EXISTS (
    -- Ensures the course actually has at least one enrollment
    SELECT * FROM enrollments e WHERE e.course_id = c.course_id
)
AND NOT EXISTS (
    -- Correlated subquery: Checks if there are any grades that are NOT 'A'
    SELECT *
    FROM enrollments e 
    WHERE e.course_id = c.course_id 
      AND (e.grade != 'A' OR e.grade IS NULL)
);
-- 37
SELECT p1.professor_id, p1.prof_name, p1.department_id, p1.salary
FROM professors p1
WHERE p1.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p1.department_id
);
-- 38
SELECT d.department_id, d.dept_name, dept_averages.avg_salary
FROM departments d
JOIN (
    -- Derived table
    SELECT department_id, AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) AS dept_averages ON d.department_id = dept_averages.department_id
WHERE dept_averages.avg_salary > 85000.00;
-- TASK 2
-- 39
CREATE VIEW vw_student_enrollment_summary AS
SELECT 
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name AS department,
    COUNT(e.course_id) AS courses_enrolled,
    AVG(CASE 
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'D' THEN 1
        WHEN e.grade = 'F' THEN 0
        ELSE NULL 
    END) AS gpa
FROM students s
LEFT JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;
-- 40
CREATE VIEW vw_course_stats AS
SELECT 
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    AVG(CASE 
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'D' THEN 1
        WHEN e.grade = 'F' THEN 0
        ELSE NULL 
    END) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;
-- 41
select full_name,department,courses_enrolled,gpa 
from vw_student_enrollment_summary where gpa>3.0;
-- 42
-- multitable view is not updatable
update vw_student_enrollment_summary 
set department='Computer Science'
where full_name='Angel John';
-- 43
DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

-- Recreate vw_student_enrollment_summary as an updatable single-table subset view
CREATE VIEW vw_student_enrollment_summary AS
SELECT student_id, first_name, last_name, email, enrollment_year, department_id
FROM students
WHERE enrollment_year >= 2020
WITH CHECK OPTION;
-- Task 3
-- 44
DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN
    DECLARE v_exists INT DEFAULT 0;
    SELECT COUNT(*) INTO v_exists
    FROM enrollments
    WHERE student_id = p_student_id AND course_id = p_course_id;
    IF v_exists = 0 THEN
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (p_student_id, p_course_id, p_enrollment_date);
        SELECT 'Enrollment successful.' AS status_message;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate enrollment error: Student is already enrolled in this course.';
    END IF;
END$$

DELIMITER ;
-- 45
CREATE TABLE department_transfer_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    old_department_id INT,
    new_department_id INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
-- 46
DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_new_dept_id INT
)
BEGIN
    DECLARE v_old_dept_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Transaction failed. Changes rolled back.' AS status_message;
    END;
    START TRANSACTION;
    SELECT department_id INTO v_old_dept_id 
    FROM students 
    WHERE student_id = p_student_id;
    UPDATE students 
    SET department_id = p_new_dept_id 
    WHERE student_id = p_student_id;
    INSERT INTO department_transfer_log (student_id, old_department_id, new_department_id)
    VALUES (p_student_id, v_old_dept_id, p_new_dept_id);
    COMMIT;
    SELECT 'Transfer completed and logged successfully.' AS status_message;
END$$
DELIMITER ;
-- 47
-- Assuming department 999999 does not exist
CALL sp_transfer_student(1, 999999);
SELECT student_id, department_id FROM students WHERE student_id = 1;
SELECT * FROM department_transfer_log WHERE student_id = 1;
