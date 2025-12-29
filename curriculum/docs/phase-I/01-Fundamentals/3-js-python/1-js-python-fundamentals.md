# JS & Python Fundamentals

## Intro

Modern software engineering rarely relies on a single programming language. Instead, engineers choose tools based on the problem they are solving. JavaScript and Python are two of the most widely used languages in the world, and together they cover an enormous portion of today’s software landscape.

In this lecture, we introduce **JavaScript** and **Python**, explain why both are beginner-friendly yet professionally powerful, and establish a shared foundation for understanding how programming languages work at runtime. Rather than treating them as competitors, we will frame them as **complementary tools** that often coexist within the same system.

---

## Why JavaScript?

JavaScript is one of the most impactful programming languages ever created because it runs **directly in the browser**. Originally developed in the mid-1990s to make web pages interactive, JavaScript quickly evolved from simple button click handlers into a full-featured programming language capable of powering entire applications.

For new programmers, JavaScript offers immediate feedback and visibility. Code you write can instantly affect what users see and interact with on a webpage. This tight feedback loop makes learning engaging and reinforces cause-and-effect relationships between code and behavior.

Today, JavaScript is far more than a browser scripting language. Modern frameworks such as **React**, **Vue**, and **Angular** allow developers to build complex, state-driven user interfaces. These frameworks abstract much of the complexity of directly manipulating the **DOM (Document Object Model)**, which represents the structure of a webpage in memory. While you won’t interact deeply with the DOM immediately, it’s important to know that JavaScript is the language that connects user actions to visual changes on the screen.

JavaScript is also used on the server through platforms like **Node.js**, enabling developers to write full-stack applications using a single language. This versatility is powerful but can introduce challenges. Common obstacles include asynchronous programming, understanding event-driven execution, and managing rapidly evolving tooling. These challenges are normal—and learning to reason about them is part of becoming a professional developer.

---

## Why Python?

Python was created with a different philosophy: **readability and simplicity first**. Developed in the late 1980s and early 1990s, Python emphasizes clear syntax that closely resembles human language. This makes it an excellent entry point for new programmers who want to focus on logic rather than syntax overhead.

Python is widely used across many domains. In **data analytics**, Python dominates due to libraries like NumPy, pandas, and matplotlib. In **machine learning and AI**, frameworks such as TensorFlow and PyTorch rely heavily on Python. On the server side, frameworks like **Django** and **Flask** allow developers to build robust backend systems, APIs, and full web applications.

For beginners, Python’s main benefit is how quickly it allows you to express ideas. You can often write fewer lines of code to achieve the same result as other languages. However, Python also presents challenges. Developers must learn to manage whitespace-based syntax, understand dynamic typing, and reason about performance trade-offs when scaling applications.

---

## Common Ground

![common](./resources/common.png)

Despite their differences, JavaScript and Python share important similarities. Both are **interpreted, runtime languages**, meaning code is executed line-by-line at runtime rather than fully compiled ahead of time. This allows for rapid iteration, experimentation, and interactive debugging.

Both languages rely on a runtime environment (Node.js for JavaScript, the Python interpreter for Python) to execute code. They support variables, control flow, functions, and data structures in conceptually similar ways. Learning one builds transferable skills that make learning the other significantly easier.

---

## Key Differences

![diff](./resources/diff.png)

At a high level, JavaScript and Python differ in how they approach execution and design philosophy. JavaScript is deeply tied to **event-driven programming** and asynchronous behavior, especially in web environments. Python is more linear and often emphasizes sequential execution.

JavaScript was shaped by the needs of browsers and user interaction, while Python was shaped by clarity and general-purpose computing. These origins influence how developers write and structure programs, even when the underlying logic is similar.

---

## Variables

Within these two languages we will hear some common references to **variables**, **functions**, and **classes**, but each one of these will carry it's unique type of naming convention. 

Firs off, what is a **variable**? Think of variables as empty boxes with a label, these boxes are meant to be efficient so we will always place some form of data within this box. The meaningful part about these variables are their labels and how we will go about filling out their labels depending on the language we are working in.

![vars](./resources/variables.png)

* **JavaScript** typically uses **camelCase**:

        ```js
        let userName = "Alex";
        ```

> if you are familiar with JS you may have questions about `const`, `var` and `let` we will address these later on but for now please continue to utilize `let` to establish your variables.

* **Python** typically uses **snake_case**:

        ```py
        user_name = "Alex"
        ```

> other than the naming convention, you may notice that Python has no key word for establishing a variable instead it utilizes the `=` as an identifier for an assignment.

Other conventions you may encounter include:

* **PascalCase** (often for classes)
* **UPPER_CASE** (often for constants)

Naming conventions matter because they communicate intent and help teams read code consistently.

---

## Docker Set Up

Because JavaScript and Python rely on different runtimes, Docker allows us to define those environments explicitly.

### Node.js Dockerfile Example

```Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY example.js .
CMD ["node", "example.js"]
```

This Dockerfile creates a Node.js environment, copies a JavaScript file into the container, and runs it using the Node runtime.

---

### Python Dockerfile Example

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY example.py .
CMD ["python3", "example.py"]
```

This Dockerfile defines a Python environment and executes a Python script. Notice how Docker allows us to switch languages simply by changing the base image.

---

## Primitive Data Types

A **primitive data type** represents a single, indivisible value. These are the basic building blocks of all programs and are rather straight forward with their applications.

---

### Strings

A **string** is a sequence of characters used to represent text. Keep in mind these characters must be wrapped by either `""` or `''` marks. In order to avoid running into weird punctuation issues within a string we recommend you establish your strings with `""` moving forward.

**JavaScript Example:**

```js
let message = "Hello, world!";
console.log(message);
```

> note the `console.log()` function is a built in tool within JavaScript for *logging* content onto the *console* where this code is being executed.

**Python Example:**

```py
message = "Hello, world!"
print(message)
```

> the `print()` function is a built in tool within Python for printing content onto the terminal where code is being executed.

Strings support many built-in methods for manipulation.

- Reference: [https://www.w3schools.com/js/js_string_methods.asp](https://www.w3schools.com/js/js_string_methods.asp)
- Reference: [https://www.w3schools.com/python/python_strings.asp](https://www.w3schools.com/python/python_strings.asp)

---

### Numbers and Integers

Numbers represent numeric values used for counting and calculation and are not wrapped by any special character.

**JavaScript Example for Numbers:**

```js
let count = 10;
console.log(count);
```

**Python Example for Integers:**

```py
count = 10
print(count)
```

Reference:

- [https://www.w3schools.com/js/js_numbers.asp](https://www.w3schools.com/js/js_numbers.asp)
- [https://www.w3schools.com/python/python_numbers.asp](https://www.w3schools.com/python/python_numbers.asp)

---

### Booleans

A **boolean** represents a truth value: `true` or `false` and are also not wrapped by any special character.

**JavaScript Example:**

```js
let isActive = true;
console.log(isActive);
```

**Python Example:**

```py
is_active = True
print(is_active)
```

> Note the key difference in booleans within JavaScript and Python is the capitalization of the first letter of the boolean value i.e. `True` or `False` in Python and `true` or `false` in JavaScript.

Reference:

- [https://www.w3schools.com/js/js_booleans.asp](https://www.w3schools.com/js/js_booleans.asp)
- [https://www.w3schools.com/python/python_booleans.asp](https://www.w3schools.com/python/python_booleans.asp)

---

### Null and None

These represent the intentional absence of a value meaning this variable is intentionally empty.

**JavaScript Example:**

```js
let data = null;
console.log(data);
```

**Python Example:**

```py
data = None
print(data)
```

---

### Python Only – Float

A **float** represents a number with a decimal point, in JavaScript decimal numbers are still numbers but in Python they're treated separately.

```py
price = 9.99
print(price)
```

Reference: 

- [https://www.w3schools.com/python/python_numbers.asp](https://www.w3schools.com/python/python_numbers.asp)

---

### JavaScript Only – Undefined

`undefined` means a variable has been declared but not assigned a value.

```js
let value;
console.log(value);
```

---

## Complex Data Types

Complex data types group multiple values together. And their application may become a bit more complex due to many reasons.

---

### Arrays and Lists

![lists](./resources/lists.png)

A list (Python) or array (JavaScript) stores ordered collections of all data types. Meaning we could have a mixture of strings, integers, booleans all stored within a list.

A key concept about a list is that they're *iterable* data structures, meaning you can access specific *slots/indexes* within the list by calling it's numerical placement in the list starting from 0.

**JavaScript Example:**

```js
// idxs         0       1       2
let colors = ["red", "green", "blue"];
console.log(colors);
console.log(colors[1])
```

**Python Example:**

```py
# idxs      0       1        2
colors = ["red", "green", "blue"]
print(colors)
print(colors[0])
```

> It is important to not that accessing a slot within the list happens in instant time.

Reference:

- [https://www.w3schools.com/js/js_arrays.asp](https://www.w3schools.com/js/js_arrays.asp)
- [https://www.w3schools.com/python/python_lists.asp](https://www.w3schools.com/python/python_lists.asp)

---

### Objects and Dictionaries

![Dictionaries](./resources/dictionaries.png)

These store data as key-value pairs meaning that every value can only be accessed by it's dedicated key.

**JavaScript Object:**

```js
let user = { name: "Alex", age: 30 };
console.log(user);
console.log(user.name)
```

**Python Dictionary:**

```py
user = {"name": "Alex", "age": 30}
print(user.get('name'))
```

Reference:

- [https://www.w3schools.com/js/js_objects.asp](https://www.w3schools.com/js/js_objects.asp)
- [https://www.w3schools.com/python/python_dictionaries.asp](https://www.w3schools.com/python/python_dictionaries.asp)

---

#### Objects vs Dictionaries

While similar in purpose, objects and dictionaries differ in usage and have a bit of syntaxual sugar that can make exchanging between them a hassle.

* **JavaScript objects** often use dot notation to access Object values:

        ```js
        user.name
        ```

* **Python dictionaries** use key access methods that call the key to grab a value:

        ```py
        user.get("name")
        ```

JavaScript objects allow property access without string keys, while Python dictionaries explicitly use keys, reinforcing intentional access patterns.

Additionally both of them can generate new items with the following syntax known as bracket notation:

```python
my_dict = {
    "first_name": "John",
    "last_name": "Doe"
}

my_dict["middle_initial"] = "M"

my_dict["is_ok"] = False

del my_dict["is_ok"]
```

---

## Mutable vs Immutable

![mutant](./resources/mutant.png)

It is important we understand in which data structures we can change the original data and how in others we must make a copy with a partial or edited version of the original data. This concept is known as mutable and immutable data structures:

**Mutable** data types can be changed after creation.
**Immutable** data types cannot.

An easier way to remember this is by understanding that `mutable` is like a `mutant` like Wolverine they are mutated to have special abilities.

| Mutable                | Immutable |
| ---------------------- | --------- |
| Lists / Arrays         | Strings   |
| Dictionaries / Objects | Numbers   |
| Sets                   | Booleans  |

Understanding mutability helps prevent bugs related to shared state and unexpected changes.

---

## Conclusion

JavaScript and Python are foundational languages that open doors across the software industry. While they differ in syntax, philosophy, and runtime environments, they share core programming concepts that transfer easily between them. By learning both, you gain flexibility—front-end interactivity with JavaScript, backend logic and data processing with Python. Together, they form a powerful toolkit that you will continue to build upon throughout your development journey.
