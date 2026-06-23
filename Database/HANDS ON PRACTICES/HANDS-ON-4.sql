
#HANDS ON 4
#Task 1 (Query Performance Analysis using EXPLAIN)

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
JOIN courses c
ON e.course_id = c.course_id
WHERE s.enrollment_year = 2022;

EXPLAIN
SELECT *
FROM students
WHERE department_id = 1;

EXPLAIN
SELECT *
FROM students
WHERE email = 'arjun.mehta@college.edu';

#Task 2 (Indexes)
CREATE INDEX idx_enrollment_year
ON students(enrollment_year);
SHOW INDEX FROM students;

CREATE UNIQUE INDEX idx_student_course
ON enrollments(student_id, course_id);
SHOW INDEX FROM enrollments;

CREATE INDEX idx_course_code
ON courses(course_code);
SHOW INDEX FROM courses;

CREATE INDEX idx_salary
ON professors(salary);

EXPLAIN
SELECT *
FROM students
WHERE enrollment_year = 2022;

#Task 3 (Performance Comparison)

SELECT *
FROM students
WHERE enrollment_year = 2022;

SELECT *
FROM students
WHERE first_name = 'Arjun';

EXPLAIN
SELECT *
FROM students
WHERE enrollment_year = 2022;

EXPLAIN
SELECT *
FROM students
WHERE first_name = 'Arjun';


