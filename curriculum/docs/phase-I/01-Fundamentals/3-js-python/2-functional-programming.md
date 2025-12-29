# Functional Programming

## Intro

As programs grow beyond simple scripts, we need structured ways to **control flow**, **transform data**, and **reuse logic**. Functional programming concepts give us those tools. While JavaScript and Python are not purely functional languages, they both heavily support **functional patterns** that are used daily in professional codebases.

In this lecture, we focus on **decision-making**, **iteration**, and **functions**—the building blocks that allow programs to react to data, repeat behavior, and encapsulate logic. These concepts are foundational and will appear everywhere: backend APIs, frontend applications, data processing pipelines, automation scripts, and technical interviews.

Rather than memorizing syntax, the goal is to understand **when and why** each construct is used.

---

## Comparison Operators

Comparison operators allow programs to **compare values** and produce a boolean result (`true/false`). These operators are most commonly used inside **conditional statements** and **loops**.

Common comparison operators in **both JavaScript and Python** include:

- Equality (`==` or `===` in JS)
- Inequality (`!=`)
- Greater than / Less than (`>`, `<`)
- Greater than or equal to / Less than or equal to (`>=`, `<=`)

**JavaScript Example:**

```js
let age = 18;
console.log(age >= 18);
````

**Python Example:**

```py
age = 18
print(age >= 18)
```

> **Scenario:**
> Comparison operators are used when validating user input, checking permissions, filtering data, or determining execution paths.

---

## Conditional Statements

Conditional statements allow a program to **branch execution** based on conditions. They answer the question: *“If this is true, what should happen?”*

**JavaScript Example:**

```js
let score = 85;

if (score >= 70) {
  console.log("Pass");
} else {
  console.log("Fail");
}
```

**Python Example:**

```py
score = 85

if score >= 70:
    print("Pass")
else:
    print("Fail")
```

> **Scenario:**
> Conditionals are everywhere—authentication checks, feature flags, error handling, game logic, and API responses.

---

## Iterations

Iteration allows a program to **repeat an action** over a sequence of data. This is critical for working with collections such as lists, arrays, strings, and objects.

---

### Iterating a List / Array or String

#### Iteration by Value

This is the most common and readable approach when you only care about the values.

**JavaScript Example:**

```js
let colors = ["red", "green", "blue"];

for (let color of colors) {
  console.log(color);
}
```

**Python Example:**

```py
colors = ["red", "green", "blue"]

for color in colors:
    print(color)
```

> **Scenario:**
> Use this when transforming or inspecting each item in a collection.

---

#### Iteration by Index

Sometimes you need the **position** of an element, not just the value.

**Python Example:**

```py
colors = ["red", "green", "blue"]

for idx in range(len(colors)):
    print(idx, colors[idx])
```

##### The `range()` Function (Python)

`range()` generates a sequence of numbers and is commonly used for controlled iteration.

```py
for i in range(3):
    print(i)
```

> **Scenario:**
> Index-based iteration is useful when modifying elements by position or synchronizing multiple lists.

---

### Iterating by Both Index and Value

Python provides `enumerate()` to cleanly access both index and value.

```py
colors = ["red", "green", "blue"]

for idx, color in enumerate(colors):
    print(idx, color)
```

> **Scenario:**
> This is preferred over manual index tracking for readability and safety.

---

### Iterating Through a Dictionary / Object

#### Iterating by Keys

**JavaScript Example:**

```js
let user = { name: "Alex", age: 30 };

for (let key in user) {
  console.log(key);
}
```

**Python Example:**

```py
user = {"name": "Alex", "age": 30}

for key in user:
    print(key)
```

---

#### Iterating by Keys and Values

**JavaScript Example:**

```js
for (let [key, value] of Object.entries(user)) {
  console.log(key, value);
}
```

**Python Example:**

```py
for key, value in user.items():
    print(key, value)
```

> **Scenario:**
> This pattern is common when processing structured data such as API responses or configuration files.

---

### While Loop (Use With Care)

A `while` loop continues execution **until a condition becomes false**.

**JavaScript Example:**

```js
let count = 0;

while (count < 3) {
  console.log(count);
  count++;
}
```

**Python Example:**

```py
count = 0

while count < 3:
    print(count)
    count += 1
```

> **Important:**
> `while` loops are powerful but risky. If the condition never becomes false, you create an **infinite loop**. They are best used when the number of iterations is not known ahead of time.

---

## Functions (Parameters & Arguments)

Functions allow you to **encapsulate reusable logic**. They are one of the most important tools in programming.

---

### Declaring a Function

**JavaScript Example:**

```js
function greet(name) {
  console.log("Hello " + name);
}
```

**Python Example:**

```py
def greet(name):
    print("Hello " + name)
```

---

### Calling a Function

```js
greet("Alex");
```

```py
greet("Alex")
```

> **Parameters** are placeholders.
> **Arguments** are the actual values passed in.

---

### The Return Statement

The `return` statement sends a value **back to the caller** and ends the function execution.

**JavaScript Example:**

```js
function add(a, b) {
  return a + b;
}
```

**Python Example:**

```py
def add(a, b):
    return a + b
```

> **Scenario:**
> Use `return` when the result needs to be reused elsewhere in your program.

---

### Arrow Functions (JavaScript Only)

Arrow functions provide a **shorter syntax** and are commonly used in functional patterns.

```js
const multiply = (a, b) => a * b;
```

> **Scenario:**
> Arrow functions are heavily used in callbacks, array methods, and modern frontend code.

---

### Lambda Functions (Python Only)

Lambda functions are **anonymous, one-line functions**.

```py
multiply = lambda a, b: a * b
```

> **Scenario:**
> Lambdas are commonly used with `map`, `filter`, and sorting operations.

---

## Leveraging Built-In Functional Tools

Functional programming shines when working with collections.

---

### Filter / `filter()`

Filters elements based on a condition.

**JavaScript Example:**

```js
let nums = [1, 2, 3, 4];
let evens = nums.filter(n => n % 2 === 0);
```

**Python Example:**

```py
nums = [1, 2, 3, 4]
evens = list(filter(lambda n: n % 2 == 0, nums))
```

---

### Sorted / `sort()`

Sorts data.

**JavaScript Example:**

```js
let nums = [3, 1, 4, 2];
nums.sort((a, b) => a - b);
```

**Python Example:**

```py
nums = [3, 1, 4, 2]
sorted_nums = sorted(nums)
```

---

### Map / List Comprehension

Transforms each element in a collection.

**JavaScript Example:**

```js
let doubled = nums.map(n => n * 2);
```

**Python List Comprehension Example:**

```py
doubled = [n * 2 for n in nums]
```

> **Scenario:**
> These patterns are heavily used in data processing, frontend state updates, and API response transformations.

---

## Conclusion

Functional programming concepts provide a powerful mental framework for writing clean, expressive, and maintainable code. Comparison operators and conditionals let programs make decisions, iteration allows them to process collections, and functions encapsulate logic into reusable units.

By learning these ideas in both JavaScript and Python, you build language-agnostic problem-solving skills that transfer across the entire software stack. These patterns will reappear constantly as you move into backend development, frontend frameworks, data processing, and technical interviews.
