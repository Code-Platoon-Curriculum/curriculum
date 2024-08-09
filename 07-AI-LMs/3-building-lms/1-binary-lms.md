# Building a Learning Model with PyTorch

## Introduction

In this lecture, we will delve into the process of building a learning model with PyTorch, focusing on the essential components and techniques needed to construct neural networks. We will explore the theory behind learning models, understand the role of different layers in a neural network, and learn how to implement these layers using PyTorch's `nn.Linear` and `nn.Sigmoid` classes. We will also compare the use of `nn.Sequential` and `nn.Module` for creating models, providing practical code examples to illustrate the benefits and limitations of each approach. By the end of this lesson, you'll be equipped to build and understand a binary classification model using PyTorch.

## Lesson

### What are Learning Models?

Learning models, often referred to as machine learning models, are algorithms designed to recognize patterns and make predictions based on input data. These models learn from historical data to identify relationships between features and outcomes, allowing them to generalize and make predictions on new, unseen data. In neural networks, learning models consist of multiple layers of interconnected nodes (neurons) that process and transform input data through various operations, ultimately producing an output. By training these models with data, we adjust their parameters (weights and biases) to improve their performance and accuracy in tasks such as classification, regression, or clustering.

![binary_n](./resources/binary_n.png)

### Model Layers

Neural networks are composed of various layers that perform different functions to process and transform data. The primary types of layers include:

- **Input Layer**: The first layer that receives the raw data.
- **Hidden Layers**: Intermediate layers where data is transformed through linear and non-linear operations.
- **Output Layer**: The final layer that produces the model's prediction or classification.

Each layer performs specific operations, such as applying weights and biases or applying activation functions to introduce non-linearity. Understanding these layers and their functions is crucial for designing and implementing effective neural networks.

#### Hidden Layers (`nn.Linear()`)

Hidden layers in a neural network are responsible for transforming input data through linear combinations of features. The `nn.Linear` layer in PyTorch performs a linear transformation of the input data, defined by the equation \(y = xW^T + b\), where \(x\) is the input, \(W\) is the weight matrix, and \(b\) is the bias.

```python
import torch
import torch.nn as nn

# Example of nn.Linear
linear_layer = nn.Linear(in_features=3, out_features=2)
print(linear_layer)

# Attributes of nn.Linear
weights = linear_layer.weight
biases = linear_layer.bias

print("Weights:", weights)
print("Biases:", biases)
```

In this code snippet:

- We define a `nn.Linear` layer with 3 input features and 2 output features.
- The layer's weights and biases are initialized with random values and can be accessed directly if need be.
- The `nn.Linear` layer performs a linear transformation of the input data, learning these parameters during training.

#### Activation Layer (`nn.Sigmoid`)

Activation layers introduce non-linearity into the neural network, allowing it to learn complex patterns. The `nn.Sigmoid` function is a type of activation function mainly utilized as the output layer for binary models since it maps input values to an output range between 0 and 1, following the logistic function.

![logic_func](./resources/sigmoid.png)

```python
# Example of nn.Sigmoid
sigmoid = nn.Sigmoid()
input_tensor = torch.tensor([0.0, 1.0, 2.0])
output_tensor = sigmoid(input_tensor)
print("Output after Sigmoid activation:", output_tensor)
```

In this example:

- We define a `nn.Sigmoid` activation function.
- The sigmoid function is applied to an input tensor, transforming its values to be between 0 and 1.

### Creating a Model

The forward pass of a neural network refers to the process of passing input data through the network's layers to produce an output. During the forward pass, data flows through each layer sequentially, with each layer applying its specific operations to transform the data. The output of each layer becomes the input to the next layer, ultimately producing the final prediction or classification.

Lets apply this concept and pass forward tensor through the different layers of a Neural Network:

```python
from torch import nn
input_tensor = torch.tensor([0.0, 1.0, 2.0])
layer_one = nn.Linear(3,2)
layer_two = nn.Linear(2,1)
sigmoid = nn.Sigmoid()

forward = layer_one(input_tensor)
forward = layer_two(input_tensor)
prediction = sigmoid(forward)
```

We successfully applied the forward pass manually, but this doesn't seem to be the most effective method for applying the forward pass. This code is not very reusable nor dynamic.

#### Creating a Model with `nn.Sequential`

`nn.Sequential` is a convenient way to define a neural network by stacking layers in a sequential order. It simplifies model creation by allowing you to specify the layers and their order in a single, easy-to-read block of code.

```python
import torch.nn as nn

# Example of model creation using nn.Sequential
model_sequential = nn.Sequential(
    nn.Linear(3, 2),
    nn.Linear(2, 1),
    nn.Sigmoid()
)
prediction = model_sequential(input_tensor)
```

In this code:

- We create a model using `nn.Sequential`, specifying the order of layers from input to output.
- While `nn.Sequential` is easy to use, it has limitations, such as difficulty handling more complex architectures with branching or skip connections.

#### Creating a Model with `nn.Module`

`nn.Module` provides greater flexibility for defining neural networks, allowing you to create custom models with more control over the network's architecture and forward pass. By inheriting `nn.Module`, you can define complex models with multiple components and operations.

```python
class ExModel(nn.Module):
    def __init__(self):
        super(ExModel, self).__init__()
        self.ly1 = nn.Linear(3, 2)
        self.ly2 = nn.Linear(2, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.ly1(x)
        x = self.ly2(x)
        x = self.sigmoid(x)
        return x

# Example of creating and using the custom model
model = ExModel()
prediction = model(input_tensor)
print(prediction)
```

In this example:

- We define a custom model class `ExModel` using `nn.Module`.
- The `__init__` method initializes the layers, and the `forward` method defines how data flows through the layers.
- `nn.Module` is preferred for its flexibility, allowing for complex network architectures and operations beyond simple sequential layers.

## Conclusion

Building a learning model with PyTorch involves understanding and implementing various layers and components, such as hidden layers, activation functions, and model definitions. By learning how to use `nn.Linear` and `nn.Sigmoid`, as well as creating models with `nn.Sequential` and `nn.Module`, you'll gain the skills needed to design and train neural networks effectively. Whether using the simplicity of `nn.Sequential` or the flexibility of `nn.Module`, these techniques will enable you to create and customize models for various machine learning tasks.
