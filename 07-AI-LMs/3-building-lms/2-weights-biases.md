# Weights and Biases

## Introduction

In this lesson, we will explore the critical components of neural networks: weights and biases. These parameters play a fundamental role in how a neural network learns and makes predictions. Understanding how weights and biases work, along with the mathematics behind them, is essential for building and training effective models. We'll also discuss how these parameters are initialized and how their transformation through the network allows for learning and prediction.

## Lesson

### How do Neurons get Transformed within the Neural Network?

As data flows through a neural network, neurons (the units of data) are transformed by applying weights, biases, and activation functions at each layer. This transformation process is what allows the network to learn and adapt to different tasks. When an input is passed through a layer, it is multiplied by weights and adjusted by biases before being passed through an activation function like Sigmoid. This operation is repeated as the data moves through each layer of the network, gradually adjusting the neuron's value until it reaches the output layer, where the final prediction is made. These transformations are the heart of the learning process in neural networks, enabling the model to capture complex patterns and relationships in the data.

### Linear Layer Parameters

#### Weights

Weights are the parameters within the neural network that determine the strength and direction of the connection between neurons in adjacent layers. Mathematically, weights are multiplied with the input values (features) to scale them according to their importance in predicting the target output. The weight matrix \( W \) associated with each layer is learned during training, and each weight is updated through a process called back-propagation.

For example, consider the following layer in our `ExModel`:

```python
self.ly1 = nn.Linear(3, 2)
```

Here, `nn.Linear(3, 2)` creates a layer with 3 input features and 2 output features. The weight matrix \( W \) for this layer will have a shape of \( (2, 3) \), representing the weights connecting each of the 3 inputs to the 2 outputs.

The mathematical operation at each neuron can be expressed as:

\[
y = xW^T
\]

Where:

- \( x \) is the input vector.
- \( W \) is the weight matrix.
- \( y \) is the output vector after applying weights.

Weights are crucial because they control how much influence each input feature has on the output. During training, the model learns the optimal values for these weights by minimizing the loss function, adjusting the weights iteratively to improve prediction accuracy.

#### Biases

Biases are another set of parameters added to the neural network to shift the activation function, allowing the model to fit the data better. Bias terms are added to the weighted sum of the inputs before passing them through the activation function. This helps the model capture patterns even when the input is zero, ensuring that the network can learn a broader range of functions.

In the same layer from our `ExModel`, the bias vector \( b \) is of size 2 (since the layer has 2 outputs). The output of the layer, considering both weights and biases, can be expressed as:

\[
y = xW^T + b
\]

Where:

- \( x \) is the input vector.
- \( W \) is the weight matrix.
- \( b \) is the bias vector.
- \( y \) is the output vector after applying weights and biases.

Biases provide the model with the ability to adjust the output independently of the input, giving it more flexibility to fit the training data. They are particularly important in allowing the network to model non-linear relationships in the data.

#### Weights and Biases in English

Imagine a neural network as an American football team trying to score a touchdown. In this analogy:

- **Neurons** are the players on the field, each with a specific role in moving the ball forward.
- **Weights** are the players' abilities and strengths, determining how effectively they can execute plays and advance the ball.
- **Biases** are the playbook or strategy that guides the team, ensuring they can adapt to different situations on the field.

##### Weights as Player Abilities

When the quarterback throws the ball (input data) to a receiver (neuron in the next layer), the success of that pass depends on several factors: the quarterback's throwing strength, the receiver's speed, and their ability to catch the ball. These factors represent **weights** in the neural network.

- If the quarterback has a strong arm (a large weight), the ball travels further.
- If the receiver is fast and skilled (a high weight), they’re more likely to catch the ball and advance it.

Each player's performance (neuron's output) is determined by multiplying their abilities (weights) with the input (ball's position and speed). The better the abilities (higher or more accurate weights), the better the chance of making progress toward the touchdown (correct output).

##### Biases as the Playbook

However, abilities alone don’t win games. The team also needs a strategy—a playbook. This is where **biases** come in. Biases adjust the team's approach depending on the situation, like choosing to run or pass based on the defense’s formation.

- If the team needs to gain more yards (shift in neuron activation), the playbook (bias) adjusts the strategy to favor plays that exploit the opponent's weaknesses.
- Even if the defense is strong (challenging data conditions), a good playbook (appropriate biases) helps the team (neural network) still make progress.

In the neural network, the bias adds a fixed value to the weighted input, shifting the neuron's activation threshold. This allows the model to make accurate predictions even when the input alone (player abilities) wouldn’t be enough.

##### Putting It All Together

Just like a football team needs both skilled players (effective weights) and a smart strategy (well-chosen biases) to score touchdowns, a neural network requires well-adjusted weights and biases to make accurate predictions. The weights fine-tune how each input (like a pass) influences the output (yardage gained), while the biases adjust the overall strategy, ensuring the network can handle a wide range of scenarios (different data inputs) and still produce a successful result (correct prediction).

#### Prepping for Training

Proper initialization of weights and biases is crucial for effective training. Poorly initialized parameters can lead to slow convergence, vanishing or exploding gradients, and suboptimal performance. PyTorch provides several methods for initializing these parameters, two of which are `init.xavier_uniform_` and `init.zeros_`.

- **`init.xavier_uniform_`**: This method initializes the weights by drawing samples from a uniform distribution, scaled according to the number of input and output neurons. This scaling helps in maintaining the variance of activations across layers, which is important for stable training.

```python
import torch.nn.init as init

# Initialize weights using Xavier initialization
init.xavier_uniform_(model.ly1.weight)
init.xavier_uniform_(model.ly2.weight)
```

- **`init.zeros_`**: This method initializes biases to zero. While simple, initializing biases to zero is common because it provides a neutral starting point, allowing the model to learn the biases during training.

```python
# Initialize biases to zero
init.zeros_(model.ly1.bias)
init.zeros_(model.ly2.bias)
```

We could make our life's easier by creating a `for` loop that will iterate through the Linear Layer attributes of our Model and update the weights and biases rather than doing it one by one.

```python
for layer in model.modules():
  if isinstance(layer, nn.Linear):
    init.xavier_uniform_(layer.weight)
    init.zeros_(layer.bias) 
```

These initialization methods help the model start training with parameters that are well-suited for gradient-based optimization, leading to faster convergence and better overall performance.

## Conclusion

Weights and biases are fundamental components of neural networks, determining how inputs are transformed as they pass through the network. Understanding their role and the mathematics behind them is crucial for designing and training effective models. By properly initializing these parameters using methods like `init.xavier_uniform_` and `init.zeros_`, we set the stage for successful training, allowing the model to learn complex patterns in the data efficiently. With this knowledge, you're now equipped to build, initialize, and train neural networks with a deeper understanding of how these core elements work.
