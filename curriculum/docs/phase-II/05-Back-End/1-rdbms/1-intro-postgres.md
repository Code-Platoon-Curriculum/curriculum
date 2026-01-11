# Intro to PostgreSQL

## Introduction

As we move into **Back-End development**, we need to answer a fundamental question:

> _Where does application data actually live?_

In this lesson, we introduce **PostgreSQL**, a powerful relational database system used by modern full-stack applications. You’ll learn what data is, how databases store it, and why relational databases are still the backbone of most production systems. This lecture builds the foundation for Django models, migrations, and persistent data storage.

---

## History of Databases

Databases emerged as a response to the growing need to store and manage large amounts of data efficiently as computers became more common in the mid-20th century. In the 1950s and 1960s, data was stored in **flat files**—simple text or binary files managed directly by application code—which quickly became difficult to scale, search, and maintain as systems grew. To address this, early database models such as **hierarchical databases** (like IBM’s IMS in the 1960s) and **network databases** (CODASYL) were developed, allowing data to be organized with parent–child or graph-like relationships, though they were complex and tightly coupled to application logic. A major breakthrough came in 1970 when **Edgar F. Codd** introduced the **relational model**, proposing that data be stored in tables with well-defined relationships and queried using a high-level, declarative language—this idea led to SQL and the rise of relational databases in the 1980s and 1990s, which became the backbone of enterprise software. As the internet, mobile apps, and cloud computing expanded in the 2000s, the scale and variety of data outgrew traditional relational systems, giving rise to **NoSQL databases** designed for flexibility and horizontal scalability. Today, modern systems often combine relational and non-relational databases, reflecting decades of evolution driven by changing application needs, hardware advances, and the demand for reliable, fast, and scalable data storage.

## What Is Data?

In full-stack development, **data** represents the information our application cares about in order for to enable users to conduct actions within the application itself. Examples include:

- Users
- Products
- Posts
- Comments
- Orders
- Pokémon cards
- Dogs 🐶

Let's think about an everyday full-stack application like Instagram, users most commonly interact with **text data** (usernames, captions, comments, messages), **media data** (images, videos, thumbnails), and **metadata** (timestamps, likes, views, geolocation, device info). They also interact with **relational data**, such as the connections between users (followers/following), posts, comments, and tags, which define how content is organized and displayed. Behind the scenes, applications track **state and preference data** (session tokens, saved posts, theme settings) and **event data** (clicks, scrolls, views, interactions) to support personalization, analytics, and recommendations. Together, these data types flow between the client, server, databases, and external services to create a responsive and personalized user experience.

A critical concept to understand early:

> **Data never truly lives in the browser or the back-end server.** As we've discussed in the past the browser only holds the a skeleton of components to render for the user interface. Instead it makes consistent requests to a Back-End server for data to fill in the blanks and render components for the UI. This doesn't mean that data itself lives within the Back-End server, instead the Back-End server holds the responsibility or processing data by validating prior to entry and by serializing on it's way out. But... where does data come from then??? Data itself lives within _databases_ and is separated from the Back-End server. Think about the single responsibility principle within the Full-Stack Architecture:

- The **browser** only _displays_ data temporarily
- The **server** only _processes_ data
- The **database** is where data is _persisted_

When you refresh a page:

- Browser state disappears but recreates the request prior to rendering a component.
- Server receives request and completes the task or serializing data and sends it as a response.
- **Database data remains**

This persistence is what allows applications to remember users, content, and history over time.

---

## Types of Databases

There are many ways to store data, but most modern applications use one of two major categories.

---

### What Is a Relational Database Management System (RDBMS)?

A **Relational Database Management System (RDBMS)** is software designed to store, organize, and manage data in structured tables made up of rows and columns, where relationships between tables are defined using keys (such as primary and foreign keys) to ensure consistency and integrity. RDBMSs use Structured Query Language (SQL) to create, read, update, and delete data, making them well suited for applications that require reliable transactions, clear data relationships, and strong guarantees around accuracy.

Examples of RDBMS systems:

- PostgreSQL
- MySQL
- SQLite
- Oracle

Relational databases are excellent when:

- Data has structure
- Relationships matter
- Accuracy and consistency are critical

---

### NoSQL Databases

A **non-relational database management system (NoSQL)** is designed to store and manage data that does not fit neatly into fixed tables with predefined schemas, making it well suited for flexible, large-scale, and rapidly changing applications. Instead of rows and columns, NoSQL databases organize data using models such as **document**, **key-value**, **wide-column**, or **graph** structures, allowing developers to store nested, semi-structured, or unstructured data efficiently. These systems often prioritize horizontal scalability, high availability, and performance over strict relational constraints, which is why they are commonly used for real-time analytics, caching, content feeds, and distributed systems. Popular NoSQL databases include **MongoDB**, **Redis**, **Cassandra**, **DynamoDB**, and **Neo4j**.

Key characteristics:

- Schema-less or flexible schema
- Designed for horizontal scaling
- Optimized for large, distributed systems

Examples:

- MongoDB
- Redis
- DynamoDB
- Cassandra

NoSQL databases are often used when:

- Data structure changes frequently
- Massive scale is required
- Relationships are less important

---

## PostgreSQL

---

### What and Why PostgreSQL?

**PostgreSQL** is a powerful, open-source **relational database management system** known for its correctness, extensibility, and standards compliance. It supports advanced SQL features, strong data integrity through constraints and transactions, and complex data types such as JSON, arrays, and full-text search, allowing it to handle both traditional relational data and many modern application needs. You should learn PostgreSQL over other databases because it emphasizes **doing things the right way**—with strict adherence to ACID guarantees—making it an excellent foundation for understanding how databases truly work. It is widely used in production by companies like Instagram, Netflix, and GitHub, scales from small projects to enterprise systems, and integrates extremely well with modern frameworks like Django. Learning PostgreSQL builds transferable skills, since its SQL implementation is close to the standard, and it prepares you to work confidently with both relational concepts and hybrid workloads that other databases often handle less robustly.

---

### MongoDB vs PostgreSQL

| Feature        | MongoDB (NoSQL)        | PostgreSQL (RDBMS)      |
| -------------- | ---------------------- | ----------------------- |
| Data Structure | JSON-like documents    | Tables (rows & columns) |
| Schema         | Flexible / optional    | Strict / enforced       |
| Relationships  | Manual                 | Native                  |
| Query Language | Custom                 | SQL                     |
| Data Integrity | Application-enforced   | Database-enforced       |
| Best For       | Rapid iteration, scale | Structured, relational  |

#### When to Use Each

**MongoDB might be better when:**

- Data structure changes frequently
- Relationships are minimal
- You need extreme horizontal scaling

**PostgreSQL is better when:**

- Data has clear relationships
- Accuracy matters
- You want strong validation and constraints
- You are building a traditional full-stack app

---

## What Is a DataTable?

A **data table** in a relational database is a structured collection of data organized into **rows and columns**, where each column defines a specific attribute (such as `email`, `created_at`, or `price`) and each row represents a single record or entity. This is very similar to a **Python class blueprint**, which defines the attributes and structure that its instances will have—each object created from the class is comparable to a row in the table, and the class’s attributes map to the table’s columns. Just as a class enforces rules through types, default values, and methods, a table enforces rules through data types, constraints, and relationships, ensuring consistency across all stored records. In full-stack development, this conceptual overlap makes it easier to move between object-oriented code and relational data, especially when using ORMs like Django’s models, which act as a bridge between Python classes and database tables.

---

### DataTables and OOP (Mental Model)

Consider this Python class:

```python
class Dog:
    def __init__(self, name, breed, color, age):
        self.name = name
        self.breed = breed
        self.color = color
        self.age = age
```

Now map this to a database:

| OOP Concept       | Database Concept |
| ----------------- | ---------------- |
| Class             | Table            |
| Instance (object) | Row              |
| Attribute         | Column           |

A **Dogs** table might look like:

| id  | name | breed    | color | age |
| --- | ---- | -------- | ----- | --- |
| 1   | Max  | Labrador | Black | 4   |
| 2   | Luna | Husky    | Gray  | 2   |

- The **table** defines structure
- Each **row** represents a specific dog
- Each **column** represents a property

This parallel becomes critical when we introduce Django's Object Relational Mapping capabilities.

---

## Docker and PostgreSQL

Now that we conceptually understand PostgreSQL as an RDBMS let's dive into creating it with Docker.

```Dockerfile
FROM postgres:15

WORKDIR /app

COPY . .

ENV POSTGRES_USER=cp_user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=cp_db

EXPOSE 5432

CMD ["postgres"]
```

There's a new commands here we haven't talked about:

- `ENV`: This is a way to set an environment variable that will exist within the container. This is important when it comes to PostgreSQL since we will want to define an initial user, password and database to interact with inside of this PostgreSQL container.

### Running the Container

This database is one we would like to persist as a background service without occupying the terminal. So far every container we've utilized has taken over our terminal and continues to run as long as the container is open. This time it's different, we will run this container in the background meaning the Docker engine will run it and manage it's runtime without bothering us with terminal output we don't need.

**After creating the image** we can execute the following command to run the container:

```bash
docker run -d --rm \
  -p 5433:5432 \
  -v $(pwd)/practice.sql:/app/practice.sql
  -v $(pwd)/dog_data.csv:/app/dog_data.csv
  --name postgres-container \
  postgres-img
```

Let's break down this command to understand what's going on:

- `-d`: This stands for _daemon_ mode which is a common terminology utilized to explain something is running in the background without letting us know.
- `-p 5433:5432`: During installfest you installed your own version of postgresql onto your machine which is currently running on port 5432. Now we want to link to the _contianers_ port 5432 but ours is occupied. Instead we link our machines port 5433 to the containers port 5432 so we can execute SQL commands and enter the RDBMS.
- `--rm`: This tells docker to _remove_ the container from the docker engine once it stops running.
- `--name postgres-container`: This tells docker you would like to give this container an alias of _postgres-container_.
- `-v $(pwd)/practice.sql:/app/practice.sql`: This creates a mount, meaning that any changes within our local machines `practice.sql` will be reflected within our containers `practice.sql`

Now when you execute `docker ps` you'll see this container living and linked to port 5433.

## SQL Basics

---

### Entering the Database

To interact with PostgreSQL, we use the `psql` command-line tool which was downloaded onto your machine at the same time you installed PostgreSQL. Now you can execute the following to enter your PostgreSQL container:

```bash
psql -h localhost -p 5433 -d cp_db -U cp_user
```

This means within my machine (`-h localhost`) in port 5433 (`-p 5433`) enter the database cp_db (`-d cp_db`) as the user cp_user (`-U cp_user`).

What this does:

- Launches the PostgreSQL interactive shell
- Connects you to the PostgreSQL server
- Allows you to execute SQL commands directly

---

### Creating a DataTable

Now let's go through the process of creating our own data table. Let's take that OOP example of `class Dog` from earlier and write it as a table.

```sql
CREATE TABLE dogs (
  id SERIAL PRIMARY KEY,
  name VARCHAR(20),
  breed VARCHAR(20),
  color VARCHAR(20),
  age INTEGER
);
```

Notice how after every attribute we specify the data type each attribute value should be and how much memory space should be alloted per each one. Let's break it down so we can understand what's happening:

- `SERIAL PRIMARY KEY`: Databases typically generate unique ID values for each entry within a database and the built in functionality of PostgreSQL is to generate ids in a serial manner meaning each entries id increments by 1. So 3 entries would be first as 1 second as 2 and third as 3. The beauty is that this comes programmed already within the database and it's something we as developers will rarely have to worry about.
- `VARCHAR(20)`: This stands for a string up to 20 characters (including spaces).
- `INTEGER`: This means we need a solid integer such as 1,2,3, or 4.

> Notice how all keywords are CAPITALIZED. SQL itself doesn't have this requirement but it is a common developer standard to ensure keywords are easily identifiable and written in capital letters

---

### Inserting Data into a DataTable

Data Tables are meant to hold data and just like Python classes OOP `__init__()` method, SQL has it's own method for creating an *entry* onto a the desire data table.

```sql
INSERT INTO dogs (name, breed, color, age)
VALUES ('Max', 'Labrador', 'Black', 4);
```

Why wasn't `id` included in this command? Well as we stated previously by adding `SERIAL PRIMARY KEY` when we created the Data Table, we handed off the responsibility of managing ID's to PostgreSQL itself.

---

### Maneuvering Commands in `psql`

PostgreSQL provides helpful meta-commands using `\`.

| Command   | Purpose                 |
| --------- | ----------------------- |
| `\l`      | List all databases      |
| `\c`      | Connect to a database   |
| `\d`      | List tables             |
| `\d dogs` | Describe the dogs table |
| `\q`      | Quit psql               |
| `\i`      | Executes SQL files      |

These commands help you explore the database schema quickly.

---

## Inserting Data from a CSV File

---

### Why CSV Files?

Through out your career you'll encounter data files in many different formats such as JSON, CSV, XML and many other types of files. Yet, one of the most commonly used files to import/export data is through CSV (Comma-Separated Values) since they offer the following:

- Human-readable
- Easy to export/import
- Widely supported
- Ideal for bulk data ingestion

---

### Importing Data from CSV

With that said, eventually there may come a time where you'll need to *INJECT* data onto your database from some sort of exported file. Let's go over how we would manage this action.

```sql
\COPY dogs(id, name, breed, color, age)
FROM '/app/dog_data.csv'
DELIMITER ','
CSV HEADER;
```

This efficiently inserts multiple rows at once. Onto your data table but it does cause an issue. Since data was entered from a CSV file the `SERIAL PRIMARY KEY` built in functionality failed to update and recognized what was the last value entered onto the table. We fix this by executing the following:

---

### Updating a SERIAL Primary Key

After importing data, the `SERIAL` counter may be out of sync. To fix it execute the following:

```sql
SELECT setval('dogs_id_seq', (SELECT MAX(id) FROM dogs));
```

This ensures future inserts don’t collide with existing IDs.

---

## Conclusion

In this lecture, you explored what data is and where it truly lives within a full-stack application, examined the key differences between relational and NoSQL databases, and learned why PostgreSQL is a critical skill for backend developers. You connected database tables to familiar object-oriented concepts, practiced basic SQL commands for creating and managing data, and saw how real-world data can be imported using CSV files. This foundation sets the stage for our next topic—**constraints, relationships, and Django models**—where data integrity, structure, and application logic come together in more powerful and meaningful ways.
