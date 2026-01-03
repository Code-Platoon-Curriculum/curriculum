# Data Structures

---

## Introduction

---

We're already familiar with a number of data structures, especially lists (arrays) and dictionaries (objects).  Learning how to choose the right data structure for a given problem is a big part of solving it, and solving it efficiently.

---

However, there are many more possible data structures besides lists and dictionaries.  We'll look at a few common ones today, namely stacks, queues, and linked lists.  As with any data structure, each of them has its own characteristics which makes it either a more or less appropriate tool for solving a given problem.

---

## Stacks

---

We've seen stacks already.  Any time you run a function you are adding a record to the execution stack, which you can see in the VS Code debugger.  If you try running a recursive function in the debugger, pay attention to how records are added to and removed from the stack.


---

You should find that records are always added to the top of the stack, and records are always removed from the top of the stack as well.  This is called LIFO, or Last In First Out.  <br/>

---

![stack](./page-resources/stack.png)

---

This also means that stacks have only one access point, like some unfortunate animals that have to do two very different things with only one thing: <br/>

---

![cnidarians](./page-resources/cnidarians.jpeg)


Stacks should have (at minimum) the following API:
1. push - add an item to the top
2. pop - remove an item from the top and return that item
3. peek - return the value of the item currently on the top

---

Fortunately, we can create our own custom data types in Python.  Given the above requirements, our `Stack` should start out looking something like this:

```python
class Stack:
    def __init__(self):
        pass

    def push(self):
        pass

    def pop(self):
        pass

    def peek(self):
        pass
```

---

The first thing we need to figure out is the underlying data type we will be pushing onto and popping off of.  The most obvious choice is a list, but there are other options.

```python
class Stack:
    def __init__(self):
        self.base = []

    def push(self):
        pass

    def pop(self):
        pass

    def peek(self):
        pass
```

---

The next step is to implement `push` and `pop`.  This is pretty straightforward using Python list builtins:

```python
class Stack:
    def __init__(self):
        self.base = []

    def push(self, item):
        self.base.append(item)

    def pop(self):
        return self.base.pop()

    def peek(self):
        pass
```

---

Finally, we'll need to implement `peek`.  This is also fairly easy:

```python
class Stack:
    def __init__(self):
        self.base = []

    def push(self, item):
        self.base.append(item)

    def pop(self):
        return self.base.pop()

    def peek(self):
        if self.base:
            return self.base[-1]
        return None
```

You can decide how you handle trying to access an empty `base`.  Here I'm just returning `None`.

---

That's all there is to it.  Try running other Python list methods on a `Stack` instance.  What happens, and why?

---


## Queues

Queues are very similar to stacks, except that you insert from the bottom and remove from the top.  This is more like how a line works (or a queue in British English).  A queue is FIFO, or First In First Out.<br/>

![queue](./page-resources/queue.png)

---

Queues should have (at minimum) the following API:
1. enqueue - add an item to the beginning
2. dequeue - remove an item from the end and return that item
3. peek - return the value of the item currently at the beginning
