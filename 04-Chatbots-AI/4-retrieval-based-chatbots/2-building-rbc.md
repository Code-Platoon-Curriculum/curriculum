# Building a Deep Learning Retrieval-Based Chatbot with BERT and FAISS

## Introduction

In this lecture, you will build a deep-learning retrieval-based chatbot using:

Sentence-BERT (SBERT) – to generate contextual sentence embeddings

FAISS (Facebook AI Similarity Search) – to perform fast similarity search among stored responses

A small intents dataset stored in JSON format

By the end, your chatbot will:

✅ Understand the meaning of a user’s message (not just keywords)
✅ Retrieve the most semantically relevant response
✅ Perform similarity search efficiently using FAISS

We’ll also discuss how this approach forms the foundation of modern retrieval-augmented chatbots (RAG systems).

## Prepare the Dataset

Just as before, we’ll use a small intents.json file containing:


- `tag` → the intent category

- `patterns` → example user inputs

- `responses` → possible chatbot replies

```python
import json

# Load intents.json
with open("./resources/intents.json", "r") as f:
    intents = json.load(f)

# Quick check
print(intents["intents"][0])
```

**Expected Output:**

```json
{
  "tag": "greeting",
  "patterns": ["hello", "hi there", "hey", "good morning", "good evening"],
  "responses": ["Hello! How can I help you today?"]
}
```

## Installing Dependencies

We’ll need three major packages:

- sentence-transformers → for deep contextual embeddings
- faiss-cpu → for efficient similarity search
- numpy → for vector operations

Run these commands in your terminal or Jupyter environment:

```bash
pip install -U sentence-transformers faiss-cpu numpy
```

## Load the BERT-Based Model

**BERT (Bidirectional Encoder Representations from Transformers)** is a deep learning model developed by Google that understands the meaning of words in context by processing text bidirectionally—that is, considering both the left and right surroundings of each word. Unlike earlier models that read text in one direction, BERT captures nuanced semantic relationships, enabling it to generate rich, contextualized embeddings that reflect sentence meaning rather than just word similarity. In **retrieval-based chatbots**, using BERT (or its optimized variants like Sentence-BERT) is considered best practice because it allows the system to retrieve responses based on semantic relevance rather than exact keyword overlap—meaning the chatbot can recognize that “How’s it going?” and “How are you?” express the same intent, leading to more natural, intelligent, and user-aligned responses.

We’ll use a lightweight Sentence-BERT variant called MiniLM (small but powerful).

```python
from sentence_transformers import SentenceTransformer

# Load pretrained Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')
```

> This model maps sentences to 768-dimensional embeddings that capture semantic meaning, not just word overlap.


## Flatten and Encode All Patterns

We’ll create a list of all patterns (possible user phrases) and encode them into embeddings.

```python
pattern_texts = []
pattern_tags = []

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        pattern_texts.append(pattern)
        pattern_tags.append(intent["tag"])

# Convert patterns to embeddings
pattern_embeddings = model.encode(pattern_texts, convert_to_numpy=True, normalize_embeddings=True)
```

> normalize_embeddings=True ensures cosine similarity ≈ dot product.

Each `pattern_text` now has a semantic vector (deep contextual meaning).

## Building a FAISS Similarity Index

Now we’ll store all embeddings in a FAISS index, which enables instant nearest-neighbor search.

```python
import faiss
import numpy as np

# Determine embedding dimension
embedding_dim = pattern_embeddings.shape[1]

# Create FAISS index (L2 distance, cosine works similarly since we normalized)
index = faiss.IndexFlatIP(embedding_dim)  # IP = Inner Product
index.add(pattern_embeddings)

print(f"Indexed {index.ntotal} patterns for retrieval.")
```

FAISS allows us to search for the most similar embeddings in O(log N) time — far faster than manually looping through vectors.

## Implementing the Retrieval Function

By accomplishing the following, we will be able to take in user input and return an appropriate response for the correct intent:

1. Encode the user input into an embedding
2. Query FAISS for the most similar patterns
3. Retrieve the corresponding intent and response

```python
import random

def retrieve_response(user_input, top_k=3):
    # Step 1: Encode input into embedding
    user_emb = model.encode([user_input], convert_to_numpy=True, normalize_embeddings=True)
    
    # Step 2: Search for top-k most similar patterns
    distances, indices = index.search(user_emb, top_k)
    
    # Step 3: Retrieve the best matching intent
    best_idx = indices[0][0]
    best_tag = pattern_tags[best_idx]
    
    # Step 4: Retrieve a random response from that intent
    for intent in intents["intents"]:
        if intent["tag"] == best_tag:
            return random.choice(intent["responses"])
```

Notes:

- FAISS returns the indices of the most similar embeddings.
- You can adjust top_k to analyze multiple potential matches.

Let’s try a few examples.

```python
print(retrieve_response("hey there"))
print(retrieve_response("good night"))
print(retrieve_response("thanks!"))
print(retrieve_response("who are you"))
```


Example Output:

```bash
Hello! How can I help you today?
Goodbye! Have a wonderful day!
You're very welcome!
I'm your friendly retrieval-based chatbot!
```

Even if the user says “hey there!” instead of “hi”, SBERT understands the meaning — semantic similarity, not word matching.

## Creating an Interactive Chat Loop

```python
print("Chatbot is ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Chatbot: Goodbye!")
        break
    response = retrieve_response(user_input)
    print(f"Chatbot: {response}")
```

✅ Try paraphrasing phrases — you’ll see that Sentence-BERT still retrieves correct intents even with different wording.

### Conceptual Diagram

```bash
User Input
   ↓
Sentence-BERT
   ↓
[User Embedding]
   ↓
FAISS Index ───→ [Pattern Embeddings]
   ↓
Retrieve Most Similar Pattern
   ↓
Get Corresponding Intent
   ↓
Return Response
```

## Next-Step Improvements

To evolve this into a production-grade chatbot, you can:

- **Add Confidence Thresholds**

If the similarity score is below a threshold, respond with a fallback:

```python
if distances[0][0] < 0.5:
    return "I'm not sure I understand. Could you rephrase that?"
```

- **Re-Rank with a Cross-Encoder**

Use a cross-encoder model to re-score top results for more precision.

- **Store in a Vector Database**

Move FAISS into a persistent vector DB like:

- Pinecone
- Weaviate
- Qdrant

- **Retrieval-Augmented Generation (RAG)**

Combine this retriever with an LLM generator (like GPT or LLaMA):

- Retrieve top 3 results with FAISS
- Feed them as context to an LLM to generate a contextualized response

## Summary

In this lecture, you:

✅ Built a retrieval-based chatbot powered by deep contextual embeddings
✅ Used Sentence-BERT to transform text into semantic vectors
✅ Integrated FAISS for fast similarity search
✅ Implemented a clean retrieval + response pipeline
✅ Learned how to upgrade spaCy-based bots into deep-learning systems
