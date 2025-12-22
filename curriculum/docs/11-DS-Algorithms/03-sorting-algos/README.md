# Sorting Algorithms

## What are we trying to accomplish?

You will learn about the Bubble Sort, Insertion Sort, and Merge Sort sorting algorithms. You will learn the algorithm itself, discover what kind of data produces best-case, average-case, or worst-case time complexity for each algorithm, and you will learn how to implement each algorithm.

This will help you understand fundamental concepts of sorting, foster algorithmic thinking and problem-solving skills, and give you a foundation to learn more advanced algorithms.

Understanding these sorting algorithms will provide you with a solid foundation in algorithmic thinking and performance analysis, enabling you to choose the most appropriate sorting method based on the characteristics of your data.

## TLO's (Tangible Learning Objectives)

- None of these concepts will be evaluated here in Code Platoon but they will be expected of you upon reaching the interview process or possibly your first job.

## ELO's (Enabling Learning Objectives)

- Bubble sort: Implement it, be able to explain its runtime complexity, and give examples of different inputs resulting in best-case, worst-case, or average-case complexity.

- Insertion Sort: Implement insertion sort, explain its runtime complexity, and give examples of different inputs resulting in best-case, worst-case, or average-case complexity.

- Merge Sort: Implement it iteratively (not recursively) and explain its runtime complexity, and give examples of different inputs resulting in best-case, worst-case, or average-case complexity.

## Lessons & Assignments

- [Lesson - Bubble Sort, Insertion Sort, And Complexity Analysis](./1-bubble-insertion-sort.md)
    - Assignment: Selection Sort
        - Read about Selection Sort in [Grokking Algorithms (Chapter 2)](https://drive.google.com/drive/folders/1JXp_dvxjdFWyrVmSq6wqs9vcvqSDtZ5O). 
        - Watch [this video on Selection Sort](https://www.youtube.com/watch?v=g-PGLbMth_g&t=63s). Now:  
        1. Create your own diagram of how Selection Sort works for a list of length 4, like we have been in class. **Put this diagram in the `README.md` file of the github repo you will create for this assignment.**
        2. Write your own implementation of Selection Sort in Python.
        3. Write pytest tests for it:
            - Test for a list of length 0 of randomly ordered integers (such as `[]`)
            - Tests for a list of length 1 of randomly ordered integers (such as `[3]`)
                - Write tests specifically for `0`, a positive integer, and a negative integer.
            - Tests for a list of length 4 of randomly ordered integers (such as `[-4, 0, 1, -9]`).
                - Make sure your data includes `0` and a negative integer.
            - Each test should do two things:
                - Test the list has been correctly sorted
                - **Your program must have a print statement for each "step" of the sorting algorithm.** The test should look at this output to check that your algorithm is behaving correctly. 

- [Lesson - Merge Sort](./2-merge-sort.md)
  - [Assignment: Implement Merge Sort for I024 Slices](https://github.com/Code-Platoon-Assignments/algos-merge-sort-1024-calories/tree/main)
