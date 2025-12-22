# Familiarizing Yourself with a New Database: Best Practices and Common Pitfalls

## Introduction

Welcome, aspiring SQL developers! When you embark on a journey with a new database, it's essential to navigate through the intricacies to work efficiently and avoid potential pitfalls. In this lecture, we'll explore the best practices for getting acquainted with a new database and highlight common mistakes to steer clear of.

## Exploring the Database Structure

### Good Practice: Utilize Schema and Table Descriptions

- **Best Practice:** Leverage schema and table descriptions to understand the purpose and structure of each element.
  
  ```sql
  -- View schema description
  COMMENT ON SCHEMA your_schema IS 'Description of your schema';

  -- View table description
  COMMENT ON TABLE your_table IS 'Description of your table';
  ```

  We haven't talked about comments yet or where they go so lets take a moment here to iterate on comments within PostgreSQL.

  Comments are typically stored within a separate table named `pg_description` where every table created is referenced to by it's object ID(oid). Unfortunately `pg_description` doesn't actually store the table name just the description and oid which means in order to pull a comment from this table we have to utilize a function `obj_description`. Here's an example

  ```sql
  SELECT obj_description('<table>'::regclass);
  ```

  This function expects one argument which is the tables oid... but how do we get said oid? Oid's and names are stored within a separate table named `pg_class` and we can find it by running a query to explicitly return the oid of a table by matching the relname to the table name.... but this is a long process and there has to be a quicker way. Instead we utilize `<table>::regclass` which will return a special data type of the class named `<table>` and from this class `obj_description` will only grab the oid to find the correct description and print it onto our terminal.

### Bad Practice: Neglecting to Document Database Elements

- **Pitfall:** Failing to document schema, tables, or columns can lead to confusion for you and your team.

## Querying the Database

### Good Practice: Start with SELECT Statements

- **Best Practice:** Begin by querying data with SELECT statements to explore and understand the content.

  ```sql
  -- Retrieve all columns from a table
  SELECT * FROM your_table;
  ```

### Bad Practice: Modifying Data Without Proper Understanding

- **Pitfall:** Avoid updating or deleting data before understanding its impact on the database.

## Analyzing Data Relationships

### Good Practice: Examine Foreign Key Relationships

- **Best Practice:** Identify foreign key relationships to understand how tables are linked.

### Bad Practice: Ignoring Foreign Key Constraints

- **Pitfall:** Neglecting foreign key constraints may lead to inconsistencies in the data.

## Ensuring Data Integrity

### Good Practice: Apply Constraints for Data Quality

- **Best Practice:** Implement constraints (e.g., NOT NULL, CHECK) to maintain data integrity.

  ```sql
  -- Add NOT NULL constraint
  ALTER TABLE your_table
  ALTER COLUMN your_column SET NOT NULL;
  ```

### Bad Practice: Allowing Null Values Without Reason

- **Pitfall:** Allowing unnecessary NULL values may lead to unexpected behavior.

## Monitoring Performance

### Good Practice: Use EXPLAIN ANALYZE for Query Optimization

- **Best Practice:** Employ EXPLAIN ANALYZE to understand and optimize query performance.

  ```sql
  EXPLAIN ANALYZE SELECT * FROM your_table WHERE condition;
  ```

### Bad Practice: Neglecting Query Performance

- **Pitfall:** Ignoring performance considerations can result in slow and inefficient queries.

## Conclusion

Navigating a new database requires a strategic and meticulous approach. By adopting these best practices and avoiding common pitfalls, you'll not only understand the database more effectively but also contribute to maintaining a robust and efficient system. Remember, a well-documented and well-understood database is a powerful asset for any developer. Happy querying!
