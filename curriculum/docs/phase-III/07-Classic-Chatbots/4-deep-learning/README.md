# Deep Learning

## What are we trying to accomplish?

In this lesson, students will learn how to build and train **fully connected neural networks** using PyTorch to perform multi-class classification on tabular data. Rather than relying on rules or statistical text representations, students will work with machine learning models that learn predictive patterns directly from data. Students will set up a complete ML pipeline—from data loading and preprocessing through model definition, training, and evaluation—gaining hands-on experience with the core tools and concepts that underpin modern deep learning systems. By the end of this lesson, students will understand how data flows through a neural network during both the forward and backward pass, and will be able to build, train, and evaluate their own classification models in Python.

---

## Lectures & Assignments

### Lectures

* [Lecture - Working with Data](./1-data-preprocessing.md)
* [Lecture - Multi-Classification Models](./2-learning-models.md)

### [Assignments](./assignments.md)

---

## TLO's (Terminal Learning Objectives)

* Build and train a fully connected neural network using PyTorch for multi-class classification
* Preprocess tabular data for a machine learning pipeline using pandas and scikit-learn
* Convert cleaned data into PyTorch tensors and structure it with `TensorDataset` and `DataLoader`
* Define a custom neural network class using `nn.Module` with linear and activation layers
* Implement a complete training loop using `CrossEntropyLoss` and the Adam optimizer
* Evaluate model performance using an evaluation loop and accuracy metrics

---

## ELO's (Enabling Learning Objectives)

* What learning models are and how fully connected neural networks process data layer by layer
* How input layers, linear (hidden) layers, and activation layers work together in a neural network
* Why data preprocessing is a required step before training any machine learning model
* How to handle missing values, scale features, and split data into training and testing sets
* What PyTorch tensors are and how they differ from standard Python data structures
* How `TensorDataset` and `DataLoader` organize and batch data for efficient training
* What Softmax activation does and why it is used in multi-class classification output layers
* How weights and biases are initialized and why they are the learnable parameters of a network
* What loss functions measure and how `CrossEntropyLoss` quantifies prediction error
* How the Adam optimizer uses gradients to update model parameters during training
* The distinction between the forward pass (prediction) and backward pass (backpropagation)
