# Training the Model

## Introduction

In this lecture, we'll delve into the process of training a neural network to make accurate predictions. Training a neural network involves iterating over the data, adjusting the model parameters to minimize the prediction error, and evaluating its performance on unseen data. We'll cover the key concepts of datasets, the training loop, optimizers, backpropagation, and model evaluation.

## Lecture

### Creating DataSets

To begin, we need to structure our data for efficient loading and batching. PyTorch provides the `Dataset` and `DataLoader` classes to facilitate this process. Here's how we can create datasets from our preprocessed data and use data loaders to handle batching:

```python
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

# Create the data Split for Training and Testing
training_features, testing_features, training_labels, testing_labels = train_test_split(scaled_features, target, test_size=0.2, random_state=42)

# Create TensorDatasets
train_dataset = TensorDataset(training_features, training_labels)
test_dataset = TensorDataset(testing_features, testing_labels)

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
```

- **TensorDataset** : Creates a tensor of 2 indexed tensors
  - `index 0`: holds the features for said sample
  - `index 1`: holds the label for said sample
  
  ```python
    [
        [[features], [labels]],
        [[features], [labels]],
        [[features], [labels]],
    ]
  ```

- **DataLoader** : Creates an iterable object that takes in the original TensorDataset and "shuffles" the nested samples every time it's called.

### The Training Loop

#### How does training a model work?

Training a model involves iterating through the data, making predictions, calculating the loss (the difference between predictions and actual values), and updating the model parameters to minimize this loss. This process is repeated for a specified number of epochs.

- **Loss Function**: Measures the error between the predicted values and the actual values. For binary classification, we use `nn.BCELoss()`.
- **Optimizer**: Adjusts the model parameters based on the calculated gradients. The optimizer helps to minimize the loss function. We will use `Adam` in our training loop.
- **Number of Epochs**: Determines how many times the entire dataset is passed through the model. More epochs can lead to better performance but may also cause over-fitting.

Here's the basic structure of a training loop without the loss or optimizer functions:

```python
num_of_epochs = 20
for epoch in range(num_of_epochs):
    for features, labels in train_loader:
        output = model(features.float())
```

#### Optimizers

Optimizers are crucial for training neural networks. They update the model's parameters to minimize the loss function. The optimal minimum refers to the point where the loss is the smallest. Learning rate and momentum are key parameters that affect this process:

- **Learning Rate**: Controls the step size of the parameter updates. A high learning rate can lead to overshooting the minimum, while a low learning rate can result in slow convergence.
- **Momentum**: Helps accelerate gradients vectors in the right directions, thus leading to faster converging.

We'll use the `optim.Adam` optimizer, which combines the advantages of two other extensions of stochastic gradient descent.

```python
optimizer = optim.Adam(model.parameters(), lr=0.01)
```

#### Backward Step (BackPropagation)

The backward step, or backpropagation, is a crucial phase in training neural networks. During backpropagation, the model adjusts its weights based on the error calculated in the forward pass. This is how the model "learns" to make better predictions.

- **Forward Step**: Passes the input data through the model to get the output.
- **Backward Step**: Computes the gradient of the loss with respect to each parameter, allowing the optimizer to update the model's weights.

We use `nn.BCELoss()` as the loss function for our binary classification model:

```python
criterion = nn.BCELoss()
```

#### The Complete Loop

Combining all these components, we get the complete training loop:

```python
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
num_of_epochs = 20

for epoch in range(num_of_epochs):
    model.train()  # Set the model to training mode
    for features, labels in train_loader:
        optimizer.zero_grad()
        output = model(features)
        loss = criterion(output, labels.view(-1, 1).float())
        loss.backward()
        optimizer.step()

    print(f'Epoch {epoch+1}/{num_of_epochs}, Loss: {loss.item()}')
```

### Testing the Model

After training the model, we need to evaluate its performance on the testing data. This involves using the model to make predictions on the test data and comparing these predictions to the actual values.

- **Model Evaluation**: Use `model.eval()` to set the model to evaluation mode, which disables dropout and batch normalization.
- **Accuracy Measurement**: Use `torchmetrics.Accuracy` to calculate the accuracy of the model.

```python
from torchmetrics import Accuracy

accuracy = Accuracy(task='binary')

model.eval()  # Set the model to evaluation mode
with torch.no_grad():
    for features, labels in test_loader:
        output = model(features)
        predicted = output.round()
        accuracy.update(predicted, labels)

print(f'Accuracy: {accuracy.compute().item()}')
```

## Conclusion

In this lecture, we covered the process of training a neural network, including creating datasets, understanding the training loop, optimizers, backpropagation, and testing the model. By following these steps, you can train your neural network to make accurate predictions. As you continue practicing and experimenting, you'll gain a deeper understanding of these concepts and improve your model's performance.
