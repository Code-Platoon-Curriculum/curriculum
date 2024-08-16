# Doubly Linked Lists

## Introduction

Doubly linked lists are a variation of the Linked List data structure that enable both moving forwards and backwards in a Linked List - traversing the list in both directions. This is useful when frequent insertions and deletions are necessary. The cost is that there is more to keep track of when implementing the data structure.

[SLIDES]

## Lecture

### Each Node Points Forwards and Backwards

Each node in a doubly linked list has a pointer to the next node in the list, and, the previous one:

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Reference to the next node
        self.prev = None  # Reference to the previous node
```

### Keep Track of Both Head and Tail

We are going to keep track of the *tail* (the end) of our doubly linked list, just like we do with the *head*.

This isn't strictly necessary but will make it easier to explore *backwards traversal*, which we will do shortly.

```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None # Keep track of tail of the list to make traversing backwards easier
```

> Singly Linked Lists can also have *tail pointers*. For more information about it's tradeoffs, [read this Stack Overflow Post](https://stackoverflow.com/questions/58824716/how-to-implement-doubly-linked-list-without-using-tail-pointer)

### Operations on Doubly Linked Lists

Just like a singly linked list, these are the basic operations you can perform:

- **Inserting** a new node into the list
- **Deleting** a node from the list
- **Traversing** the list

#### Insertion

There are three possibly ways to insert a new node into the list:

- Insert at the head of the list
- Insert at the tail of the list
- Insert at a given position in the list (before or after a specific node)

We will focus on the first two.

In addition to what we already learned with a singly linked list, the two things we have to keep track of for our doubly linked list when inserting are:

1. Updating `my_node.prev` - each node points both forwards and backwards.
2. Updating the list's tail when necessary.

##### Insertion at Head of List

Note the additional logic to handle updating the tail.

```python
def insert_at_head(self, data):
    new_node = Node(data)
    # List is empty
    if not self.head:
        self.head = new_node
        self.tail = new_node
        return

    # List has at least one element
    new_node.next = self.head
    self.head.prev = new_node # Point head.prev to it's new neighbor to the left.
    self.head = new_node
```


##### Insertion at Tail of List

Because our list keeps track of the tail, inserting at the end of the list is easy. The tradeoff for this is all the extra logic in our code to keep track of the tail.

```python
def insert_at_tail(self, data):
    new_node= Node(data)
    # List is empty
    if not self.head:
        self.head = new_node
        self.tail = new_node
        return

    # List has at least one element
    self.tail.next = new_node
    new_node.prev = self.tail
    self.tail = new_node
```

#### Deletion

Deletion becomes more straightforward. Because each node points to both it's left and right neighbors, we do not need two pointers like we do for a singly linked list.

- Unlike a singly linked list, two pointers are not needed
- We have an extra *edge case* - if the node to delete is the **tail**.

```python
def delete_by_value(self, key):
    # Node to delete is head 
    if self.head.data == key:
        self.head = self.head.next # note that we did not actually dleete the old head, just remove it from the list
        return

    # Node to delete is tail
    if self.tail.data == key:
        self.tail = self.tail.prev # note that we did not actually delete the old tail, just remove it from the list
        return

    # Node to delete is not head or tail
    current_node = self.head
    while current_node and current_node.data != key:
        current_node = current_node.next

    # Node to delete not in list
    if current_node is None:
        return

    # connect left neighbor to right neighbor
    current_node.prev.next = current_node.next
    # connect right neighbor to left neightbor
    current_node.next.prev = current_node.prev

    # Not strictly necessary but a good habit
    current_node = None
```

This implemention traverses the list forwards to find the node to delete. We could also implement a deletion method that traverses the list backwards.

> The implementation for inserting a node at a given point, or after a specific node is not very different than the implementation for deleting a specific node.

#### Traversal

Unlike a singly linked list, a doubly linked list can traverse both forwards and backwards.

##### Forwards Traversal

Forwards traversal is the same as a singly linked list:

```python
def print_list_forwards(self):
    current_node = self.head
    while current_node:
        print(current_node.data, end=" ")
        current_node = current_node.next
```

##### Backwards Traversal

Although keeping track of our list's tail is extra work, it makes backwards traversal very simple.

```python
def print_list_backwards(self):
    current_node = self.tail
    while current_node:
        print(current_node.data, end=" ")
        current_node = current_node.prev
```

## Conclusion

Doubly linked lists are more complex to implement, because each node points both forward and backwards. If we choose to keep track of our lists tail, that also adds complexity to our implementation.

However being able to traverse the list both forwards and backwards makes insertion and deletion more efficient.