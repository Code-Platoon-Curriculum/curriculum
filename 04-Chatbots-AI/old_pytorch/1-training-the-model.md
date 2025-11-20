# Training the Model

## Introduction

In this lecture, we'll delve into the process of training a neural network to make accurate predictions. Training a neural network involves iterating over the data, adjusting the model parameters to minimize the prediction error, and evaluating its performance on unseen data. We'll cover the key concepts of datasets, the training loop, optimizers, backpropagation, and model evaluation.

## Lecture

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
