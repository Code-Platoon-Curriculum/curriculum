class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        
        # If list is empty, make new node the head
        if not self.head:
            self.head = new_node
            new_node.next = self.head  # Point to itself
            return
            
        # Find the last node
        current = self.head
        while current.next != self.head:
            current = current.next
            
        # Add the new node and make it circular
        current.next = new_node
        new_node.next = self.head
    
    def print_list(self):
        if not self.head:
            return
            
        current = self.head
        while True:
            print(current.data, end=" -> ")
            current = current.next
            # avoid infinite loop
            if current == self.head:
                break
        print("(back to start)")

# Lets run our code:
my_list = CircularLinkedList()

my_list.append("hello")
my_list.append("world")
my_list.append("its")
my_list.append("sunny")

my_list.print_list()

def has_cycle(head):
    if not head or not head.next:
        return False
        
    slow = head
    fast = head.next
    
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    
    return False


print(has_cycle(my_list.head)) # True

# Implement a Singly LInked List and use has_cycle() on it
class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def insert_at_end(self, data):
        self.length +=1
        new_node = Node(data)

        # Inserting into empty list
        if not self.head:
            self.head = new_node
            return

        # Add node to end of list
        last_node = self.head

        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node 


    def __repr__(self):
        return f"Length: {self.length}"
    

my_singly_linked_list = LinkedList()
my_singly_linked_list.insert_at_end('goodbye')
my_singly_linked_list.insert_at_end('its')
my_singly_linked_list.insert_at_end('snowy')
print(my_singly_linked_list)

print(has_cycle(my_singly_linked_list.head)) # False