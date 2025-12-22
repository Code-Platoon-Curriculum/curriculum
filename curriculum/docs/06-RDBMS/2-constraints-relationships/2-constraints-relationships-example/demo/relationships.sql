-- -- ONE - TO - ONE
-- DROP TABLE IF EXISTS employees CASCADE;

-- CREATE TABLE employees(
--     employee_id SERIAL PRIMARY KEY,
--     employee_name VARCHAR(100) NOT NULL
-- );

-- DROP TABLE IF EXISTS social_securities;

-- CREATE TABLE social_securities(
--     ssn_id SERIAL PRIMARY KEY,
--     employee_id INT UNIQUE,
--     ssn VARCHAR(11) UNIQUE NOT NULL,
--     FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
-- );

-- INSERT INTO employees(employee_name) VALUES('Roger');
-- INSERT INTO social_securities(employee_id, ssn) VALUES(1, '222-22-2222');
-- INSERT INTO social_securities(employee_id, ssn) VALUES(1, '333-33-3333')

-- -- MANY - TO - ONE

-- DROP TABLE IF EXISTS universities CASCADE;

-- CREATE TABLE universities(
--     university_id SERIAL PRIMARY KEY,
--     university_name VARCHAR(70) UNIQUE NOT NULL
-- );

-- DROP TABLE IF EXISTS students;

-- CREATE TABLE students(
--     student_id SERIAL PRIMARY KEY,
--     student_name VARCHAR(50) NOT NULL,
--     university_id INT,
--     FOREIGN KEY (university_id) REFERENCES universities(university_id)
-- );

-- INSERT INTO universities(university_name) VALUES('Code Platoon');
-- INSERT INTO students(student_name, university_id) VALUES('Sam', 1);
-- INSERT INTO students(student_name, university_id) VALUES('Jesus', 1);
-- INSERT INTO students(student_name, university_id) VALUES('Hailey', 1);
-- INSERT INTO students(student_name, university_id) VALUES('Jacob', 1);


-- MANY - TO - MANY RELATIONSHIPS
DROP TABLE IF EXISTS students CASCADE;

CREATE TABLE students(
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(50) NOT NULL
);

DROP TABLE IF EXISTS courses CASCADE;

CREATE TABLE courses(
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS course_students;

CREATE TABLE course_students(
    course_students_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

INSERT INTO students(student_name) VALUES('Tristan');
INSERT INTO students(student_name) VALUES('James');
INSERT INTO students(student_name) VALUES('Ryan');
INSERT INTO students(student_name) VALUES('Gary');
INSERT INTO students(student_name) VALUES('Jacob');

INSERT INTO courses(course_name) VALUES('Python');
INSERT INTO courses(course_name) VALUES('JavaScript');

INSERT INTO course_students(student_id, course_id) VALUES(1, 2);
INSERT INTO course_students(student_id, course_id) VALUES(2, 1);
INSERT INTO course_students(student_id, course_id) VALUES(2, 2);
INSERT INTO course_students(student_id, course_id) VALUES(3, 1);
INSERT INTO course_students(student_id, course_id) VALUES(4, 1);
INSERT INTO course_students(student_id, course_id) VALUES(5, 1);
INSERT INTO course_students(student_id, course_id) VALUES(5, 2);