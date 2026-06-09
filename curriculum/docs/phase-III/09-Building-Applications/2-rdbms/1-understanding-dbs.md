# Relational Databases

---

## Intro

Welcome, builders. Before you can instruct an AI agent to scaffold a database for your application, you need to understand what you're actually asking it to build. Agentic tools like Claude Code are remarkably powerful, but they operate on the mental model *you* bring to the conversation. If your model is fuzzy, the output will be fuzzy. If your model is clear, the output will be precise, structured, and something you can actually trust.

This lecture is about building that mental model for **relational databases** — one of the most foundational concepts in software engineering. By the end, you'll understand what a relational database is, how to look at your application idea and extract the data it needs, how to represent that data correctly, and how to describe the connections between different pieces of data.

---

## Lesson

### What is a Relational Database Management System

A **Relational Database Management System**, or **RDBMS**, is software that stores, organizes, and retrieves structured data using a model based on *tables* and *relationships between those tables*.

To understand what "relational" means, forget computers for a moment. Imagine a public library. The library has a physical card catalog (or today, a digital one) that tracks every book it owns. It also keeps records of every person who holds a library card. And it keeps a log of every time someone borrows a book. These three collections of information — books, members, and loans — are separate, but they are *related*. A loan connects a specific member to a specific book on a specific date. Without that relationship, the data is just a pile of disconnected facts.

An RDBMS works exactly the same way. It stores data in **tables** — think of a table like a spreadsheet, with rows and columns. Each row is a single record (one book, one member, one loan). Each column is a specific attribute of that record (title, name, date). And crucially, tables can be *linked together* through shared pieces of data, which is where the "relational" in the name comes from.

The software that sits on top of this structure — the RDBMS itself — handles all the mechanics: writing data to disk, making sure multiple users can read and write at the same time without corrupting anything, enforcing rules about what data is valid, and giving you a query language (almost always **SQL** — Structured Query Language) to ask questions like "give me all the books borrowed by members who signed up in 2024."

Some of the most widely used RDBMSs in the world include **PostgreSQL**, **MySQL**, **SQLite**, and **Microsoft SQL Server**. In your work as a builder, you'll most commonly encounter **PostgreSQL** — it's the engine powering Supabase, the platform you'll connect to in the next lecture. PostgreSQL is open-source, battle-tested, and capable of handling everything from a small side project to large-scale production systems.

The key things to hold onto from this section are:

- Data is stored in **tables** (rows and columns).
- Tables can be **linked** to each other through relationships.
- An **RDBMS** is the software engine that manages all of this.
- You talk to it using **SQL**.

---

### How to Identify Data Needed for Your Application

One of the most common mistakes new builders make is jumping straight into building before they've thought clearly about their data. They end up with a messy structure that doesn't match their application's real needs — and when you're relying on an AI agent to help you build, that messiness compounds fast. Garbage in, garbage out.

So how do you figure out what data your application actually needs? The answer is to start with your **user stories**. For example, imagine you're building a simple task management app:

- *As a user, I want to create tasks so that I can track what I need to do.*
- *As a user, I want to assign tasks to projects so that I can organize my work.*
- *As a user, I want to mark tasks as complete so that I know what I've finished.*

Now, read those stories carefully and ask: **what "things" (nouns) does this application need to remember?** From the stories above, you can extract:

- A **user** (the person using the app)
- A **task** (something to be done)
- A **project** (a collection of tasks)

Each of these nouns is almost certainly going to become its own **table** in your database. This is a powerful heuristic: the nouns in your user stories map to your tables. The attributes of those nouns — the descriptive details — map to your **columns**.

Let's keep extracting. For a task, what do we need to know?

- What is it called? (a name or title)
- Is it done? (a completed status)
- When was it created? (a date and/or time)
- Which project does it belong to? (a connection)
- Who created it? (a connection)

For a project:

- What is it called? (a name or title)
- What is it about? (a description)
- Who owns it? (a connection)

This process — reading user stories, identifying nouns, and then listing the attributes of each noun — is how you begin designing your data model. It doesn't require a computer. It doesn't require code. It just requires careful reading and clear thinking.

> **Tip:** When you're unsure whether something should be its own table or just a column, ask yourself: *"Does this thing have attributes of its own?"* A task's "status" (pending, in progress, complete) is just a value — it probably doesn't need its own table. But a "project" has a name, a description, and an owner — it has its own attributes, so it earns its own table.

---

### Mapping out your First Table From Object to Data

Once you've identified your nouns and their attributes, you're ready to design your first table. Let's walk through this together using the **task** from our example above.

Think of a table as a structured container for a specific type of thing. Every row in the table represents one instance of that thing. Every column represents one fact about it. Almost like a spread sheet.

Here is what a `tasks` table might look like:

| id | title              | is_complete | created_at          | project_id |
|----|--------------------|-------------|---------------------|------------|
| 1  | Write intro email  | false       | 2024-11-01 09:00:00 | 3          |
| 2  | Review pull request| true        | 2024-11-01 10:30:00 | 3          |
| 3  | Plan sprint        | false       | 2024-11-02 08:00:00 | 7          |

A few things to notice:

- **Every row has a unique `id`.** This is the row's identity — its permanent name. This column is called the **Primary Key**. No two rows in the same table share a primary key. Think of it like a Social Security number: it exists purely to uniquely identify this one record in the whole table.
- **Column names are specific and lowercase**, usually with underscores instead of spaces. This is standard practice in databases.
- **The `project_id` column references another table.** That's a relationship — we'll get to that shortly.

The table name itself is typically the **plural** of the noun: `tasks`, `users`, `projects`. This convention signals that the table holds *many* records of that type.

Now lets bring this into <a href="https://drawsql.app/" target="_">DrawSQL</a> and attempt to ctranslate this structure: a table name, a set of columns, each column with a specific type.

---

#### Choosing the Right Types to Represent Your Data

Every column in a database table must have a **data type** — a declaration of what kind of value lives in that column. Choosing the right data type matters for three reasons: it ensures your data is stored correctly, it prevents invalid data from sneaking in, and it allows the database to perform operations efficiently.

Here are the most important types you'll work with in PostgreSQL:

---

**`INTEGER` (or `INT`)**

A whole number. No decimals. Use this for counts, IDs, quantities, ages — anything that's a number but will never have a fractional part.

> *Real-life analogy:* The number of seats at a table. You can have 4 seats or 5 seats, but never 4.7 seats.

---

**`BIGINT`**

A very large whole number. Use this when you expect values that could exceed ~2 billion — for example, unique user IDs in a large-scale system, or metrics like total page views.

> In practice, many databases auto-generate IDs using a special `BIGSERIAL` type that automatically increments, which is a `BIGINT` under the hood.

---

**`DECIMAL` (or `NUMERIC`)**

A number with a precise fractional part. This is the right choice for **money** — never use a floating point type (like `FLOAT` or `REAL`) for currency, because floating point arithmetic can introduce tiny rounding errors that cause real financial problems.

> *Real-life analogy:* The price of a product. $19.99 needs to be stored exactly as `19.99`, not approximately.

---

**`VARCHAR(n)`**

A variable-length string of text, up to `n` characters. Use this for short text values where you want to enforce a maximum length — usernames, email addresses, titles, city names.

> *Real-life analogy:* A form field with a character limit. You can type anything you want, but the form only accepts up to 255 characters.

---

**`TEXT`**

An unrestricted string of text. Use this for long-form content — descriptions, comments, blog post bodies — where you don't want to (or can't) predict a character limit.

> *Real-life analogy:* The notes field in your phone's Notes app. There's no cap; write as much as you want.

---

**`BOOLEAN`**

A value that is either `true` or `false`. Perfect for flags and states: is this task complete? Is this account active? Is this post published?

> *Real-life analogy:* A light switch. It's either on or off, nothing in between.

---

**`TIMESTAMP`** (or **`TIMESTAMPTZ`** for time-zone-aware)

A specific point in time, down to the second (or microsecond). Use this to record *when* something happened: when a record was created, when a user last logged in, when an order was placed.

> *Real-life analogy:* The timestamp on a receipt. Not just a date — a precise moment.

---

**`DATE`**

Just a calendar date, with no time component. Use this when the time of day is irrelevant — a birthday, a due date, an anniversary.

> *Real-life analogy:* A calendar entry that just says "November 15th" without a specific time.

---

**`UUID`**

A Universally Unique Identifier — a randomly generated 128-bit value that looks like `a1b2c3d4-e5f6-7890-abcd-ef1234567890`. Many modern systems use UUIDs instead of sequential integers for primary keys because they're globally unique, which makes them safe to generate on the client side or across distributed systems without collision.

> Supabase defaults to UUIDs for primary keys. You'll see this in action in the next lecture.

---

**`JSONB`**

Stores a JSON object in a binary format, allowing you to store semi-structured or flexible data inside a single column. This is a PostgreSQL superpower — most traditional RDBMSs don't support this. Use it sparingly for truly flexible data (like configuration objects or metadata) where you don't know the exact shape in advance. Don't use it as a crutch to avoid designing a proper relational structure.

> *Real-life analogy:* A filing cabinet drawer labeled "Miscellaneous." Sometimes you need it, but if *everything* goes in there, you've given up on organizing.

---

**Putting it together:** Here's the `tasks` table with proper data types:

| Column      | Type          | Notes                          |
|-------------|---------------|-------------------------------|
| id          | UUID          | Primary key, auto-generated   |
| title       | VARCHAR(255)  | Required                       |
| is_complete | BOOLEAN       | Defaults to `false`           |
| created_at  | TIMESTAMPTZ   | Set automatically on insert   |
| project_id  | UUID          | Foreign key → `projects.id`  |

---

### Relationships

#### What are Relationships

You've identified your tables. Each table holds information about one type of thing. But in almost every real application, those things are connected. A task belongs to a project. A project belongs to a user. A student enrolls in many courses. These connections are called **relationships**, and they are the heart of what makes a *relational* database relational.

Relationships are implemented through a mechanism called a **Foreign Key**. A foreign key is a column in one table that contains the primary key of a row in another table. It's a pointer — a way of saying "this record over here is linked to that record over there."

Think of it like this: if your `tasks` table has a column called `project_id`, and that column contains the value `3`, that's a foreign key pointing to the row in the `projects` table where `id = 3`. The database can use that link to connect the two records whenever you need them together.

There are three fundamental types of relationships you'll encounter. Understanding which type applies in a given situation is one of the most important design decisions you'll make.

---

#### One-to-One

A **one-to-one relationship** exists when a single record in Table A is associated with exactly one record in Table B, and vice versa.

This type of relationship is the least common. It often appears when you want to split a large table into two for organizational or performance reasons, or when a secondary set of attributes only applies to a subset of records.

> *Real-life analogy:* A person and their passport. One person has exactly one passport. One passport belongs to exactly one person. (In the context of your country's records, at least.)

**Database example:** Imagine a `users` table and a `user_profiles` table. The core `users` table holds authentication data (email, password hash). The `user_profiles` table holds extended information (bio, avatar URL, website). Every user has at most one profile, and every profile belongs to exactly one user.

```
users                   user_profiles
--------                ----------------
id (PK)  ◄──────────── user_id (FK, unique)
email                   bio
password_hash           avatar_url
```

The word "unique" on the foreign key column is what enforces the one-to-one nature — it prevents two profile rows from pointing to the same user.

---

#### Many-to-One

A **many-to-one relationship** (sometimes called **one-to-many**, depending on which direction you're reading it) is by far the most common relationship in relational databases.

It exists when *many* records in Table A are associated with *one* record in Table B.

> *Real-life analogy:* Many employees work at one company. One company has many employees. From the employee's perspective, they have one employer (many-to-one). From the company's perspective, it has many employees (one-to-many). It's the same relationship, just viewed from different angles.

**Database example:** Our task management app. Many tasks can belong to one project. A project can have many tasks.

```
projects                tasks
--------                ------
id (PK)  ◄──────────── project_id (FK)
name                    id (PK)
description             title
                        is_complete
```

The foreign key (`project_id`) lives on the "many" side — in the `tasks` table. Each task row says "I belong to project X" by storing X's ID. The `projects` table doesn't need to know anything about the tasks directly; you can find all tasks for a project by querying the `tasks` table for rows where `project_id` matches.

This is the pattern you'll implement most frequently. Whenever you find yourself saying "each [thing] belongs to one [other thing]," you're describing a many-to-one relationship, and the foreign key goes on the "each [thing]" side.

---

#### Many-to-Many

A **many-to-many relationship** exists when records in Table A can be associated with multiple records in Table B, *and* records in Table B can be associated with multiple records in Table A.

> *Real-life analogy:* Students and courses at a university. One student can enroll in many courses. One course can have many students enrolled. Neither side is exclusively "one."

This is where things get interesting — and where a new concept comes in. You *cannot* represent a many-to-many relationship with a simple foreign key column on one of the two tables. Think about why: if a student can be in multiple courses, you can't just add a `course_id` column to the `students` table — that only holds one course ID.

The solution is a **junction table** (also called a bridge table, pivot table, or associative table). This is a third table whose entire purpose is to record the *pairings* between the two main tables.

**Database example:** Students and courses.

```
students                  enrollments                 courses
--------                  -----------                 --------
id (PK)  ◄─────────────── student_id (FK)             id (PK)
name                      course_id (FK) ──────────►  name
email                     enrolled_at                 credits
                          grade
```

Each row in `enrollments` represents one student-course pairing. Notice that the junction table can also carry its own data — in this case, when the student enrolled and what their grade is. That data belongs to the *relationship itself*, not to the student alone or the course alone.

The primary key of a junction table is often a **composite key** — a combination of both foreign keys (`student_id` + `course_id`) — since the combination of the two is what makes a row unique.

---

#### How to Choose Your Relationships

Now that you know the three types, here's a practical decision process for choosing which applies to your situation.

**Write out the relationship in plain English, in both directions.**

Take any two tables and describe their relationship from each side:

- "A task belongs to ___ project(s)." → *one* project → many-to-one
- "A project has ___ task(s)." → *many* tasks → one-to-many (same relationship, other side)

If one direction is "one" and the other is "many": **many-to-one / one-to-many**. Foreign key goes on the "many" side. If both directions are "one": **one-to-one**. Foreign key (with a unique constraint) goes on either side, but typically the "weaker" or "optional" entity. If both directions are "many": **many-to-many**. You need a junction table.

---

**Resist the urge to model everything as many-to-many.**

New designers often reach for junction tables even when a simpler relationship would do. Before you create a junction table, ask: "is there a real-world scenario where the link goes in both directions with multiple records on each side?" If the answer is no, simplify.

---

**Draw it out.**

Before writing a single line of code, sketch your tables and their relationships. This is exactly what tools like <a href="https://drawsql.app" target="_">DrawSql</a> are for. Drag in a table, add your columns, drag in another table, draw the relationship line between them. Seeing your data model visually is one of the fastest ways to catch mistakes — a foreign key pointing the wrong way, a missing junction table, a table that shouldn't exist at all.

In your hands-on portion of this lecture, you'll practice building this diagram in DrawSQL. Don't skip this step. The 15 minutes you spend diagramming will save you hours of refactoring later.

---

## Conclusion

A **Relational Database Management System** is the backbone of most serious applications. It stores data in structured **tables**, enforces rules about what data is valid, and allows tables to be linked through **relationships** using **foreign keys**.

Designing a good data model starts long before you touch a database tool. It starts with your **user stories** — reading them carefully, identifying the nouns, and listing the attributes of each noun. Those nouns become your **tables**. Those attributes become your **columns**. And the connections between your nouns become your **relationships**.

When building your columns, choose **data types** that accurately reflect the nature of each piece of data — don't reach for `TEXT` when `BOOLEAN` is the right call, and never store money in a floating-point type.

When connecting tables, identify the type of relationship — **one-to-one**, **many-to-one**, or **many-to-many** — and implement it correctly. Most of your relationships will be many-to-one, with a foreign key on the "many" side. When you encounter many-to-many, reach for a junction table.

Finally, always **draw your schema first**. A clear visual diagram is both a thinking tool and a communication tool — it's what you'll share with teammates, what you'll describe to an AI agent, and what you'll reference when something breaks.
