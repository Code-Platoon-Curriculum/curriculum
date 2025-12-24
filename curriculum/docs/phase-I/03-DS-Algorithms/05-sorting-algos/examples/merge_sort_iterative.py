"""
Iterative implementation of merge sort
"""
def merge_sort_iterative(items):
    """Merge sort function implemented iteratively. Takes a 
    list of integers, returns them sorted in increasing order."""
    
    items_len = len(items)
    
    # The 'base case' - no need to sort.
    if items_len <= 1:
        return items
    
    # We are going to build our sub-lists 'bottom up' - breaking each item in the list into its own sublist of length 1,
    # then combine them into sublists of length 2 (and sort them), combine those into sublists of length 4, and so on.
    sublist_len = 1

    while sublist_len < items_len:
        # This is the key:
        #  range(start, stop, step) does ..
        # range(0, 10, 2) is [0, 2, 4, 6, 8]
        # This for loop chunks the entire list into sublists of length 2, 4, 8, and so on 
        # https://cs.stanford.edu/people/nick/py/python-range.html
        for i in range(0, items_len, 2 * sublist_len):

            # left sublist of desired size
            left_sublist = items[i:i + sublist_len]

            # right sublist of desired size
            right_sublist = items[i + sublist_len:i + 2 * sublist_len]

            # compare, sort, and merge the two sublists
            merged_sublists = merge(left_sublist, right_sublist)

            # Copy the merged sublist back into the original list at the correct spot.
            items[i:i + len(merged_sublists)] = merged_sublists
        
        # Once all the smaller sublists of size sublist_len are sorted,
        # double sublist_len so we compare and sort the sublists of the next size up, so to speak.
        sublist_len *= 2
    
    return items

def merge(left, right):
    """Assumes left and right are sorted lists. Look at the first element 
    of each list, and moves the smaller of the two to the end of the result list. 
    When one of the lists is empty, all that remains is 
    to copy the remaining items from the other list."""

    result = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1

    return result

    # Example execution of our algorithm
    data = [2, 8, 5, 3, 9, 4, 1, 7]
    sorted = merge_sort_iterative(data)
    print(sorted)