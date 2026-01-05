# OOP Methods

## Intro

So far, you’ve learned how to create **classes**, define **instance attributes**, and distinguish between **instance-level** and **class-level** data. The next step in mastering Object-Oriented Programming is understanding **methods**—functions that live inside a class and define **behavior**.

Not all methods are the same. In Python, methods can operate at **different levels of responsibility**:
- On a **specific instance**
- On the **class itself**
- Or independently of both

In this lesson, we’ll explore **instance methods**, **class methods**, and **static methods**, when to use each, and how choosing the right method level leads to cleaner, more maintainable code.

---

## Instance Methods

An **instance method** is the most common type of method. It operates on a **specific instance** of a class and has access to instance attributes through `self`.

### Key Characteristics

- First parameter is always `self`
- Can read and modify instance attributes
- Requires an instance to be called

### Example

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def celebrate_birthday(self):
        self.age += 1
        return f"Happy Birthday! You are now {self.age}."
```

Usage:

```python
person = Person("Alice", 25)
print(person.celebrate_birthday())
```

> **Mental model:**
> Instance methods answer the question:
> **“What can this object do?”**

---

## Class Methods (`cls`)

A **class method** operates on the **class itself**, not a specific instance. Instead of `self`, it receives the class as its first parameter, conventionally named `cls`.

Class methods are defined using the `@classmethod` decorator.

### Key Characteristics

* First parameter is `cls`
* Can access and modify class attributes
* Can be called on the class *or* an instance
* Often used as **alternative constructors**

---

### Creating a Class Method That Will Create Instances

One of the most common and powerful uses of class methods is creating **factory methods**—methods that return new instances of the class.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, data_str):
        name, age = data_str.split(",")
        return cls(name.strip(), int(age))
```

Usage:

```python
person = Person.from_string("Alice, 25")
print(person.name)  # Alice
print(person.age)   # 25
```

Why this matters:

* Encapsulates object creation logic
* Keeps constructors clean
* Makes your code more expressive

> **Mental model:**
> Class methods answer:
> **“What should the class do or know?”**

---

## Class Methods vs Instance Methods

Understanding the distinction between these two method types is crucial.

| Feature                | Instance Method     | Class Method             |
| ---------------------- | ------------------- | ------------------------ |
| First parameter        | `self`              | `cls`                    |
| Operates on            | One specific object | The class as a whole     |
| Accesses instance data | ✅ Yes               | ❌ No                     |
| Accesses class data    | ✅ Yes               | ✅ Yes                    |
| Common use cases       | Object behavior     | Factories, configuration |

> **Rule of thumb:**
> If the behavior depends on **individual object state**, use an instance method.
> If it depends on **class-wide logic**, use a class method.

---

## Static Methods

A **static method** is a method that lives inside a class but does **not** receive `self` or `cls`.

Static methods are defined using the `@staticmethod` decorator.

### Key Characteristics

* No access to instance or class state
* Behaves like a regular function
* Namespaced inside the class for organization

### Example

```python
class Person:
    @staticmethod
    def greet(name):
        return f"Hello {name}"
```

Static methods are useful when:

* The logic conceptually belongs to the class
* The method doesn’t need object or class data

> **Mental model:**
> Static methods answer:
> **“What helper behavior logically belongs here?”**

---

## Best Practices for Choosing Method Level

Choosing the correct method type improves clarity and reduces bugs.

| Question to Ask                            | Use This Method Type |
| ------------------------------------------ | -------------------- |
| Does it operate on instance data?          | Instance Method      |
| Does it affect or create the class itself? | Class Method         |
| Is it utility logic related to the class?  | Static Method        |
| Does it need `self`?                       | Instance Method      |
| Does it need `cls`?                        | Class Method         |
| Needs neither `self` nor `cls`?            | Static Method        |

> **Professional insight:**
> Method type communicates **intent**. Choose the one that best describes responsibility.

---

## Conclusion

In this lesson, you learned how Python supports **three levels of behavior** within classes:

* **Instance methods** define what individual objects can do
* **Class methods** define behavior related to the class as a whole
* **Static methods** provide utility behavior scoped to the class

Understanding and applying the correct method type leads to:

* Cleaner APIs
* Better separation of concerns
* More readable and maintainable code

As your programs grow, these distinctions become increasingly important—and mastering them now sets you up for advanced OOP patterns and professional-grade code design.
