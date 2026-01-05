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

### Understanding Logarithms

Logarithms appear frequently in Big-O—especially with efficient algorithms like binary search.

A **logarithm** answers the question:
> “How many times can I divide this number in half before I reach 1?”

Example:
- `log₂(8) = 3` → because `8 → 4 → 2 → 1`

In algorithms, **Logarithmic time** means the problem size is reduced **dramatically** each step, that is why divide-and-conquer approaches are so powerful and encouraged within programming.

---

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
