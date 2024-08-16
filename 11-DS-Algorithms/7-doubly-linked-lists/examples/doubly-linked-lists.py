"""
name: Doubly Linked Lists
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Reference to the next node
        self.prev = None  # Reference to the previous node

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None # Keep track of tail of the list to make traversing backwards easier

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

    def print_list_forwards(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" ")
            current_node = current_node.next

    def print_list_backwards(self):
        current_node = self.tail
        while current_node:
            print(current_node.data, end=" ")
            current_node = current_node.prev

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