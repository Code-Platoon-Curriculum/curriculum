# Data Processing

## Introduction

In this lesson, we'll dive into the process of data processing for language modeling. We'll cover essential steps such as loading text data, tokenization, creating sequences, and building a vocabulary. These steps are crucial for preparing our text data for training a language model effectively.

## Lesson Content

### Loading Text Data

- Before we can start processing text data, we need to load it into our Python environment.
- Text data can be sourced from various places such as files, databases, or web scraping.
- Let's load a sample text file into memory:

```python
# Load text data from a file
def load_text(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

# Example usage
text_data = load_text('sample_text.txt')
print("Loaded text data:", text_data[:100])  # Print the first 100 characters
```

### Tokenization and Creating Sequences

- Tokenization involves splitting text into smaller units called tokens, usually words or subwords.
- After tokenization, we create sequences of tokens to feed into the language model.
- Let's tokenize our text data and create sequences:

```python
import nltk
from nltk.tokenize import word_tokenize

# Tokenization
tokens = word_tokenize(text_data)

# Creating sequences
sequence_length = 10
sequences = []
for i in range(0, len(tokens) - sequence_length + 1):
    sequence = tokens[i:i+sequence_length]
    sequences.append(sequence)

print("Example sequence:", sequences[0])
```

### Building Vocabulary

- The vocabulary consists of all unique tokens present in the text data.
- It represents the set of words or subwords that the language model will learn during training.
- Let's build the vocabulary from our tokenized data:

```python
# Build vocabulary
vocabulary = set(tokens)
print("Vocabulary size:", len(vocabulary))
```

## Conclusion

In this lesson, we've explored the data processing steps necessary for preparing text data for language modeling. We've covered loading text data from a file, tokenization, creating sequences, and building a vocabulary. These steps are essential for effectively training a language model on text data. In the next lesson, we'll move on to building and training our language model using PyTorch.
