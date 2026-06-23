
#HANDS ON 2
#Task 1 (Insert, Update, Delete Data)

INSERT INTO departments (dept_name, head_of_dept, budget)
VALUES
('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
('Electronics', 'Dr. Priya Nair', 620000.00),
('Mechanical', 'Dr. Suresh Iyer', 540000.00),
('Civil', 'Dr. Ananya Sharma', 430000.00);

INSERT INTO students
(first_name, last_name, email, date_of_birth, department_id, enrollment_year)
VALUES
('Arjun', 'Mehta', 'arjun.mehta@college.edu', '2003-04-12', 1, 2022),
('Priya', 'Suresh', 'priya.suresh@college.edu', '2003-07-25', 1, 2022),
('Rohan', 'Verma', 'rohan.verma@college.edu', '2002-11-08', 2, 2021),
('Sneha', 'Patel', 'sneha.patel@college.edu', '2004-01-30', 3, 2023),
('Vikram', 'Das', 'vikram.das@college.edu', '2003-09-14', 1, 2022),
('Kavya', 'Menon', 'kavya.menon@college.edu', '2002-05-17', 2, 2021),
('Aditya', 'Singh', 'aditya.singh@college.edu', '2004-03-22', 4, 2023),
('Deepika', 'Rao', 'deepika.rao@college.edu', '2003-08-09', 1, 2022);

INSERT INTO courses
(course_name, course_code, credits, department_id, max_seats)
VALUES
('Data Structures & Algorithms', 'CS101', 4, 1, 60),
('Database Management Systems', 'CS102', 3, 1, 60),
('Object Oriented Programming', 'CS103', 4, 1, 60),
('Circuit Theory', 'EC101', 3, 2, 60),
('Thermodynamics', 'ME101', 3, 3, 60);

INSERT INTO enrollments
(student_id, course_id, enrollment_date, grade)
VALUES
(1, 1, '2022-07-01', 'A'),
(1, 2, '2022-07-01', 'B'),
(2, 1, '2022-07-01', 'B'),
(2, 3, '2022-07-01', 'A'),
(3, 4, '2021-07-01', 'A'),
(4, 5, '2023-07-01', NULL),
(5, 1, '2022-07-01', 'C'),
(5, 2, '2022-07-01', 'A'),
(6, 4, '2021-07-01', 'B'),
(7, 5, '2023-07-01', NULL),
(8, 1, '2022-07-01', 'A'),
(8, 3, '2022-07-01', 'B');

INSERT INTO professors
(prof_name, email, department_id, salary)
VALUES
('Dr. Anand Krishnan', 'anand.k@college.edu', 1, 95000),
('Dr. Meena Pillai', 'meena.p@college.edu', 1, 88000),
('Dr. Sunil Rajan', 'sunil.r@college.edu', 2, 82000),
('Dr. Latha Gopal', 'latha.g@college.edu', 3, 79000),
('Dr. Kartik Bose', 'kartik.b@college.edu', 4, 76000);

INSERT INTO students
(first_name,last_name,email,date_of_birth,department_id,enrollment_year)
VALUES
('Siva','Krishnan','siva.krishnan@college.edu','2003-06-10',1,2022),
('Rahul','Kumar','rahul.kumar@college.edu','2003-08-15',2,2023);

SELECT COUNT(*) AS total_students
FROM students;

SELECT *
FROM enrollments
WHERE student_id=5
AND course_id=1;

UPDATE enrollments
SET grade='B'
WHERE student_id=5
AND course_id=1;

SELECT *
FROM enrollments
WHERE student_id=5
AND course_id=1;

SELECT *
FROM enrollments
WHERE grade IS NULL;

DELETE FROM enrollments
WHERE grade IS NULL;

SELECT *
FROM enrollments
WHERE grade IS NULL;

SELECT COUNT(*) AS total_students
FROM students;

SELECT COUNT(*) AS total_enrollments
FROM enrollments;

#Task 2 (Single Table Queries)
SELECT *
FROM students
WHERE enrollment_year = 2022
ORDER BY last_name ASC;

SELECT *
FROM courses
WHERE credits > 3
ORDER BY credits DESC;

SELECT *
FROM professors
WHERE salary BETWEEN 80000 AND 95000;

SELECT *
FROM students
WHERE email LIKE '%@college.edu';

SELECT enrollment_year,
COUNT(*) AS total_students
FROM students
GROUP BY enrollment_year;

#Task 3 (Multi-Table JOINs)

SELECT
    CONCAT(s.first_name,' ',s.last_name) AS student_name,
    d.dept_name
FROM students s
JOIN departments d
ON s.department_id = d.department_id;

SELECT
    CONCAT(s.first_name,' ',s.last_name) AS student_name,
    c.course_name,
    e.grade
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
JOIN courses c
ON e.course_id = c.course_id;

SELECT
    s.student_id,
    s.first_name,
    s.last_name
FROM students s
LEFT JOIN enrollments e
ON s.student_id = e.student_id
WHERE e.student_id IS NULL;

SELECT
    c.course_name,
    COUNT(e.student_id) AS total_students
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id,c.course_name;

SELECT
    d.dept_name,
    p.prof_name,
    p.salary
FROM departments d
LEFT JOIN professors p
ON d.department_id = p.department_id;

#Task 4 (Aggregations & Grouping)

SELECT
    c.course_name,
    COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id,c.course_name;

SELECT
    d.dept_name,
    ROUND(AVG(p.salary),2) AS avg_salary
FROM professors p
JOIN departments d
ON p.department_id = d.department_id
GROUP BY d.dept_name;

SELECT *
FROM departments
WHERE budget > 600000;

SELECT
    e.grade,
    COUNT(*) AS total_students
FROM enrollments e
JOIN courses c
ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade;

SELECT
    e.grade,
    COUNT(*) AS total_students
FROM enrollments e
JOIN courses c
ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade;

SELECT
    d.dept_name,
    COUNT(s.student_id) AS total_students
FROM students s
JOIN departments d
ON s.department_id = d.department_id
GROUP BY d.dept_name
HAVING COUNT(s.student_id) > 2;
