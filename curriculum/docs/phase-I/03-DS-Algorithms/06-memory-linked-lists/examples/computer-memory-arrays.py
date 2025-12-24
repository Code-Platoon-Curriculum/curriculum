"""
Computer Memory and Arrays
"""
import sys

# Python Memory Usage for list vs tuple
lst_example = [1, 2, 3, 4, 5]
tuple_example = (1, 2, 3, 4, 5)

print("Memory occupied by list:", sys.getsizeof(lst_example))
print("Memory occupied by tuple:", sys.getsizeof(tuple_example))


# Tuples are immutable
tuple_example = (1, 2, 3, 4, 5)
# This will raise an error
tuple_example[0] = 10