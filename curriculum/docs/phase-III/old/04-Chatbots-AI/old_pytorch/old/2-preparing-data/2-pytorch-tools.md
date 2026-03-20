# PyTorch Tools

## Intro

Welcome to the lecture on PyTorch Tools! In this session, we will explore some essential tools and components provided by PyTorch for building and training neural networks. We'll cover the basics of tensors, hidden layers, activation functions, weights, and biases, providing code examples and explanations along the way.

## Lesson

### Everything is a Tensor

In PyTorch, tensors are the fundamental data structure used to represent data and perform operations in neural networks. Tensors can be scalars, vectors, matrices, or higher-dimensional arrays. Let's create a simple tensor:

```python
import torch

# Create a 1D tensor
my_tensor = torch.tensor([1, 2, 3, 4, 5])
print(x)
```

### Hidden Layers

Hidden layers in neural networks perform intermediate computations between input and output layers. The `nn.Linear` module in PyTorch represents a fully connected layer, which performs a linear transformation of the input data. It's first argument should be the same as the number of neurons within the tensor being passed in, and the output is a desired tensor with neuron output.

```python
import torch.nn as N
print(my_tensor.shape) # this will tell me my number of neurons
# Create a fully connected layer
hidden_layer = N.Linear(5,3)
print(hidden_layer)
```

This will create a Linear Layer but if we try to pass in our current tensor into it we will see it raises an error:

> RuntimeError: mat1 and mat2 must have the same dtype, but got Long and Float

This happens because the `dtype` of our tensor shows int64 and Linear Layers only accept tensors of `dtype` float32 within it. So how do we fix this... we simply need to change our tensor into a float and PyTorch has an extremely easy way to implement this:

```python
linear_layer = N.Linear(5,3)
output = linear_layer(my_tensor.float())
print(output)
```

### Activation Layers

Activation functions introduce non-linearity into the neural network, allowing it to learn complex patterns in the data. PyTorch provides various activation functions such as `nn.Sigmoid()` and `nn.Softmax()`.

#### nn.Sigmoid()

The sigmoid function squashes the input values between 0 and 1, making it suitable for binary classification tasks (True if closer to one and False if closer to 0). This means the layer right before the sigmoid function must return a tensor of 1 neuron.

```python
my_tensor = tensor([1, 2, 3, 4, 5])
linear_layer = N.Linear(5,1) # < ONLY 1 NEURON in the output
linear_output = linear_layer(my_tensor.float())
# Create a sigmoid activation function
sigmoid = N.Sigmoid()
output = sigmoid(linear_output)
print(output)
```

#### nn.Softmax()

The softmax function normalizes the input values into a probability distribution over multiple classes, often used in multi-class classification tasks. This means the last layer must return the same number of classes as neurons. If I'm trying to determine if an animal is a mammal, reptile, or something else that gives me 3 separate classes. Meaning my last linear layer should return a 3 neuron tensor.

```python
my_tensor = tensor([1, 2, 3, 4, 5])
linear_layer = N.Linear(5,3) #< there are 3 possible classes
linear_output = linear_layer(my_tensor.float())
# Create a softmax activation function
softmax = N.Softmax(dim=-1)
output = softmax(linear_output)
print(output)
```

### Weights and Biases

Weights and biases are parameters learned by the neural network during training, enabling it to make predictions on new data. These weights and biases live within the hidden layers of a neural network which we currently know as the `N.Linear()` function and are usually initialized with random weights and biases unless specified.

#### Weights

Weights are the parameters that determine the strength of connections between neurons in different layers of the network. When a model is being trained these weights are manipulated through mathematical operations to make each Layer more accurate. We can see these weights within layers like this:

```python
my_tensor = tensor([1, 2, 3, 4, 5])
linear_layer = N.Linear(5,3)
linear_output = linear_layer(my_tensor.float())
softmax = N.Softmax(dim=-1)
softmax(linear_output)
print(linear_layer.weight)
# Accessing weights of a linear layer
weights = linear_layer.weight
print(weights)
```

#### Biases

Biases are the parameters that shift the output of a linear transformation and are updated and maintained in the same way that weights are implemented.

```python
my_tensor = tensor([1, 2, 3, 4, 5])
linear_layer = N.Linear(5,3)
linear_output = linear_layer(my_tensor.float())
softmax = N.Softmax(dim=-1)
softmax(linear_output)
# Accessing biases of a linear layer
biases = linear_layer.bias
print(biases)
```

### Loss Functions

Loss functions are utilized to calculate how off our current weights and biases are and what `gradients` can be applied to each layers weights and biases to make each independent layer more accurate.

Loss functions typically take in 2 arguments, one representing the prediction and two representing the hard truth. We will utilize `CrossEntropyLoss` for classification(t/f || multi-class) predictions and `MSELoss` for regression(numeric) predictions.

### Optimization

Finally our optimizer will take the gradients calculated by the loss function and apply them to each layer of the neural network from last layer to first layer. For the majority of our models we will utilize Stochastic Gradient Descent `SDG` as our optimizer to apply these gradients to each layers weights and biases at each step.

## Conclusion

In this lecture, we've covered essential PyTorch tools for building and training neural networks. We learned about tensors, hidden layers, activation functions, weights, and biases, along with code examples to illustrate each concept. Understanding these tools lays the foundation for developing sophisticated deep learning models using PyTorch. Keep exploring and experimenting with PyTorch to unlock its full potential in your machine learning projects!
