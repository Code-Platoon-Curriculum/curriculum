# Understanding Big-O

## Intro

As developers, we often ask questions like:

- *Is this solution fast enough?*
- *How will this behave when the data gets really large?*
- *Why does one algorithm feel instant while another feels painfully slow?*

**Big-O notation** gives us a language to answer those questions.

In this lecture, we will focus on **understanding what Big-O is**, **what it measures**, and—most importantly—**how to quickly identify the time complexity of an algorithm by looking at its structure**. This skill is foundational for writing scalable code and is a core expectation in technical interviews.

---

## What is Big-O Analysis?

![big-o](./resources/Big-O-Chart.png)

**Big-O notation** describes the **growth rate** of an algorithm’s runtime as the size of the input increases.

> Big-O does **not** measure exact execution time.  
> It measures how performance **scales**.

Main aspects of measuring *Big-O* are: thinking about **worst-case scenarios** of for an algorithm action while ignoring constants and small optimizations, but still focus on how runtime grows as `n` (input size) grows.

> “If my input doubles, how much more work does my algorithm do?”

Big-O allows us to compare algorithms **independently of hardware, language, or implementation details**.

---

## Time Complexity vs Space Complexity

Up to this point we have mostly been talking about **time complexity**, which means:

> “How many operations does this algorithm need to do as the input grows?”

But Big-O can also be used to talk about **space complexity**, which means:

> “How much extra memory does this algorithm need as the input grows?”

So when we analyze an algorithm, we are usually thinking about two separate questions:

| Type | Question |
| ---- | -------- |
| **Time Complexity** | How long does this take as `n` grows? |
| **Space Complexity** | How much extra memory does this need as `n` grows? |

The important phrase here is **extra memory**.

We are usually not counting the original input itself. If a function receives a list with 1,000 items, that list already exists before the function starts doing its work. Instead, we care about what additional memory the function creates while it runs.

---
# Space Complexity

### O(1) Space — Constant Space

**Definition:**  
The algorithm only uses a fixed amount of extra memory, no matter how large the input gets.

```python
def get_largest_number(arr):
    largest = arr[0]

    for num in arr:
        if num > largest:
            largest = num

    return largest
```

This function loops through the whole list, so the **time complexity** is:

```text
O(n)
```

But the **space complexity** is:

```text
O(1)
```

Even if the list has 10 items or 10,000 items, we only create one extra variable:

```python
largest
```

That means the memory usage does not grow with the input size.

#### Identifiers

* A few simple variables
* No new list, dictionary, set, or recursive call stack that grows with input
* Memory usage stays basically the same as `n` grows

---

### O(n) Space — Linear Space

**Definition:**  
The algorithm creates extra memory that grows directly with the input size.

```python
def double_numbers(arr):
    doubled = []

    for num in arr:
        doubled.append(num * 2)

    return doubled
```

This function creates a new list called `doubled`.

If the original list has 5 items, `doubled` will have 5 items.  
If the original list has 10,000 items, `doubled` will have 10,000 items.

So the **time complexity** is:

```text
O(n)
```

And the **space complexity** is also:

```text
O(n)
```

The runtime grows because we loop over every item.  
The memory grows because we store a new result for every item.

#### Identifiers

* Creating a new list based on the input
* Creating a new dictionary or set based on the input
* Storing values that grow as the input grows

---

### Recursion and Space Complexity

Recursive functions can also use extra space because each recursive call gets added to the **call stack**.

```python
def countdown(n):
    if n == 0:
        return

    print(n)
    countdown(n - 1)
```

This function has a time complexity of:

```text
O(n)
```

It counts down from `n` to `0`, so the number of calls grows with `n`.

But it also has a space complexity of:

```text
O(n)
```

That is because every recursive call waits on the call stack until the base case is reached.

For example:

```text
countdown(5)
countdown(4)
countdown(3)
countdown(2)
countdown(1)
countdown(0)
```

Each function call is stacked on top of the previous one.

So even though we are not creating a list, dictionary, or set, we are still using memory through the recursive call stack.

#### Identifiers

* Recursive calls
* Function calls waiting for other function calls to finish
* Stack depth grows as the input grows

---

### Binary Search Space Complexity

This is a good example of how two solutions can have the same time complexity but different space complexity.

Iterative binary search:

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return True
        elif target < arr[mid]:
            right = mid - 1
        else:
            left = mid + 1

    return False
```

Recursive binary search:

```python
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return False

    mid = (left + right) // 2

    if arr[mid] == target:
        return True
    elif target < arr[mid]:
        return binary_search_recursive(arr, target, left, mid - 1)
    else:
        return binary_search_recursive(arr, target, mid + 1, right)
```

Both versions have the same time complexity:

```text
O(log n)
```

That is because both versions cut the search area in half each time.

But they have different space complexity:

| Version | Time Complexity | Space Complexity |
| ------- | --------------- | ---------------- |
| While loop binary search | O(log n) | O(1) |
| Recursive binary search | O(log n) | O(log n) |

The while loop version only needs a few variables:

```python
left
right
mid
```

So its space complexity is `O(1)`.

The recursive version creates a new function call each time it searches a smaller half of the list. Since binary search cuts the input in half each time, the call stack grows at a rate of `O(log n)`.

---

## Space Complexity Cheat Sheet

| Pattern in Code | Likely Space Complexity |
| --------------- | ----------------------- |
| A few variables only | O(1) |
| New list based on input | O(n) |
| New dictionary or set based on input | O(n) |
| Recursive function with one call each step | Usually O(n) |
| Recursive function that halves the problem each step | Usually O(log n) |
| Recursive branching with many calls | Can become O(n), O(2ⁿ), or worse depending on what is stored |

---

## Key Takeaway

When analyzing Big-O, we should ask two questions:

```text
How much time does this take?
How much extra memory does this use?
```

A solution can be good on time but expensive on space, or it can save memory but take longer to run.

As developers, we are often making tradeoffs between speed and memory. Big-O helps us talk about those tradeoffs clearly.

---

### Understanding Logarithms

Logarithms appear frequently in Big-O—especially with efficient algorithms like binary search.

A **logarithm** answers the question:
> “How many times can I divide this number in half before I reach 1?”

Example:
- `log₂(8) = 3` → because `8 → 4 → 2 → 1`

In algorithms, **Logarithmic time** means the problem size is reduced **dramatically** each step, that is why divide-and-conquer approaches are so powerful and encouraged within programming.

---
# Time Complexity

## Big-O In Action

Let’s walk through the most common Big-O complexities you’ll encounter, what they look like in code, and how to recognize them quickly, again the point of this lesson is not for you to learn each algorithm but to look for key factors like nested for loops or division of iterable ds at each iteration to quickly recognize what the Big-O complexity of an algorithm is at it's current state.

---

### O(1) — Constant Time

**Definition:**  
The algorithm always takes the same amount of time, regardless of input size. Accessing iterable data by index is a constant time operation, just like accessing a value of a dictionary by it's key is also instant time.

```python
def get_first_item(arr):
    return arr[0]
```

#### Identifiers

* Direct access
* No loops
* No recursion

✅ Fastest possible complexity
✅ Ideal for performance-critical operations

---

### O(n) — Linear Time

**Definition:**
Runtime grows directly with input size. This means that if my input size is 1,000 than the number of operations that need to happen are also 1,000.

```python
def linear_search(arr, target):
    for item in arr:
        if item == target:
            return True
    return False
```

#### Identifiers

* Single loop
* Iterates over entire dataset

---

### O(log n) — Logarithmic Time

**Definition:**
Runtime grows slowly as input size increases. Usually applied by a divide and conquer behavior where at each iteration we cut the searching data structure by half.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return True
        elif target < arr[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return False
```

#### Identifiers

* Dividing input in half
* Binary search
* Tree traversal

✅ Extremely efficient
⚠️ Usually requires sorted data

---

### O(n log n) — Linearithmic Time

**Definition:**
Combines linear work with logarithmic splitting and leverage other programming concepts like *recursion*. This means that if my number of input is 100 well I would need at minimum 100 operation but at it's worse scenario I would need 664 operations. It's not doubling to 1,000 which is the outcome you may expect for having nested operations. This is only achievable because of the recursive call stack.

Common examples are algorithms like `Merge Sort` or `Quick Sort`. Let's take a look at *Quick Sort*:

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

data = [3, 6, 8, 10, 1, 2, 1]
print(quicksort(data))
```

You can easily see the division of the iterable object between left, middle and right and then the concept of recursion within the return statement itself.

#### Identifiers

* Divide-and-conquer algorithms
* Recursive splitting + iteration

```python
# Conceptual example (merge sort behavior)
split data → process halves → merge results
```

> Often the **best achievable complexity for sorting**.

---

### O(n²) — Quadratic Time

**Definition:**
Runtime grows with the square of the input size. Meaning that at every iteration there is two separate operations so we are doubling our operations. If the input size is 100 than the operations needed would be 10,000.

```python
def print_pairs(arr):
    for i in arr:
        for j in arr:
            print(i, j)
```

#### Identifiers

* Nested loops over the same dataset
* Comparing every element to every other element

⚠️ Becomes slow very quickly
❌ Poor scalability

---

### O(2ⁿ) — Exponential Time

**Definition:**
Runtime doubles with each additional input. This is really inefficient and if the input size was 100 than the number of operations that would happen are 1,267,650,600,228,229,401,496,703,205,376. You can see how this dramatically hurts our efficiency.

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

#### Identifiers

* Recursive calls branching multiple times
* Recalculating the same values repeatedly

❌ Extremely inefficient
❌ Not viable for large inputs

---

### O(n!) — Factorial Time

**Definition:**
Runtime grows faster than exponential time.

A common example would be an algorithms that is attempting to generate all permutations of a list

#### Identifiers

* Algorithms that try **every possible ordering**
* Bruteforce solutions to permutation problems

❌ Worst practical complexity
❌ Only usable for very small inputs

---

## Quick Identification Cheat Sheet

| Pattern in Code     | Likely Big-O |
| ------------------- | ------------ |
| No loops            | O(1)         |
| One loop            | O(n)         |
| Loop with halving   | O(log n)     |
| Loop + halving      | O(n log n)   |
| Nested loops        | O(n²)        |
| Recursive branching | O(2ⁿ)        |
| All permutations    | O(n!)        |

---

## Conclusion

Big-O analysis helps us think beyond “does this work?” and ask:

> “Will this still work **at scale**?”

In this lesson you learned about Big-O notation, how to quickly look at different algorithms and recognize how to quickly recognize an algorithms Big-O complexity by identifying key coding patterns.

As we continue deeper into Data Structures & Algorithms, **Big-O will be the lens through which we evaluate every solution**—both in real-world systems and technical interviews.

## [Assignments](./assignments.md)
