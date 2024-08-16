# Circular Linked Lists

## Introduction

In a circular linked list, the last node points to the first. They are useful for real-world applications such as scheduling and managing playlists. However because the last node points back to the first, keeping track of when we've reached the end of the list is potentially more difficult.

## Lecture

This lesson will focus on a singly-linked circular list. Doubly linked lists can also be circular.

### Creating the List Node

Creating the list node is the same as a singly linked list:

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

## Conclusion