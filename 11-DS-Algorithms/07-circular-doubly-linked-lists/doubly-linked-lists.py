class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        # For connecting to the previous node. 
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def append(self, data):
        new_node = Node(data)
        
        # If list is empty
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        
        # Add to end and update pointers
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
    
    def insert_after(self, ref_node, data):
        if not ref_node:
            return
            
        new_node = Node(data)
        
        # Update next pointers
        new_node.next = ref_node.next
        ref_node.next = new_node
        
        # Update prev pointers
        new_node.prev = ref_node
        if new_node.next:
            new_node.next.prev = new_node
        else:
            self.tail = new_node
    
    def delete(self, node):
        if not node:
            return
            
        # Update head if needed
        if node == self.head:
            self.head = node.next
            
        # Update tail if needed
        if node == self.tail:
            self.tail = node.prev
            
        # Update surrounding nodes
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

    def print_forward(self):
        current = self.head
        while current:
            print(current.data, end=" ⟷ ")
            current = current.next
        print("None")

    def print_backward(self):
        current = self.tail
        while current:
            print(current.data, end=" ⟷ ")
            current = current.prev
        print("None")

my_list = DoublyLinkedList()
my_list.append("hello")
my_list.append("world")
my_list.append("its")
my_list.append("sunny")
my_list.insert_after(my_list.head.next, ",") # insert after "hello", "world"

my_list.print_forward() # hello world, its sunny
my_list.print_backward() # sunny its , world hello