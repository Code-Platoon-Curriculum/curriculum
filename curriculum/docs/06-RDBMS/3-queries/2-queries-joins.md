# SQL for Mechanic Shop

## Introduction

Welcome SQL developers! In this lecture, we'll explore SQL queries applied to a hypothetical mechanic shop database. By delving into real-life scenarios, you'll learn how to leverage SQL commands to extract valuable information. Let's embark on a journey through various queries, starting from the basics and progressing to more advanced topics.

## Overview of Database

Our database models a mechanic shop, featuring tables such as `car`, `service`, `driver`, and more. Each table contains essential information about cars, services, employees, and drivers. To better understand the mechanics of SQL, we'll address common queries applied in real-world situations.

## Math Operators

### Greater Than (>)

Scenario: Identify cars with a production year after 2020.

**Query:**

```sql
SELECT * FROM car WHERE year > 2020;
```

### Equal (=)

Scenario: Find the services priced exactly at $29.99.

**Query:**

```sql
SELECT * FROM service WHERE price = 29.99;
```

### Greater Than or Equal To (>=)

Scenario: Retrieve services priced at $50 or more.

**Query:**

```sql
SELECT * FROM service WHERE price >= 50;
```

## COUNT

### Counting Cars

Scenario: The shop is closing early; determine the number of cars currently within the shop.

**Query:**

```sql
SELECT COUNT(*) FROM car;
```

### Counting Services

Scenario: Assess the impact of the early closure by counting the ongoing services.

**Query:**

```sql
SELECT COUNT(*) FROM car_service;
```

### Counting High-Value Cars

Scenario: Identify the number of cars valued at over $40,000.

**Query:**

```sql
SELECT COUNT(*) FROM car WHERE price > 40000;
```

## SUM

### Calculating Total Revenue

Scenario: Sum up the total revenue generated from all services.

**Query:**

```sql
SELECT SUM(price) AS total_revenue FROM service;
```

### Summing Up Salaries

Scenario: Calculate the total salary expense for all employees.

**Query:**

```sql
SELECT SUM(salary) AS total_salary FROM employees;
```

### Summing Car Quantities

Scenario: Determine the total quantity of cars in the shop.

**Query:**

```sql
SELECT SUM(quantity) AS total_cars FROM car;
```

## AVG

### Calculating Average Service Price

Scenario: Find the average price of all services offered.

**Query:**

```sql
SELECT AVG(price) AS average_price FROM service;
```

### Average Employee Salary

Scenario: Assess the average salary of employees in the shop.

**Query:**

```sql
SELECT AVG(salary) AS average_salary FROM employees;
```

### Average Car Year

Scenario: Determine the average production year of cars in the shop.

**Query:**

```sql
SELECT AVG(year) AS average_year FROM car;
```

## WHERE

### Filtering Cars by Make

Scenario: Locate all Honda cars in the shop.

**Query:**

```sql
SELECT * FROM car WHERE make = 'Honda';
```

### Filtering Services by Type

Scenario: Find services containing the word 'Brake.'

**Query:**

```sql
SELECT * FROM service WHERE name_of_service LIKE '%Brake%';
```

### Filtering drivers by Age

Scenario: Identify drivers aged 40 or older.

**Query:**

```sql
SELECT * FROM driver WHERE age >= 40;
```

## IN

### Selecting Specific Cars

Scenario: Retrieve information for specific cars by ID.

**Query:**

```sql
SELECT * FROM car WHERE id IN (1, 3, 5);
```

### Selecting Specific Services

Scenario: Find details for specific services by ID.

**Query:**

```sql
SELECT * FROM service WHERE id IN (2, 4, 6);
```

### Selecting Cars Owned by Specific drivers

Scenario: Identify cars owned by specific individuals.

**Query:**

```sql
SELECT * FROM car WHERE driver IN (1, 3, 5);
```

## AS

### Aliasing Columns

Scenario: Enhance the readability of the result by aliasing columns.

**Query:**

```sql
SELECT car_id AS car_identifier, plate_number AS license_plate FROM plate;
```

### Calculating Total Cost of Services

Scenario: Determine the total cost of services with an alias for clarity.

**Query:**

```sql
SELECT SUM(price) AS total_cost FROM service;
```

### Calculating Average Car Price

Scenario: Present the average car price with a more descriptive alias.

**Query:**

```sql
SELECT AVG(price) AS average_car_price FROM car;
```

## LIKE '%text', '%text%', 'text%'

### Searching for drivers

Scenario: Find drivers with names containing the word 'John.'

**Query:**

```sql
SELECT * FROM driver WHERE name LIKE '%John%';
```

### Searching for Specific Car Models

Scenario: Locate cars with model names ending in 'X.'

**Query:**

```sql
SELECT * FROM car WHERE model LIKE '%X';
```

### Searching for Specific Service Types

Scenario: Identify services starting with the word 'Engine.'

**Query:**

```sql
SELECT * FROM service WHERE name_of_service LIKE 'Engine%';
```

## LIMIT

### Limiting Car Results

Scenario: Display only the first 5 cars in the shop.

**Query:**

```sql
SELECT * FROM car LIMIT 5;
```

### Limiting Service Results

Scenario: Show a maximum of 3 services currently offered.

**Query:**

```sql
SELECT * FROM service LIMIT 3;
```

### Limiting driver Results

Scenario: Present details for the first 2 drivers in the database.

**Query:**

```sql
SELECT * FROM driver LIMIT 2;
```

## DESC

### Sorting Cars by Year (Descending)

Scenario: Retrieve cars ordered by production year in descending order.

**Query:**

```sql
SELECT * FROM car ORDER BY year DESC;
```

### Sorting Services by Price (Descending)

Scenario: Display services ordered by price in descending order.

**Query:**

```sql
SELECT * FROM service ORDER BY price DESC;
```

### Sorting Employees by Salary (Descending)

Scenario: List employees ordered by salary in descending order.

**Query:**

```sql
SELECT * FROM employees ORDER BY salary DESC;
```

## GROUP BY

### Grouping Cars by Make

Scenario: Group cars by their make to analyze distribution.

**Query:**

```sql
SELECT make, COUNT(*) AS car_count FROM car GROUP BY make;
```

### Grouping Services by Price Range

Scenario: Categorize services into price ranges for analysis.

**Query:**

```sql
SELECT CASE WHEN price < 30 THEN 'Low'
            WHEN price < 50 THEN 'Medium'
            ELSE 'High' END AS price_range,
       COUNT(*) AS service_count
FROM service
GROUP BY price_range;
```

### Grouping drivers by Age Range

Scenario: Classify drivers into age groups for demographic analysis.

**Query:**

```sql
SELECT CASE WHEN age < 30 THEN 'Young'
            WHEN age < 50 THEN 'Middle-Aged'
            ELSE 'Senior' END AS age_group,
       COUNT(*) AS driver_count
FROM driver
GROUP BY age_group;
```

## JOIN

### Joining Cars and drivers

Scenario: Retrieve information about cars and their respective drivers.

**Query:**

```sql
SELECT car.*, driver.name AS driver_name
FROM car
JOIN driver ON car.driver = driver.id;
```

### Joining Services and Cars

Scenario: Obtain details about services and the cars they are associated with.

**Query:**

```sql
SELECT service.*, car.make, car.model
FROM car_service
JOIN service ON car_service.service_id = service.id
JOIN car ON car_service.car_id = car.id;
```

### Joining Employees and Departments

Scenario: Understand the department distribution of employees.

**Query:**

```sql
SELECT employees.*, department.department_name
FROM employees
JOIN department ON employees.department_id = department.id;
```

## LEFT JOIN

### Left Joining Cars and Plates

Scenario: Retrieve information about cars and their license plates.

**Query:**

```sql
SELECT car.*, plate.plate_number
FROM car
LEFT JOIN plate ON car.id = plate.car_id;
```

### Left Joining Services and Cars

Scenario: Access details about services and their associated cars.

**Query:**

```sql
SELECT service.*, car.make, car.model
FROM service
LEFT JOIN car_service ON service.id = car_service.service_id
LEFT JOIN car ON car_service.car_id = car.id;
```

### Left Joining Employees and Shifts

Scenario: View employee details along with their shifts.

**Query:**

```sql
SELECT employees.*, shifts.start_time, shifts.end_time
FROM employees
LEFT JOIN shifts ON employees.id = shifts.employee_id;
```

## RIGHT JOIN

### Right Joining Cars and Plates

Scenario: Retrieve information about license plates and the cars they belong to.

**Query:**

```sql
SELECT car.*, plate.plate_number
FROM plate
RIGHT JOIN car ON plate.car_id = car.id;
```

### Right Joining Services and Cars

Scenario: Access details about services and the cars they are associated with.

**Query:**

```sql
SELECT service.*, car.make, car.model
FROM car_service
RIGHT JOIN service ON car_service.service_id = service.id
RIGHT JOIN car ON car_service.car_id = car.id;
```

### Right Joining Employees and Shifts

Scenario: View employee details along with their shifts.

**Query:**

```sql
SELECT employees.*, shifts.start_time, shifts.end_time
FROM shifts
RIGHT JOIN employees ON shifts.employee_id = employees.id;
```

## JOINING 3 TABLES

### Joining Cars, drivers, and Services

Scenario: Retrieve comprehensive details about cars, their drivers, and the services they've undergone.

**Query:**

```sql
SELECT car.*, driver.name AS driver_name, service.name_of_service
FROM car
JOIN driver ON car.driver = driver.id
JOIN car_service ON car.id = car_service.car_id
JOIN service ON car_service.service_id = service.id;
```

### Joining Services, Cars, and Employees

Scenario: Gather information about services, the cars they are associated with, and the employees who performed them.

**Query:**

```sql
SELECT service.*, car.make, car.model, employees.employee_name
FROM service
JOIN car_service ON service.id = car_service.service_id
JOIN car ON car_service.car_id = car.id
JOIN employees ON car_service.employee_id = employees.id;
```

### Joining drivers, Cars, and Plates

Scenario: Retrieve data about drivers, their cars, and the associated license plates.

**Query:**

```sql
SELECT driver.*, car.make, car.model, plate.plate_number
FROM driver
JOIN car ON driver.id = car.driver
LEFT JOIN plate ON car.id = plate.car_id;
```

## Conclusion

Congratulations on completing this comprehensive SQL lecture for the mechanic shop database! You've covered a wide range of queries, from basic math operators to complex joins involving multiple tables. Armed with this knowledge, you're well-equipped to tackle real-world scenarios and extract valuable insights from databases. Keep practicing, exploring, and building your SQL expertise!

## Additional Resources

- [Aggregate Functions (COUNT, AVG etc)](https://www.postgresql.org/docs/15/tutorial-agg.html)
- [GROUP BY and HAVING](https://www.postgresql.org/docs/15/queries-table-expressions.html#QUERIES-GROUP)
- [Different types of JOINs](https://www.postgresql.org/docs/15/tutorial-join.html)
- [LIKE and ILIKE](https://www.postgresql.org/docs/15/functions-matching.html#FUNCTIONS-LIKE)
- [Comparisons (IS, NOT, boolean comparison)](https://www.postgresql.org/docs/15/functions-comparison.html)
