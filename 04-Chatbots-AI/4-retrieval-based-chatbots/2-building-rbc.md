# Building a Retrieval-Based Chatbot with Word Embeddings

## Introduction

In this lecture, you will **build a fully functional retrieval-based chatbot** using Python, spaCy’s pretrained word embeddings (`en_core_web_md`), and a small dataset of intents stored in a JSON file.  

By the end, your chatbot will:

* Process user input
* Match it to the **closest intent** in the dataset using semantic similarity
* Retrieve and return the appropriate response

We'll also touch on **next-step improvements** using similarity scoring and ranking for more advanced chatbots.

---

## Prepare the Dataset

For this lecture, we will use a small `intents.json` file containing `tag`, `patterns`, and `responses`. Just like we did in our *Rule Based Chatbot*, we must have a key to utilize for returning responses that correspond to dictated intents. 

You'll notice this file is a `json` file, but it can be read within a Python environment and it is not uncommon for data to be stored and/or shared within `json` formats.

```python
import json
# Load intents.json
with open("./resources/intents.json", "r") as f:
    intents = json.load(f)

# Check the data
print(intents["intents"][0])
```

**Should Output:**

```python
{
  "tag": "greeting",
  "patterns": ["hello", "hi there", "hey", "good morning", "good evening"],
  "responses": ["Hello! How can I help you today?"]
}
```

---

## Loading Libraries and spaCy Model

We'll use **spaCy** to create embeddings for our patterns and user input.

### What is **spaCy** and how does it help us?

In the context of word embedding techniques, `spaCy`’s `en_core_web_md` is a pre-trained English language model that provides dense vector representations (word embeddings) for words, phrases, and documents. These embeddings capture semantic meaning by positioning words with similar contexts closer together in a multi-dimensional vector space, enabling operations like measuring similarity between words, phrases, or entire texts. Unlike simple one-hot encodings, which are sparse and do not capture semantic relationships, `en_core_web_md` leverages pre-trained word vectors to encode nuanced linguistic information, allowing applications such as similarity-based retrieval, clustering, and more sophisticated natural language understanding tasks.

### Installing `spaCy`

Ensure your Python Virtual Environment is activated and connected to your development environment before executing the following commands **individually** within your terminal:

```bash
pip install -U pip setuptools wheel

pip install -U spacy

python -m spacy download en_core_web_sm
```

Now within a Python script and/or JupyterNotebook, execute this codeblock to ensure your installment was successful

```python
import spacy

# Load spaCy medium English model
nlp = spacy.load("en_core_web_md")
```

---

## Preprocess Patterns

We'll create a **list of all patterns** and associate them with their intent tag.
We’ll convert each pattern to a **spaCy vector** for semantic comparison.

```python
# Flatten patterns and keep track of their tags
pattern_texts = []
pattern_tags = []

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        pattern_texts.append(pattern)
        pattern_tags.append(intent["tag"])

# Convert all patterns into spaCy vectors
pattern_vectors = [nlp(pattern).vector for pattern in pattern_texts]
```

---

## Create a Retrieval Function

Now we’ll implement a function that:

1. Takes **user input**
2. Converts it to a **vector** using spaCy embeddings
3. Computes **similarity** between the input and all patterns
4. Returns the **response** from the closest pattern’s intent

```python
import numpy as np
import random

def retrieve_response(user_input):
    user_vector = nlp(user_input).vector
    similarities = [np.dot(user_vector, pattern_vec) / (np.linalg.norm(user_vector) * np.linalg.norm(pattern_vec))
                    for pattern_vec in pattern_vectors]
    
    # Find the index of the highest similarity
    best_idx = np.argmax(similarities)
    
    # Get the corresponding intent tag
    best_tag = pattern_tags[best_idx]
    
    # Retrieve a random response for that intent
    for intent in intents["intents"]:
        if intent["tag"] == best_tag:
            return random.choice(intent["responses"])
```

**Notes:**

* Here we use **cosine similarity** conceptually: `dot(A, B) / (||A|| * ||B||)`.
* The function currently **returns the best single response**.
* Later, this can be extended to **rank multiple responses** for richer interaction.

---

## Test the Chatbot

```python
# Example interactions
print(retrieve_response("hello!"))
print(retrieve_response("good night"))
print(retrieve_response("thanks a lot"))
print(retrieve_response("what is your name"))
```

**Expected Output (will vary due to random choice among responses):**

```
Hello! How can I help you today?
Goodbye! Have a wonderful day!
You're very welcome!
I'm your friendly retrieval-based chatbot!
```

---

## Create a Chat Loop 

To make the chatbot interactive:

```python
print("Start chatting with the chatbot (type 'quit' to stop)")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Chatbot: Goodbye!")
        break
    response = retrieve_response(user_input)
    print(f"Chatbot: {response}")
```

---

## Next Steps

While our chatbot now retrieves the **single most similar pattern**, there are ways to **improve it**:

* **Similarity scoring techniques:**

  * Rank the top N similar patterns and pick the most confident response
  * Set thresholds to detect “unknown” queries
* **Embeddings enhancements:**

  * Use **sentence embeddings** (`sentence-transformers`) for better semantic understanding
  * Fine-tune embeddings on domain-specific data
* **Context awareness:**

  * Use conversation history to select responses more intelligently

---

## 🧾 Summary

In this lecture, you:

* Loaded a **realistic JSON intents dataset**
* Converted text patterns and user input to **spaCy vectors**
* Built a **retrieval-based chatbot** that matches user queries to the closest intent
* Implemented a **chat loop** to interact with the chatbot in Jupyter
* Discussed **next-step improvements** for similarity scoring and embeddings

By the end, you now have a **working retrieval-based chatbot** powered by pretrained word embeddings that can be extended to more complex, semantic-aware chatbots.
