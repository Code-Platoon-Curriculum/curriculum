# PostgreSQL SQL Commands CheatSheet

## SQL Commands

- **SELECT Statement**
  
  ```sql
  SELECT column1, column2 FROM table_name WHERE condition;
  ```

  - **What it's used for?**
    - Retrieves data from one or more tables based on specified conditions.
  - **How to use it**
    - Replace `column1`, `column2`, `table_name`, and `condition` as needed.
  - **When to use it**
    - When you want to fetch specific data from a table.

- **INSERT Statement**
  
  ```sql
  INSERT INTO table_name (column1, column2) VALUES (value1, value2);
  ```

  - **What it's used for?**
    - Inserts new records into a table.
  - **How to use it**
    - Replace `table_name`, `column1`, `column2`, `value1`, and `value2` with appropriate values.
  - **When to use it**
    - When you need to add new data to a table.

- **UPDATE Statement**
  
  ```sql
  UPDATE table_name SET column1 = value1 WHERE condition;
  ```

  - **What it's used for?**
    - Modifies existing records in a table.
  - **How to use it**
    - Replace `table_name`, `column1`, `value1`, and `condition` as needed.
  - **When to use it**
    - When you want to change data in a table based on certain conditions.

- **DELETE Statement**
  
  ```sql
  DELETE FROM table_name WHERE condition;
  ```

  - **What it's used for?**
    - Deletes records from a table based on specified conditions.
  - **How to use it**
    - Replace `table_name` and `condition` as needed.
  - **When to use it**
    - When you need to remove specific data from a table.

- **CREATE TABLE Statement**
  
  ```sql
  CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    ...
  );
  ```

  - **What it's used for?**
    - Creates a new table with specified columns and data types.
  - **How to use it**
    - Replace `table_name`, `column1`, `datatype`, and additional columns as needed.
  - **When to use it**
    - When you need to define a new table structure.

- **ALTER TABLE Statement**
  
  ```sql
  ALTER TABLE table_name ADD COLUMN new_column datatype;
  ```

  - **What it's used for?**
    - Modifies an existing table by adding a new column.
  - **How to use it**
    - Replace `table_name`, `new_column`, and `datatype` as needed.
  - **When to use it**
    - When you want to add a new column to an existing table.

- **DROP TABLE Statement**
  
  ```sql
  DROP TABLE table_name;
  ```

  - **What it's used for?**
    - Removes an existing table and all its data.
  - **How to use it**
    - Replace `table_name` with the name of the table to be dropped.
  - **When to use it**
    - When you want to delete a table and its associated data.

- **SELECT with WHERE Clause**
  
  ```sql
  SELECT column1, column2 FROM table_name WHERE condition;
  ```

  - **What it's used for?**
    - Filters data based on specified conditions.
  - **How to use it**
    - Replace `column1`, `column2`, `table_name`, and `condition` as needed.
  - **When to use it**
    - When you want to retrieve specific rows based on certain criteria.

- **ORDER BY Clause**
  
  ```sql
  SELECT column1, column2 FROM table_name ORDER BY column1 [ASC|DESC];
  ```

  - **What it's used for?**
    - Sorts the result set in ascending (ASC) or descending (DESC) order.
  - **How to use it**
    - Replace `column1`, `column2`, and `table_name` as needed.
  - **When to use it**
    - When you want to arrange the output in a specific order.

- **LIMIT Clause**
  
  ```sql
  SELECT column1, column2 FROM table_name LIMIT n;
  ```

  - **What it's used for?**
    - Limits the number of rows returned in the result set.
  - **How to use it**
    - Replace `column1`, `column2`, `table_name`, and `n` as needed.
  - **When to use it**
    - When you want to retrieve only a specific number of rows.

- **JOIN Clause (Inner Join)**
  
  ```sql
  SELECT * FROM table1 INNER JOIN table2 ON table1.column = table2.column;
  ```

  - **What it's used for?**
    - Combines rows from two or more tables based on a related column.
  - **How to use it**
    - Replace `table1`, `table2`, and the join condition as needed.
  - **When to use it**
    - When you need to retrieve data that spans multiple tables.

- **LEFT JOIN Clause**
  
  ```sql
  SELECT * FROM table1 LEFT JOIN table2 ON table1.column = table2.column;
  ```

  - **What it's used for?**
    - Returns all rows from the left table and matched rows from the right table.
  - **How to use it**
    - Replace `table1`, `table2`, and the join condition as needed.
  - **When to use it**
    - When you want to retrieve unmatched rows from the left table.

- **AS Keyword (Alias)**
  
  ```sql
  SELECT column1 AS alias_name FROM table_name;
  ```

  - **What it's used for?**
    - Renames a column or table with an alias.
  - **How to use it**
    - Replace `column1`, `alias_name`, and `table_name` as needed.
  - **When to use it**
    - When you want to provide a more meaningful name to a column or table.

- **LIKE Operator**
  
  ```sql
  SELECT * FROM table_name WHERE column1 LIKE 'pattern';
  ```

  - **What it's used for?**
    - Filters data based on a specified pattern using wildcard characters (% and _).
  - **How to use it**
    - Replace `table_name`, `column1`, and the pattern as needed.
  - **When to use it**
    - When you need to search for a specific pattern in text data.

- **IN Operator**
  
  ```sql
  SELECT * FROM table_name WHERE column1 IN (value1, value2, ...);
  ```

  - **What it's used for?**
    - Filters data based on a set of specified values.
  - **How to use it**
    - Replace `table_name`, `column1`, and the list of values as needed.
  - **When to use it**
    - When you want to retrieve rows with values matching any in a specified list.

- **COUNT Aggregate Function**
  
  ```sql
  SELECT COUNT(column1) FROM table_name;
  ```

  - **What it's used for?**
    - Returns the number of rows that satisfy the specified conditions.
  - **How to use it**
    - Replace `column1` and `table_name` as needed.
  - **When to use it**
    - When you want to count the number of rows in a table.

- **SUM Aggregate Function**
  
  ```sql
  SELECT SUM(column1) FROM table_name;
  ```

  - **What it's used for?**
    - Returns the sum of values in a numeric column.
  - **How to use it**
    - Replace `column1` and `table_name` as needed.
  - **When to use it**
    - When you want to find the total of a numeric column.

- **AVG Aggregate Function**
  
  ```sql
  SELECT AVG(column1) FROM table_name;
  ```

  - **What it's used for?**
    - Returns the average value of a numeric column.
  - **How to use it**
    - Replace `column1` and `table_name` as needed.
  - **When to use it**
    - When you want to calculate the average of a numeric column.

- **GROUP BY Clause**

  ```sql
  SELECT column1, COUNT(column2) FROM table_name GROUP BY column1;
  ```

  - **What it's used for?**
    - Groups the result set by one or more columns and applies aggregate functions.
  - **How to use it**
    - Replace `column1`, `column2`, and `table_name` as needed.
  - **When to use it**
    - When you want to perform aggregate functions on grouped data.
