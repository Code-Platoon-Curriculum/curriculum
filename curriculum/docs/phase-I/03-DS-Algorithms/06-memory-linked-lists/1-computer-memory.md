# Understanding Computer Memory in Python Programming

## Introduction

Today, we're diving into the heart of your code - computer memory. This is a critical aspect that influences the performance and efficiency of your programs. In this lecture, we'll learn about different kinds of computer memory, their differences, and explore why understanding computer memory is crucial in coding, specifically focusing on Python programming.

- [SLIDES](https://docs.google.com/presentation/d/1mBlIOEieBYjzEKMzQ-yxVaZVsAUuWmjwzKmKLew3HL4/edit#slide=id.g27fd771933b_0_9)

## Lecture

**Computer Memory** refers to the hardware components responsible for temporarily or permanently storing data and instructions in a computer. All computers have some form of memory. All data in a computer, from files, to currently running program,s and even the OS itself, is stored in memory. So memory is essential to a computer's functionality and performance.

### Kinds of Computer Memory

There are two kinds of computer memory - *primary memory*, and *secondary memory*, aka *storage*.

- Primary memory is *volatile* - the data stored in it disappears when the computer is turned off. It is smaller, faster, and more expensive.

- Secondary memory is *non-volatile* - the data stored in it *persists* when the computer is turned off. It is larger, slower, and cheaper.


#### Primary Memory

Primary Memory, aka *Working Memory* or *Main Memory* is where the CPU stores and retrieves data actively in use. For example, when you have multiple applications open on your computer, the data from these applications resides in RAM for quick access.

##### Examples of Primary Memory

- RAM (Random Access Memory)
- The CPU Cache

#### Secondary Memory

Unlike Main Memory, Secondary Memory, often referred to as Storage, is non-volatile, meaning it retains data even when the power is turned off. An example of this is your computer's hard drive or solid-state drive (SSD), where data is stored persistently, allowing you to power off and restart your computer without losing stored information.

##### Examples of Secondary Memory

- HDD (Hard Disk Drive)
- SSD (Solid State Drive)

There is also *external storage*, such as:

- Backup tapes
- USB sticks
- External Hard Drives
- Floppy disks, CD-ROMs, etc.

### How Computer Memory is Organized

#### Memory Addresses

Memory in a computer can be thought of as a contiguous block of identically sized 'slots', like so:

![memory](./resources/memory.png)

- Memory is like a single long street, with plots of land of identical size, one after the other. 
- Each spot in memory has an *address* 
- For contiguous blocks of memory the address is **relative to the beginning of the street, and the size of a plot of land.**

![memory addresses](./resources/memory-adresses.png)

- This is a simple example of a 32-bit architecture - the standard size of a 'thing' in this memory structure is 32 bits, or 4 bytes.

- Memory addresses are usually described in hexadecimal, so you will often see a memory address look like '0x1047cc0f0'.

- Even though we don't usually consider memory locations in Python, we can see this concept with the built in `id()` function.

```py
x = 1 # create a variable called x and store a 1 in it
id(x) # the memory location of x, as a decimal (4370252016)
hex(id(x)) # the memory location of x, as hexadecimal (0x1047cc0f0)
```

Let's assume that all primitive values we represent in memory (integers, floats, characters, booleans) can fit within this amount of space.

If 32-bits represents a single slot in memory, and an individual character can be stored in a single slot, a string might look like this in memory:

![hello memory](./resources/hello-memory.png)

### Arrays

An **Array** is a collection of elements of the same data type that are stored at **contiguous memory locations. An example:

```py
nums = [1, 4, 12, 7, 2]
```

- All elements in an array must be the same type.
- Array data structures are always stored in contiguous blocks of memory.

![num array](./resources/num-array.png)

> Javascript 'Arrays' are not true Arrays! They are really more like Python Lists.

`nums` is a variable that _refers_ to the array. We call this a _pointer_. A pointer refers to a specific address in memory, so in this example the pointer `nums` holds the memory address `0`.

#### Getting an element in an Array is O(1)

Let's consider what is actually happening when you index an array.

```py
nums[0] # 1
nums[2] # 12
nums[4] # 2
```

Indexing is simple arithmetic. To get the memory location of an index in an array we simply do:

```sh
memory_address_of_beginning_of_arr + index_desired * size_of_each_thing_in_array
```

To get the value of `nums[4]` we take the beginning memory location of `nums` and add `4 * sizeof(int)`. 

Because we established that an int is 32 bits, that means the memory address of `nums[4]` is: `0 + 4 * 32 = 128`.

The memory being in a contiguous block holding same-sized objects is necessary because it's what allows us to 'jump' to the 4-th index without having to actively look through the previous elements.

> Getting some element at index *i* of an array is a *O(1)* operation - constant time.

### Why It's Important to Understand Computer Memory in Coding

Let's dig into why this matters.

#### Resource Optimization

- Efficient memory usage directly impacts the performance of your code.
- Reducing memory consumption allows for better scalability and lower hardware requirements.

#### Preventing Memory Leaks

Understanding memory helps in identifying and preventing memory leaks, where memory is allocated but not released.

#### Performance Improvement

Writing code that is mindful of memory leads to faster execution and improved overall system performance.

### What Happens in Computer Memory When I Create a List?

#### Where Does the List Live?

When you create a list in Python, it gets stored in the computer's primary memory (RAM). The list holds references to the objects it contains, and each object might have its own memory location.

#### What Happens When I Change the List?

1. **Adding Elements:**
   - If you append an element to the list, Python allocates more memory to accommodate the new element.

   ```python
   lst_of_nums = [1, 2, 3]
   lst_of_nums.append(4)  # Memory is adjusted to include 4
   ```

2. **Modifying Elements:**
   - When you modify an existing element, the change happens directly in the allocated memory.

   ```python
   lst_of_nums[1] = 10  # Modifying the second element in-place
   ```

3. **Removing Elements:**
   - Removing an element or using methods like `pop` can free up the memory associated with that element.

   ```python
   removed_item = lst_of_nums.pop()  # Memory for the last item is released
   ```

#### Constructive vs. Destructive Operations

##### Constructive Operations

Some operations create a new list or tuple, consuming additional memory.

   ```python
   # Constructive method - Creating a new list
   lst_of_nums = [1, 2, 3]
   new_list = lst_of_nums + [4, 5, 6]
   # The addition creates a new list in memory, not modifying lst_of_nums
   ```

Constructive operations result in increased memory usage as additional memory is allocated to the program.

##### Destructive Operation

Some operations modify the existing list, without allocating additional memory.

   ```python
   # Destructive method - Modifying the existing list
   lst_of_nums = [1, 2, 3]
   lst_of_nums.append(4)
   # The append method modifies the original list, no new memory allocation
   ```

Destructive operations are generally more memory-efficient as they operate in-place, directly modifying the existing data structure without additional memory needing to be allocated.

#### Memory Occupancy: List vs. Tuple

1. **Memory Usage:**
   - Lists and tuples are both used to store ordered collections of items, but they differ in their memory occupancy.

   ```python
   import sys

   lst_example = [1, 2, 3, 4, 5]
   tuple_example = (1, 2, 3, 4, 5)

   print("Memory occupied by list:", sys.getsizeof(lst_example))
   print("Memory occupied by tuple:", sys.getsizeof(tuple_example))
   ```

   - In general, tuples have a smaller memory footprint than lists. This is because lists are mutable, and they require additional space to accommodate potential changes.

2. **Immutable Nature of Tuples:**
   - Tuples are immutable, meaning their elements cannot be changed after creation. This immutability allows for a more compact memory representation.

   ```python
   # Tuple is immutable
   tuple_example = (1, 2, 3, 4, 5)
   # This will raise an error
   tuple_example[0] = 10
   ```

### How to Account for Memory When Thinking About Efficient Programming?

#### Memory Considerations

1. **Object Size:**
   - Understand the memory size of different data types and objects.
   - For example, integers take less memory than floating-point numbers.

2. **Memory Allocation:**
   - Consider how memory is allocated when creating variables or data structures.
   - Be mindful of memory-intensive operations, especially in loops.

   ```python
   # Inefficient: Creating a new list in each iteration
   result = []
   for i in range(1000):
       result.append(some_function(i))

   # Efficient: Allocate memory once
   result = [some_function(i) for i in range(1000)]
   ```

3. **Memory Release:**
   - Explicitly release memory when it's no longer needed, especially in resource-intensive applications.

   ```python
   # Inefficient: Keeping a large list in memory unnecessarily
   data = get_large_data()
   # Process data
   # Memory for data is not released

   # Efficient: Release memory after use
   data = get_large_data()
   # Process data
   del data  # Explicitly release memory
   ```

> The reason we don't have to do this for small variables is because Python (and Javascript) does this **memory management** for us. That is part of what the **Python interpreter** (the program that interprets our python source code and turns it into bytecode the computer actually executes and runs) does for us. Languages like Python that provide memory management (also called **garbage collection**) are known as **high-level languages** because our software is **abstracted** away from the computer hardware, as opposed to a **low-level language** like C where we explicitly have to allocate or deallocate (aka release) memory for every single variable. Other popular high-level languages include Javascript, PHP, Ruby, and C#.

4. **Choosing Data Structures:**
   - Select the appropriate data structure based on the application's requirements.
   - Use tuples when immutability is beneficial, and lists when mutability is necessary.

   ```python
   # Immutability of tuples
   tuple_example = (1, 2, 3, 4, 5)
   # This operation is not allowed
   tuple_example[0] = 10
   ```

5. **Constructive vs. Destructive Operations:**
   - Be aware of the distinction between constructive and destructive methods.
   - Opt for destructive methods when you want to modify the existing structure without consuming additional memory.

   ```python
   # Destructive method - Modifying the existing list
   lst_of_nums = [1, 2, 3]
   lst_of_nums.append(4)
   # The append method modifies the original list, no new memory allocation
   ```

6. **Memory Occupancy Awareness:**
   - Understand the memory footprint of different data structures to make informed decisions.

   ```python
   import sys

   lst_example = [1, 2, 3, 4, 5]
   tuple_example = (1, 2, 3, 4, 5)

   print("Memory occupied by list:", sys.getsizeof(lst_example))
   print("Memory occupied by tuple:", sys.getsizeof(tuple_example))
   ```

## Conclusion

Understanding how computer memory works in Python is pivotal for writing efficient and optimized code. As you embark on your coding journey, keep in mind that writing high-performance code isn't just about functionality; it's about using computer resources wisely. Happy coding!

- Working Memory vs Storage
- Arrays are contiguous blocks of memory where each element in the Array is the same Type and of a fixed size
- Higher-level languages like Python do most memory management for us
- Being aware of in-place operations vs operations that require additional memory to be allocated