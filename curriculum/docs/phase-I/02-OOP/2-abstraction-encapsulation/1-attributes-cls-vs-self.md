# Class vs Instance Attributes

**<a href="https://docs.google.com/presentation/d/1-BcmDpQ32uS7J7dOLPRVNQei4rAhCI87bz4zJQtmlYs/edit?usp=drive_link" target="_blank" rel="noopener noreferrer">Lecture PowerPoint</a>**

## Intro

Up to this point, you’ve learned how to define **classes**, create **instances**, and manage data using **instance attributes** with getters and setters. This has allowed each object to maintain its own state safely and predictably.

In this lesson, we’ll introduce a new concept: **class attributes**. While instance attributes belong to *individual objects*, class attributes belong to the *class itself* and are **shared across all instances**.

Understanding the difference between **instance-level data** and **class-level data** is critical for writing scalable, memory-efficient, and intention-revealing object-oriented code.

---

## Review of Instance Attributes

Before introducing class attributes, let’s reinforce what we already know.

### What is an Instance?

An **instance** is a concrete object created from a class blueprint.

```python
person = Person("Alice", 25)
```

Here:

* `Person` is the class (the blueprint)
* `person` is an instance (a real object created from that blueprint)

Each instance gets its **own copy of instance attributes**.

---

### Instance Attributes and `self`

Instance attributes are defined and accessed using `self`.

```python
self.name = name
self.age = age
```

Key points:

* `self` refers to the **specific instance** currently being worked on
* Each instance stores its own values
* Modifying one instance does **not** affect others

Example:

```python
alice = Person("Alice", 25)
bob = Person("Bob", 30)

print(alice.name)  # Alice
print(bob.name)    # Bob
```

Even though both objects come from the same class, their data is **isolated**.

> **Mental model:**
> Instance attributes describe *what makes this object unique*.

---

## Class Attributes

A **class attribute** is defined **directly on the class**, outside of `__init__`, and is **shared by all instances**.

Example:

```python
class Person:
    species = "Human"  # class attribute

    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Now observe how it behaves:

```python
alice = Person("Alice", 25)
bob = Person("Bob", 30)

print(alice.species)  # Human
print(bob.species)    # Human
print(Person.species) # Human
```

Key characteristics of class attributes:

* Stored once, on the class
* Shared across all instances
* Accessible via both the class and instances
* Best suited for **shared, universal data**

---

## Why Class Attributes

Class attributes are useful when data:

* Is the **same for every instance**
* Represents a **shared rule, constant, or configuration**
* Should not belong to any one specific object

### Example: Tracking All Instances

```python
class Person:
    population = 0  # class attribute

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.population += 1
```

Usage:

```python
p1 = Person("Alice", 25)
p2 = Person("Bob", 30)

print(Person.population)  # 2
```

Here:

* `population` belongs to the class
* Every new instance updates the same shared value

### Common Use Cases

* Counters (number of users, objects created)
* Constants (`MAX_SIZE`, `DEFAULT_ROLE`)
* Configuration values
* Shared metadata

> **Professional insight:**
> If the data describes *the group*, not *the individual*, it belongs on the class.

---

## Instance vs Class Attributes (Quick Comparison)

| Attribute Type     | Belongs To | Stored Where  | Shared? |
| ------------------ | ---------- | ------------- | ------- |
| Instance Attribute | Object     | Each instance | ❌ No    |
| Class Attribute    | Class      | Class itself  | ✅ Yes   |

---

## Important Gotcha: Shadowing Class Attributes

If you assign to an attribute on `self` with the same name as a class attribute, you **create an instance attribute** instead of modifying the class attribute.

```python
class Person:
    species = "Human"

alice = Person("Alice", 25)
alice.species = "Mutant"

print(alice.species)   # Mutant (instance attribute)
print(Person.species)  # Human (unchanged)
```

This is called **attribute shadowing**.

> **Rule of thumb:**
> Modify class attributes using the class name, not `self`.

---

## Conclusion

In this lesson, you learned the difference between **instance attributes** and **class attributes**, a foundational concept in object-oriented programming.

You should now understand:

* What an instance is and how it stores unique data
* How `self` connects methods and attributes to a specific object
* What class attributes are and how they are shared
* When to use instance attributes vs class attributes
* Common real-world use cases for class-level data

Mastering this distinction helps you design clearer, more intentional classes—and prepares you for advanced topics like inheritance, class methods, and design patterns.

> **Takeaway:**
> Instance attributes define *who this object is*.
> Class attributes define *what all objects have in common*.
