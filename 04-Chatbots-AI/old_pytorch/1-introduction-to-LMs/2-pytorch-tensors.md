# Intro to Torch Tensors

## Introduction

In neural networks, nodes (neurons) process inputs to produce outputs, and these inputs and outputs are often represented as tensors. Tensors are multi-dimensional arrays that enable efficient computation and are fundamental in deep learning frameworks like PyTorch. Understanding tensors is crucial for building, training, and optimizing neural networks, as they represent everything from input data to model parameters.

## Lesson Content

### What is a Tensor

A tensor is a generalization of vectors and matrices to potentially higher dimensions. Tensors are essential in the context of neural networks because they enable efficient computation of mathematical operations required for training models. Let's start by looking at a multi-dimensional list in Python:

```python
import random

# Create a 3x3 matrix (list of lists) with random float values
matrix = [[random.random() for _ in range(3)] for _ in range(3)]
print(matrix)
```

This code snippet generates a 3x3 matrix filled with random float values using Python's `random` module. However, working with multi-dimensional lists in Python for mathematical operations like addition, subtraction, and multiplication can be cumbersome and inefficient, think about just creating a list like this or having to manually built these lists of lists from a data.csv file utilizing strictly Python code. The error margin is pretty high.

#### Problems with Pure Python for Multi-dimensional Arrays

Performing element-wise addition or multiplication on lists requires nested loops and additional code to handle various edge cases, making it error-prone and less readable.

Example of element-wise addition using pure Python:

```python
matrix1 = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
matrix2 = [[9.0, 8.0, 7.0], [6.0, 5.0, 4.0], [3.0, 2.0, 1.0]]

result = [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
print(result)
```

This example demonstrates element-wise addition of two 3x3 matrices, which requires nested loops to iterate over each element.

Keep in mind, in this example alone we are conducting a lot of assumptions:

1. all types are the same within the lists and the required level of precision is assumed to be the same.
2. We are assuming both matrices are the same length which won't always be the case.

#### What is a Tensor?

A tensor is a multi-dimensional array that provides a more efficient way to handle such operations. Tensors in PyTorch are similar to NumPy arrays but with additional capabilities for GPU acceleration and automatic differentiation.

Example of creating a tensor in PyTorch:

```python
import torch

tensor1 = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
tensor2 = torch.tensor([[9.0, 8.0, 7.0], [6.0, 5.0, 4.0], [3.0, 2.0, 1.0]])

# Element-wise addition
result = tensor1 + tensor2
print(result)
```

Using PyTorch tensors, the same element-wise addition is much simpler and more readable. The addition operation is performed directly on the tensors without the need for nested loops. Not to mention many of the implied scenarios we talked about earlier are either handled or identified as an issue by Pytorch right from the start of the operation.

##### Importance of Tensors in Neural Networks

In neural networks, tensors represent inputs, outputs, weights, and biases. For instance, an input layer of a neural network can be represented as a tensor where each element corresponds to a feature in the input data. Tensors enable efficient computation of forward and backward passes during training, making them a fundamental building block in deep learning.

#### Tensor Manipulation

Tensor manipulation is crucial for preparing data, training models, and making predictions. PyTorch provides various functions to manipulate tensors efficiently.

##### Essential Tensor Manipulation Tools

1. **Reshaping Tensors**: Changing the shape of a tensor without changing its data.

    ```python
    tensor = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    reshaped_tensor = tensor.view(1, 9)
    print(reshaped_tensor)
    ```

2. **Slicing and Indexing**: Accessing specific elements, rows, or columns in a tensor.

    ```python
    tensor = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    # Basic slicing
    sliced_tensor = tensor[:, 1]  # Select all rows in the second column
    print(sliced_tensor)
    
    # Boolean indexing
    boolean_tensor = tensor[tensor > 5]  # Select elements greater than 5
    print(boolean_tensor)
    ```

3. **Concatenation**: Combining multiple tensors along a specific dimension.

    ```python
    tensor1 = torch.tensor([[1, 2], [3, 4]])
    tensor2 = torch.tensor([[5, 6], [7, 8]])
    concatenated_tensor = torch.cat((tensor1, tensor2), dim=0)  # Concatenate along rows
    print(concatenated_tensor)
    ```

4. **Stacking**: Stacking tensors along a new dimension.

    ```python
    stacked_tensor = torch.stack((tensor1, tensor2), dim=1)  # Stack along columns
    print(stacked_tensor)
    ```

### Tensor Methods

PyTorch provides a wide range of tensor methods that are essential for building and optimizing neural networks. These methods include mathematical operations, aggregation, and transformation functions.

#### Built-in Tensor Methods

1. **Shape and Size**:

    ```python
    tensor = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    print(tensor.shape)  # Shape of the tensor
    print(tensor.size())  # Size of the tensor
    ```

2. **Number of Dimensions**:

    ```python
    print(tensor.ndim)  # Number of dimensions
    ```

3. **Data Type**:

    ```python
    print(tensor.dtype)  # Data type of the tensor
    ```

4. **Unsqueeze**:

    ```python
    unsqueezed_tensor = tensor.unsqueeze(0)  # Add an extra dimension at position 0
    print(unsqueezed_tensor)
    ```

5. **Ravel**:

    ```python
    raveled_tensor = tensor.ravel()  # Flatten the tensor
    print(raveled_tensor)
    ```

6. **Reshape**:

    ```python
    reshaped_tensor = tensor.reshape(1, 4)  # Reshape tensor to 1x4
    print(reshaped_tensor)
    ```

7. **Split**:

    ```python
    split_tensors = tensor.split(1, dim=0)  # Split tensor into chunks along dimension 0
    for t in split_tensors:
        print(t)
    ```

8. **Mathematical Operations**:

    ```python
    sum_tensor = tensor.sum()  # Sum of all elements
    mean_tensor = tensor.mean()  # Mean of all elements
    print(sum_tensor, mean_tensor)
    ```

9. **Aggregation Functions**:

    ```python
    max_val, max_idx = tensor.max(dim=0)  # Max values and their indices along a dimension
    print(max_val, max_idx)
    ```

10. **Transformation Functions**:

    ```python
    transposed_tensor = tensor.t()  # Transpose of the tensor
    print(transposed_tensor)
    ```

#### Scenarios for Tensor Methods

- **Normalization**: Often, input data needs to be normalized before feeding it into a neural network. This can be done using tensor operations.

    ```python
    tensor = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    normalized_tensor = (tensor - tensor.mean()) / tensor.std()
    print(normalized_tensor)
    ```

- **Broadcasting**: This feature allows you to perform operations on tensors of different shapes by automatically expanding their dimensions.

    ```python
    tensor1 = torch.tensor([1.0, 2.0, 3.0])
    tensor2 = torch.tensor([[1.0], [2.0], [3.0]])
    result = tensor1 + tensor2  # Broadcasting to match dimensions
    print(result)
    ```

## Conclusion

In this lecture, we introduced the concept of tensors and demonstrated their importance in neural networks. We covered basic tensor operations, manipulation techniques, and essential tensor methods in PyTorch. Understanding these concepts is crucial for efficiently building and optimizing learning models. Keep experimenting with tensors, as they are the building blocks of neural networks and many other machine learning algorithms. Happy coding!
