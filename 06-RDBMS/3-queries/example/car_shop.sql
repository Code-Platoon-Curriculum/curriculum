DROP TABLE IF EXISTS department CASCADE;
-- Create Department Table
CREATE TABLE department (
    id SERIAL PRIMARY KEY,
    department_name VARCHAR(50) UNIQUE NOT NULL
);

\COPY department FROM './data/department.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS employees;
-- Create Employees Table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    salary DECIMAL(7, 2) NOT NULL CHECK (salary > 0),
    first_name VARCHAR(50) NOT NULL,
    middle_init CHAR(1),
    last_name VARCHAR(50) NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES department(id),
    CHECK (middle_init IS NULL OR LENGTH(middle_init) = 1)
);

\COPY employees FROM './data/employees.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS services CASCADE;
-- Create Service Table
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name_of_service VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(7, 2) NOT NULL CHECK (price >= 0)
);

\COPY services FROM './data/services.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS driver CASCADE;
-- Create Owner Table
CREATE TABLE driver (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    age INT CHECK (age >= 0)
);

\COPY driver FROM './data/driver.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS car CASCADE;
-- Create Car Table
CREATE TABLE car (
    id SERIAL PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL CHECK (year >= 1900),
    color VARCHAR(20) NOT NULL,
    driver INT,
    FOREIGN KEY (driver) REFERENCES driver(id)
);

\COPY car FROM './data/car.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS plate;
-- Create Plate Table
CREATE TABLE plate (
    id SERIAL PRIMARY KEY,
    plate_number VARCHAR(10) UNIQUE NOT NULL,
    car_id INT,
    FOREIGN KEY (car_id) REFERENCES car(id)
);

\COPY plate FROM './data/plate.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS car_service CASCADE;
-- Create Car Service Table
CREATE TABLE car_service (
    id SERIAL PRIMARY KEY,
    service_id INT,
    car_id INT,
    FOREIGN KEY (service_id) REFERENCES services(id),
    FOREIGN KEY (car_id) REFERENCES car(id)
);

\COPY car_service FROM './data/car_service.csv' WITH CSV HEADER;
