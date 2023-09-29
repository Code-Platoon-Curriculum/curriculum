# How Computer Memory Works, Arrays, and Big-O

## What are we trying to accomplish

Today we are introducing concepts - how computer memory works, Arrays, complexity analysis and Big-O - that we will return to throughout the module. The concepts you learn today you will continue to use in this module to evaluate different kinds of programs and their performance tradeoffs.

This is also foundational knowledge which you will be expected to be familiar with in technical interviews, even if you don't use it on a daily basis at your job.

Lastly, these foundations will set you up to continue learning about computing and computer science after graduation in order to have a successful career.

## Lessons & Assignments

1. [Lesson: How computer memory works & arrays](./how-memory-works-arrays/README.md)
2. [Lesson: Complexity analysis: time complexity, space complexity](./complexity-analysis/README.md)
3. Lesson: Big-O

## Topics Covered

- (Meta) What is the purpose of the Data Structures module?
  - The tech interview
  - Foundational knowledge
- The memory model - how a computer actually works
  - Arrays
- Big-O and an intro to complexity analysis

## TLO's (Testable Learning Objectives)

- Able to analyze Big-O of simple programs using arrays and other primitive data structures for:
  - O(n) programs
  - O(n^2) programs
  - O(1) programs

## ELO's (Elective Learning Objectives)

- Able to explain the basic idea of complexity analysis: Time complexity, space complexity.
- Able to explain what Big-O is and why it matters.
- Able to explain the basics of how computers store things in memory.
- Able to explain what an Array is, and explain to them why a JS array is not a real Array.




### Slidedeck

[Data Structures Slides](https://docs.google.com/presentation/d/1Ua5oUr6mXy04ADOAZFOfy6MTAqNcqbfoOjl7fQG-M6Q/edit?usp=sharing)

### (Meta) What is the purpose of Data Structures week for Code Platoon students?

It is important to contextualize this module's material a little bit as it can feel somewhat out of place with respect to the rest of the course. Most of what we cover in this course fits into the topic of 'software development' - i.e. the practical dicipline of creating useful software. In the first two weeks you skill up in the main language we work with, Python, and then Week 4 through 10 we learn all the practical tools necessary for fullstack web development, things like:

- HTML/CSS/JS for building a basic (minimally-interactive) frontend
- React for building a modern (highly-interactive) frontend
- SQL for databases
- Django for building a 'backend' web server and API
- Deployment

### The memory model - how a computer actually works

In order to learn specific Data Structures, it's important we can do a little complexity analysis first. And in order to do this, it's important we understand a little about how memory in a computer actually works on a physical level, as this determines what is and isn't efficient to do on a computer.

Memory in a computer can be thought of as a contiguous block of identically sized 'slots', like so:

![memory](./page-resources/memory.png)

Think of memory like a single long street, with plots of land of identical size, one after the other.

Like a street, we can think of each spot in memory as having an 'address', and in this case the address is relative to the beginning of the street, and the size of a plot of land.

![memory addresses](./page-resources/memory-adresses.png)

What I have described here is an example of a 32-bit architecture - i.e. the standard size of a 'thing' in this memory structure is 32 bits, or 4 bytes. In reality memory addresses are usually described in terms of hexadecimal, so you will often see a memory address look like '0x1047cc0f0'. Even though we don't usually consider memory locations in a high-level language like Python, we can see this concept with the built in `id()` function.

```py
x = 1 # create a variable called x and store a 1 in it
id(x) # the memory location of x, as a decimal (4370252016)
hex(id(x)) # the memory location of x, as hexadecimal (0x1047cc0f0)
```

For the purposes of this lesson we will assume that all primitive values we represent in memory (integers, floats, characters, booleans) can fit within this amount of space. Bigger things could obviously be store in multiple of these locations one next to the other, but this point will be important once we start talking about arrays.

So for example, if 32-bits represents a single slot in memory, and an individual character can be stored in a single slot, a string might look like this in memory:

![hello memory](./page-resources/hello-memory.png)

Now that we understand the basic structure of computer memory, we can move on to the most essential data structure - Arrays!

### Arrays

Javascript has a data type called array and Python has a data type called a list, and both of these types roughly approximate the concept of an Array, but are ultimately more powerful that the base idea in data structure speak. For now, let's consider the concept of an array in the abstract.

An **Array** is a collection of elements of the same data type that are stored at contiguous memory locations. An example:

```py
nums = [1, 4, 12, 7, 2]
```

![num array](./page-resources/num-array.png)

`nums` is a variable that _refers_ to the array. In DS-speak we call this a _pointer_. A pointer refers to a specific address in memory, so in this example the pointer `nums` holds the memory address `0`.

So why is it important that in an Array the values are contiguous blocks of memory all of the same size? Well, let's consider what is actually happening when you index an array.

```py
nums[0] # 1
nums[2] # 12
nums[4] # 2
```

Indexing is actually just a quick mathematical operation. To get the memory location of an index in an array we evaluate an equation like:

```sh
memory_address_of_beginning_of_arr + index_desired * size_of_each_thing_in_array
```

So to get the value of `nums[4]` we take the beginning memory location of `nums` and add `4 * sizeof(int)`. Because we established that an int is 32 bits, that means the memory address of `nums[4]` is: `0 + 4 * 32 = 128`. And indeed it is!

This property of the memory being in order and holding same-sized objects is necessary because it's what allows us to 'jump' to the 4-th index without having to actively look through the previous elements.

### Analysis

This is a good time to explain the basics of complexity analysis. Imagine for a moment we didn't have this property of contiguous + same sized slots. If that were the case we would need to walk from the beginning of the list and count the # of elements one at a time until we got to the fourth. This would be an example of a _linear time_ operation, or in Big-O terms: `O(N)`. This means that, if the array had length N (for any N), the _worst case scenario_ to find a specific index is N operations. So if our array was of size 1000 and we wanted to see the last element, we would need to look at 1000 elements before we got to the one we want to see.

Luckily this isn't the case though, because of those two properties, it's a simple math formula to reach the correct index in one operation. So for an array of size 1000, to get the 1000th element all we need to do is compute: `startAddress + index * sizeof(int)` and we can immediately jump to that element. This is called _constant time_, or `O(1)`. This is the best guarantee possible - it means no matter how big the size of the data, the time it takes to do the operation remains the same.

So in this case we would say the Array has a lookup complexity of `O(1)`. Note that different operations on a data structure can have different complexity guarantees. So consider the cases of adding or removing something from an array. Assuming you already had the room for it (no need to 'grow' the array):

- adding to the end - `O(1)`. Why? Jump to the last index, add one, put it there.
- adding to the beginning/middle - `O(N)`. Why? Will first need to copy every other element to the index next to it. Middle is just as bad as beginning because we are concerned with 'worst case' behavior.

> An important note: in traditional Arrays, the full size of the Array must be known when defining it. That isn't the case with JS or Python arrays, which you can add to indefinitely. How this actually works under the hood is that, when you try to add an element to an already full array in JS, behind the scenes it will double it's size in memory, copy over all the existing elements, and then add the next one. This is significant because in reality adding an element to an array, even to the end, is not necessarily `O(1)`.

## Linked lists

After Arrays, Linked Lists are the most common, basic data structure. You often won't see these explciitly in a language, but they are definitely used everywhere under the hood. Once again, let's think of this in the abstract first.

A **Linked List** is a _non-contiguous_ data structure, meaning the elements of a linked list are not necessarily next to each other in memory.

Each element in a linked list is called a node and this node holds a `value` (the data value that we are holding) and a pointer `next` which contains a reference to the next element.

![LL](./page-resources/linked-list.png)

A LL is like an array in that it holds ordered data, but it is not contiguous in memory. How is this an advantage? The basic reason for the existence of a LL is that some data is too large to store contiguously. Imagine you wanted to download a 90GB game to your gaming PC, and all that memory needed to be contiguous? Maybe you have a total of 90GB of free space on your hard drive, but all in order? Probably not. A LL is a data structure that takes advantage of free memory being randomly distrbuted throughout your hard drive, which happens as things are created and deleted.

So what does a LL look like in code? In Python you could model such a DS like so:

```py
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

nums_0 = Node(1)
nums_1 = Node(4)
nums_2 = Node(12)
nums_3 = Node(2)
nums_4 = Node(7)

nums_0.next = nums_1
nums_1.next = nums_2
nums_2.next = nums_3
nums_3.next = nums_4
nums_4.next = None

nums = nums_0
```

The above was meant to be explicit, so you could see how the connections are made, but we can define that much more concisely like so:

```py
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

nums = Node(1, Node(4, Node(12, Node(2, Node(7)))))
```

### Analysis

OK, we defined a LL, but what is it good for? Well, let's compare it to an Array. What about lookup? Because the memory is non-contiguous, we can't just do a little math to find the 17-th element, for example, we need to walk through the LL, from the beginning, one element at a time, using `next` to traverse.

```py
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class LL:
    def __init__(self, head):
        self.head = head

    def get_by_index(self, index):
        current = self.head
        current_index = 0

        while(current_index < index):
            assert current.next != None, "Out of bounds!"
            current = current.next
            current_index += 1

        return current.value


nums = Node(1, Node(4, Node(12, Node(2, Node(7)))))
ll = LL(nums)

ll.get_by_index(4) # 7
```

This is not constant time like with an Array, it is linear time, `O(n)`!

However consider adding an element to the end of the LL? Unlike an Array, we could do this forever without ever having to change the size of the array, as the memory can be non-contiguous. And we can hold a pointer to the last element, making this constant time:

```py
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class LL:
    def __init__(self, head):
        self.head = head
        self.last_index = head

    def append(self, value):
        new_node = Node(value)
        self.last_index.next = new_node
        self.last_index = new_node


ll = LL(Node(1))
ll.append(4)
ll.append(12)
ll.append(2)
ll.append(7)
```

This is constant time! This is the basic trade off for an Array vs a LL:

Array:

- get/set: `O(1)`
- add/remove: `O(n)`

LL:

- get/set: `O(n)`
- add/remove: `O(1)`

## Additional Learning

[Stacks and Queues](https://youtu.be/Zai4ejbY6qQ?t=840) (from 14:00 - 21:00 approximately) are two data structures that can be implemented using either an Array or a Linked List. Watch this video about them for the sake of understanding, as this will open up another avenue of LeetCode type problems for you to practice.

## Assignments

- [Arrays - Two Sum](https://leetcode.com/problems/two-sum/)
- [Arrays - Search Insert Position](https://leetcode.com/problems/search-insert-position/) (ignore the desired complexity of `O(log n))`)
- [LinkedList - Remove Elements](https://leetcode.com/problems/remove-linked-list-elements/)
- [LinkedList - Reverse](https://leetcode.com/problems/reverse-linked-list/)

- Bonus: if you have time, explore Leetcode. Stick to 'easy' problems for now (they are hard enough), but it can be a good way to learn about what types of data structures are out there, as there are many more then our program can cover in this week.

> Note: we recognize even the 'easy' problems are not that easy. We want you to get more familiar with Leetcode and what these kinds of challenges involve. The problems often seem contrived but they are a kind of exercise designed to stretch the muscles of your programming brain.
