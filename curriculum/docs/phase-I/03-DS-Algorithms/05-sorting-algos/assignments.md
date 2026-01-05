# Assignments

Assignments should be completed from top to bottom as they will raise in difficulty the lower in the stack.

- <strong>Assignment - Selection Sort</strong>
    - Read about Selection Sort in <a href="https://drive.google.com/drive/folders/1JXp_dvxjdFWyrVmSq6wqs9vcvqSDtZ5O" target="_blank" rel="noopener noreferrer">Grokking Algorithms (Chapter 2)</a>
    - Watch <a href="https://www.youtube.com/watch?v=g-PGLbMth_g&t=63s" target="_blank" rel="noopener noreferrer">this video on Selection Sort</a>
    - Now:
        1. Create your own diagram of how Selection Sort works for a list of length 4, like we have been in class. **Put this diagram in the `README.md` file of the GitHub repo you will create for this assignment.**
        2. Write your own implementation of Selection Sort in Python.
        3. Write pytest tests for it:
            - Test for a list of length 0 of randomly ordered integers (such as `[]`)
            - Tests for a list of length 1 of randomly ordered integers (such as `[3]`)
                - Write tests specifically for `0`, a positive integer, and a negative integer
            - Tests for a list of length 4 of randomly ordered integers (such as `[-4, 0, 1, -9]`)
                - Make sure your data includes `0` and a negative integer
            - Each test should do two things:
                - Test that the list has been correctly sorted
                - **Your program must have a print statement for each "step" of the sorting algorithm.** The test should look at this output to check that your algorithm is behaving correctly
