# Constraints & Queries

## Introduction

Now that we understand **what databases are**, **how tables work**, and **how data is inserted**, we need to answer two critical questions:

> **How do we protect our data from becoming invalid?**
> **How do we ask intelligent questions of that data once it exists?**

This lecture introduces **constraints** and **queries**, two concepts that turn a database from a passive storage system into an **active enforcer of rules** and a **powerful information engine**.

Constraints define *what data is allowed to exist*.
Queries define *how we retrieve and reason about that data*.

Together, they form the backbone of **data integrity** and **business logic** in backend systems.

---

## Why Constraints Matter

Without constraints, a database is just a box that accepts *anything*:

* Users with no email
* Negative ages
* Duplicate usernames
* Orders without owners

These are **not application bugs** — they are **data bugs**, and once bad data exists, *every layer above it becomes unreliable*.

> A database without constraints is like a class with public attributes and no validation.

---

## Constraints as OOP Setters (Mental Model)

Let’s start with a Python example.

```python
class User:
    def __init__(self, email, age):
        self.email = email
        self.age = age

    @property
    def email(self):
      return self._email
    
    @property
    def age(self):
      return self._age

    @email.setter
    def email(self, new_email):
        if "@" not in email:
            raise ValueError("Invalid email")
        self._email = email

    @age.setter
    def age(self, new_age):
        if age < 0:
            raise ValueError("Age must be positive")
        self._age = age
```

Here’s what’s happening:

* We **do not trust raw input**
* We **validate before assignment**
* We **reject invalid state**

This is *exactly* what database constraints do.

> **Database constraints are setters that never get skipped and ensure our data maintains consistency through out its existence.**

---

## What Are Database Constraints?

A **constraint** is a rule enforced by the database that restricts the values allowed in a column or table.

Constraints:

* Protect data at the lowest level
* Cannot be bypassed by application code
* Apply universally (API, admin panel, scripts, imports)

---

## Common Constraint Types

---

### NOT NULL

Prevents missing values.

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL
);
```

**OOP Equivalent**

```python
if email is None:
    raise ValueError("email required")
```

Use when:

* A value is required for meaning
* The application cannot function without it

---

### UNIQUE

Prevents duplicates.

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE
);
```

**OOP Equivalent**

```python
if email in existing_emails:
    raise ValueError("email already taken")
```

Use when:

* Values must be globally distinct
* Examples: emails, usernames, slugs

---

### CHECK

Enforces custom logic rules.

```sql
CREATE TABLE dogs (
  id SERIAL PRIMARY KEY,
  age INTEGER CHECK (age >= 0)
);
```

**OOP Equivalent**

```python
if age < 0:
    raise ValueError("Invalid age")
```

Use when:

* Numeric or logical boundaries exist
* Business rules are predictable

---

### DEFAULT

Provides a fallback value.

```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**OOP Equivalent**

```python
def __init__(self, created_at=None):
    self.created_at = created_at or datetime.now()
```

Use when:

* A value should exist even if not provided
* Time-based metadata, flags, statuses

---

### PRIMARY KEY

Uniquely identifies a row.

```sql
id SERIAL PRIMARY KEY
```

* Cannot be NULL
* Cannot be duplicated
* Used for relationships

**OOP Equivalent**

```python
self.id = uuid4()
```

Except the database *guarantees* uniqueness globally.

---

### FOREIGN KEY (Relationships)

Foreign keys link tables together.

```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id)
);
```

This ensures:

* A post **cannot exist without a valid user**
* Orphaned data is impossible

**OOP Equivalent**

```python
class Post:
    def __init__(self, user):
        if not isinstance(user, User):
            raise ValueError("Invalid user")
        self.user = user
```

> Foreign keys enforce **object relationships at the data level**. We will talk about this in more detail once we are working within Django.

---

## Constraints Belong in the Database

A critical mindset shift:

> **Validation in Python is helpful.
> Constraints in the database are mandatory.**

Why?

* Multiple apps may access the same DB
* Scripts and migrations bypass application logic
* Databases must defend themselves

This is why Django **generates constraints automatically** when you define models correctly.

---

## Updating the Dog Table

Now that we've learned so much about constraints, let's update our Dog table within our practice.sql file and include it within our Database to look as such:

```sql
DROP TABLE IF EXISTS dogs;

CREATE TABLE dogs (
  id SERIAL PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  breed VARCHAR(20) NOT NULL,
  color VARCHAR(20) NOT NULL DEFAULT 'Unknown',
  age INTEGER NOT NULL CHECK (age >= 0),
  UNIQUE (name, breed)
);

\COPY dogs(id, name, breed, color, age)
FROM '/app/dog_data.csv'
DELIMITER ','
CSV HEADER;

SELECT setval('dogs_id_seq', (SELECT MAX(id) FROM dogs));
```

## Queries: Asking Questions of Your Data

Once data is safe, we need to **retrieve it intelligently**.

> **Queries are read-only methods that operate over collections of objects.**

---

### SELECT (The Read Operation)

```sql
SELECT * FROM dogs;
```

This will return all instances of dogs, almost exactly like:

```python
dogs = [Dog(), Dog(), Dog()]

print(dogs)
```

---

### Filtering Data (WHERE)

```sql
SELECT * FROM dogs
WHERE age > 3;
```

**OOP Equivalent**

```python
[dog for dog in dogs if dog.age > 3]
```

---

### Selecting Specific Columns

```sql
SELECT name, breed FROM dogs;
```

**OOP Equivalent**

```python
[(dog.name, dog.breed) for dog in dogs]
```

---

### Ordering Results

```sql
SELECT * FROM dogs
ORDER BY age DESC;
```

**OOP Equivalent**

```python
sorted(dogs, key=lambda d: d.age, reverse=True)
```

---

### Limiting Results

```sql
SELECT * FROM dogs
LIMIT 5;
```

**OOP Equivalent**

```python
dogs[:5]
```

---

### Aggregation (Asking Summary Questions)

Databases are extremely good at math over large datasets.

---

#### COUNT

```sql
SELECT COUNT(*) FROM dogs;
```

```python
len(dogs)
```

---

#### AVG

```sql
SELECT AVG(age) FROM dogs;
```

```python
sum(d.age for d in dogs) / len(dogs)
```

---

#### GROUP BY

```sql
SELECT breed, COUNT(*)
FROM dogs
GROUP BY breed;
```

**OOP Equivalent**

```python
from collections import defaultdict

groups = defaultdict(int)
for dog in dogs:
    groups[dog.breed] += 1
```

Except SQL does this **faster, safer, and at scale**.

---

## Constraints + Queries = Reliable Systems

When constraints and queries work together:

* Bad data never enters
* Good data is easy to retrieve
* Applications become simpler
* Bugs become harder to create

This is why professional backend systems **trust the database** and build on top of it.

---

## Conclusion

In this lecture, you learned how **constraints** and **queries** transform a database from a passive storage layer into an active guardian and decision-maker within a full-stack system. By framing constraints as the database equivalent of Python setters, you saw how rules like `NOT NULL`, `UNIQUE`, `CHECK`, and foreign keys enforce valid state in the same way well-designed classes protect their attributes. You also explored how SQL queries parallel familiar object-oriented operations—filtering, sorting, aggregating, and grouping data—while operating far more efficiently at scale. Together, constraints and queries establish trust in your data and clarity in how it is accessed, setting the foundation for Django models, migrations, and QuerySets, where these principles are expressed directly through Python code.
