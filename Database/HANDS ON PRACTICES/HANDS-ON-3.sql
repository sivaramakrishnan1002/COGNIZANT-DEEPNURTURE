
#HANDS ON 3
#Task 1 (Subqueries)

SELECT student_id,
       COUNT(*) AS total_courses
FROM enrollments
GROUP BY student_id
HAVING COUNT(*) >
(
    SELECT AVG(course_count)
    FROM
    (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) avg_table
);

SELECT c.course_name
FROM courses c
WHERE NOT EXISTS
(
    SELECT *
    FROM enrollments e
    WHERE e.course_id = c.course_id
    AND e.grade <> 'A'
);

SELECT *
FROM professors p
WHERE salary =
(
    SELECT MAX(salary)
    FROM professors
    WHERE department_id = p.department_id
);

SELECT *
FROM
(
    SELECT department_id,
           AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) dept_avg
WHERE avg_salary > 85000;

#Task 2 (Views)

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS student_name,
    d.dept_name,
    COUNT(e.course_id) AS total_courses,
    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),2
    ) AS GPA
FROM students s
LEFT JOIN departments d
ON s.department_id=d.department_id
LEFT JOIN enrollments e
ON s.student_id=e.student_id
GROUP BY s.student_id,d.dept_name;

CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),2
    ) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e
ON c.course_id=e.course_id
GROUP BY c.course_id,c.course_name,c.course_code;

SELECT *
FROM vw_student_enrollment_summary
WHERE GPA > 3;

UPDATE vw_student_enrollment_summary
SET student_name='TEST'
WHERE student_id=1;

DROP VIEW vw_course_stats;

DROP VIEW vw_student_enrollment_summary;

CREATE VIEW vw_cs_students AS
SELECT *
FROM students
WHERE department_id = 1
WITH CHECK OPTION;

#Task 3 (Stored Procedures & Transactions)

DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_date DATE
)
BEGIN

    IF EXISTS(
        SELECT 1
        FROM enrollments
        WHERE student_id=p_student_id
        AND course_id=p_course_id
    )
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Duplicate Enrollment';
    ELSE
        INSERT INTO enrollments
        (student_id,course_id,enrollment_date)
        VALUES
        (p_student_id,p_course_id,p_date);
    END IF;

END$$

DELIMITER ;
CALL sp_enroll_student(1,3,'2025-06-17');

CREATE TABLE department_transfer_log
(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_new_department INT
)
BEGIN

    DECLARE old_dept INT;

    START TRANSACTION;

    SELECT department_id
    INTO old_dept
    FROM students
    WHERE student_id=p_student_id;

    UPDATE students
    SET department_id=p_new_department
    WHERE student_id=p_student_id;

    INSERT INTO department_transfer_log
    (student_id,old_department,new_department)
    VALUES
    (p_student_id,old_dept,p_new_department);

    COMMIT;

END$$

DELIMITER ;
CALL sp_transfer_student(1,2);

START TRANSACTION;

UPDATE students
SET department_id=999
WHERE student_id=1;

ROLLBACK;

SELECT *
FROM students
WHERE student_id=1;

START TRANSACTION;

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)
VALUES
(1,3,CURDATE(),'A');

SAVEPOINT first_insert;

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)
VALUES
(999,3,CURDATE(),'A');

ROLLBACK TO first_insert;

COMMIT;
SELECT *
FROM enrollments
WHERE student_id=1
AND course_id=3;
