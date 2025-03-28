# Recursion

## Intro

By the end of this lesson, you will have a solid understanding of recursion, including its definition, key concepts, and practical application in solving various problems. This lesson will cover important topics related to recursion and provide code examples in Python.

## What is Recursion

Recursion in programming is a technique where a function calls itself in order to solve a problem by breaking it down into simpler instances of the same problem. It involves solving a larger problem by solving smaller instances of the same problem, often leading to more concise and elegant code. Learning recursion is crucial for several reasons. Firstly, it provides a powerful and intuitive approach to problem-solving, allowing for the development of clean and readable code. Secondly, recursion is widely used in various algorithms and data structures, including tree and graph traversal, sorting, and searching. Mastering recursion enhances your understanding of fundamental programming concepts, improves your ability to think recursively and analytically, and forms the foundation for tackling more complex algorithms and dynamic programming challenges. Overall, recursion is an essential skill for any programmer seeking to excel in algorithmic problem-solving and software development.

## How does Recursion help Space and Time Complexity

Recursion can impact Big-O notation and memory usage efficiency depending on how it's implemented. Here are some considerations:

**1. Time Complexity (Big-O):**

- **Improvement:** Recursion can lead to more concise and readable code, simplifying the expression of algorithms. In some cases, this simplicity can result in improved development speed and easier maintenance.
- **Impact:** Poorly designed recursive algorithms may lead to inefficient time complexity. Each recursive call adds a new frame to the call stack, and if not optimized, this can lead to a higher time complexity compared to an iterative solution. Tail recursion and memoization are techniques that can optimize certain recursive algorithms and improve time complexity.

**2. Space Complexity:**

- **Improvement:** Well-optimized recursive algorithms can be more memory-efficient than their iterative counterparts. Techniques like tail recursion, where the recursive call is the last operation in the function, can be optimized by some programming languages to use constant stack space, resulting in better space efficiency.
- **Impact:** Inefficient use of recursion, especially with deep recursion or lack of memoization, can lead to a large call stack, consuming more memory. This can result in a higher space complexity compared to an iterative solution.

**3. Readability and Maintainability:**

- **Improvement:** Recursive code can be more readable and easier to understand, expressing the problem in a way that closely mirrors its mathematical or structural nature. This can lead to improved maintainability and reduced likelihood of introducing bugs during code changes.
- **Impact:** Overly complex recursive functions might be harder to read and understand. It's essential to strike a balance between clarity and efficiency when using recursion.

**4. Dynamic Programming and Memoization:**

- **Improvement:** Recursion, combined with dynamic programming principles and memoization, can significantly improve both time and space complexity. Memoization involves caching previously computed results to avoid redundant computations, resulting in a more efficient algorithm.
- **Impact:** Without memoization, some recursive algorithms may become inefficient due to redundant computations. Introducing memoization can transform a high time complexity into a more efficient solution.

The impact of recursion on efficiency depends on how it is implemented and whether optimization techniques, such as tail recursion or memoization, are employed. While recursion can lead to more elegant and expressive code, it requires careful consideration to ensure efficiency, especially in terms of time and space complexity.

## Building a Recursive Function

Let's write a recursive function that will get us the factorial for a number. The factorial mathematical function (symbol: !) says to multiply all whole numbers from our chosen number down to 1. Some examples are:

$$ 5! = 5 * 4 * 3 * 2 * 1 $$
$$ 4! = 4 * 3 * 2 * 1 $$
$$ 3! = 3 * 2 * 1 $$
$$ 2! = 2 * 1 $$
$$ 1! = 1 $$
$$ 0! = 1 $$

**Note that zero factorial equals one, this is important.**

That is the mathematical factorial operation. Now, let's write a function using recursion to implement it in Python!

### Base Case

The base case is a crucial part of any recursive function. It defines when the recursion should stop and helps prevent infinite loops.

  ```python
  def factorial(n):
      # Base case
      if n == 0 or n == 1:
          return 1
      # Recursive case
      else:
          return n * factorial(n-1)
  ```

### Recursive Case

The recursive case is the part of the function that calls itself. It allows the problem to be broken down into smaller, more manageable subproblems.

### Example: Fibonacci Sequence

The Fibonacci Sequence is the series of numbers:

$$ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...  $$

The next number is found by adding up the two numbers before it:

... the 2 is found by adding the two numbers before it (1+1),
... the 3 is found by adding the two numbers before it (1+2),
... the 5 is (2+3),

and so on!

Example: the next number in the sequence above is 21+34 = 55

```python
  def fibonacci(n):
      # Base cases
      if n == 0:
          return 0
      elif n == 1:
          return 1
      # Recursive case
      else:
          return fibonacci(n-1) + fibonacci(n-2)
```

## The Call Stack

The call stack is a memory structure that keeps track of function calls. Pretty much every programming language, and indeed every operating system, uses a call stack. Understanding the call stack is essential not only for grasping how recursion works, but for grasping how programs, operating systems, and computers work.

Let's visualize this in [Python Tutor](http://www.pythontutor.com/visualize.html#mode=edit). 

  ```python
  def count_down(n):
      if n == 0:
          return
      print(n)
      count_down(n-1)

  count_down(3)
  ```

  > Question: Which lines of code are the base case for this function? Which are the recursive case?

### Review & Challenge: Make Recursive Factorial "Go Up"

Let's review our recursive factorial function, and, see if we can make a few changes.

**Question:** Why do we need `if n == 0` as a part of our base case for `factorial()` - what will fail if we remove it?

> Hint: What input to our function will trigger `if n == 0` in our base case logic?

**Question:** What would happen if our recursive case was `n * factorial(n+1)` ? What problem do we see, and, could we further refactor our recursive algorithm so it could actually work with this as our recursive case?

The problem we encounter is our algorithm "goes up" and goes on forever! **It never stops, because it never hits it's base case!**

It takes a bit of work, but it is indeed possible to design our recursive factorial algorithm to "go up", instead of "go down". Note how:

- Our base case has changed.
- We need to pass a `current` argument to our function, so our base case will know when to stop.
- Our recursive step needs to pass `current` as an argument.

It is common with recursive functions to pass important, consistently changing data like `current` as a function argument to subsequent recursive calls.

```python
def factorial_up(n, current=1):
    # Base case: when current exceeds n, return 1 (end of recursion)
    if current > n:
        return 1
    # Recursive case: multiply current with the factorial of the next number
    return current * factorial_up(n, current + 1)

# Example usage:
n = 5
print(f"The factorial of {n} is: {factorial_up(n)}")
```


## Recursion vs. Iteration

Recursion and iteration are two fundamental approaches to problem-solving in programming. While both are used to repeat a set of instructions, they have distinct characteristics, and choosing between them depends on the nature of the problem and the desired trade-offs.

### Comparing Recursion and Iteration

- Readability vs. Efficiency: Discuss the trade-off between the elegance and readability offered by recursion versus the potential efficiency gained by iteration. Consider scenarios where clarity is crucial, and where optimizing for performance is a higher priority.
- Stack Usage: Highlight the impact on the call stack in recursion and how excessive recursion can lead to a stack overflow. Contrast this with the controlled memory usage in iteration.
- Tail Recursion: Introduce the concept of tail recursion and how it can optimize certain recursive algorithms by allowing some programming languages to reuse the same stack frame.

### Choosing the Right Approach

- Problem Structure: Consider the natural structure of the problem. Recursive solutions often shine in problems with hierarchical or nested structures, while iteration is suitable for linear, sequential tasks.
- Resource Constraints: Assess the available resources, especially memory. If memory efficiency is crucial, iterative solutions might be preferred.
- Language and Paradigm: Understand the language being used and its support for recursion optimization or tail call optimization.

  ```python
  # Recursive approach
  def factorial_recursive(n):
      if n == 0:
          return 1
      else:
          return n * factorial_recursive(n-1)

  # Iterative approach
  def factorial_iterative(n):
      result = 1
      for i in range(1, n+1):
          result *= i
      return result
  ```

## Common Recursion Patterns

Recognize and understand common recursion patterns, such as linear recursion, binary recursion, and multiple recursion.

```python
  # Linear recursion
  def linear_sum(lst):
      if not lst:
          return 0
      else:
          return lst[0] + linear_sum(lst[1:])

  # Binary recursion
  def binary_search(lst, target, low, high):
      if low > high:
          return -1
      else:
          mid = (low + high) // 2
          if lst[mid] == target:
              return mid
          elif lst[mid] < target:
              return binary_search(lst, target, mid+1, high)
          else:
              return binary_search(lst, target, low, mid-1)
  ```

## Practice, Practice, Practice

Solve a variety of problems on coding platforms like LeetCode, HackerRank, or similar websites to reinforce your understanding of recursion.

## Conclusion

Recursion is a powerful and elegant technique for solving complex problems by breaking them down into simpler subproblems. As you continue to practice and apply recursion to various scenarios, you'll gain confidence in your ability to use this fundamental concept in your software engineering journey.

## Resources

- [Python Tutor](http://www.pythontutor.com/visualize.html#mode=edit)
- [Factorial Explanation](https://www.mathsisfun.com/numbers/factorial.html)
- [Fibonacci Sequence Explanation](https://www.mathsisfun.com/numbers/fibonacci-sequence.html)
