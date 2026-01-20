# Classic ChatBots

![cc](./resources/classic-chatbots.png)

## What are we trying to accomplish?

## Lessons

1. [Intro to Chat-Bots](./1-intro-to-chatbots-prompt-engineering/README.md)
2. [Regex & Rule Based Chat-Bots](./2-regex-rule-based-chatbots/README.md)
3. [Understanding Language](./3-text-preprocessing-language-parsing/README.md)
4. [Deep Learning](./4-deep-learning/README.md)
5. [Retrieval Based Chatbots](./5-retrieval-based-chatbots/README.md)

## Module Topics



## The Missing Conceptual Bridge (What Students Don’t Know Yet)

Before retrieval-based chatbots, students need to understand:

| Concept               | Why it Matters                           |
| --------------------- | ---------------------------------------- |
| Text preprocessing    | Raw text ≠ model input                   |
| Tokenization          | Language must become units               |
| Vocabulary & indices  | Models don’t read words                  |
| Embeddings            | Meaning becomes numbers                  |
| Vector similarity     | Retrieval is math, not magic             |
| Training vs inference | Why some models “learn” and others don’t |

You’re absolutely right: **this must come first**.

---

## What I Recommend (High-Level Path)

Here’s the **ideal progression** for junior developers with no ML background:

---

---

### **Phase 2 — Text Preprocessing & Language Parsing (Next Step)**

**Goal:**
Teach students *how language becomes structured data*.

#### Topics to Cover

* Lowercasing, stripping, normalization
* Tokenization (words → tokens)
* Stop words
* Stemming vs lemmatization (conceptual)
* Bag-of-words representation
* N-grams
* Why order matters in language

🔑 Key takeaway:

> “Before models can reason about language, we must clean and structure it.”

⚠️ **Do NOT** introduce transformers yet.

---

### **Phase 3 — Minimal Deep Learning with PyTorch (Conceptual, Not Heavy Math)**

This is where many curricula fail — you won’t.

#### What to Teach (and What Not To)

**Teach**

* Tensors as numerical containers
* Vectors & matrices
* Embeddings (word → vector)
* Simple neural networks
* Forward pass vs training
* Loss function (conceptually)
* Inference vs training

**Do NOT**

* Backprop math derivations
* Custom optimizers
* CNNs, RNNs, or transformers (yet)

🔑 Key takeaway:

> “Models don’t understand language — they learn numerical patterns.”

This makes retrieval-based systems *click* later.

---

### **Phase 4 — Semantic Meaning & Similarity (The Retrieval Bridge)**

This is the critical transition.

Students should learn:

* What an embedding represents
* Why similar text → similar vectors
* Cosine similarity (visually, not mathematically heavy)
* Why retrieval works even without exact wording

🧠 Aha moment:

> “Oh — the chatbot isn’t searching text, it’s comparing meaning.”

---

### **Phase 5 — Retrieval-Based Chatbots**

Only **now** does retrieval make sense.

Students can:

* Embed user input
* Embed knowledge base documents
* Compare vectors
* Retrieve top results
* Respond deterministically or semi-generatively

At this point:

* They understand *every layer*
* Debugging becomes logical
* LLM usage becomes responsible, not magical

---

## Why This Beats “Jump to Retrieval”

| Jumping Early         | Your Approach             |
| --------------------- | ------------------------- |
| Feels like magic      | Feels logical             |
| Hard to debug         | Easy to reason about      |
| Copy-paste embeddings | Understands vectors       |
| Weak interviews       | Strong conceptual answers |

Your students will be able to answer:

> “How does a chatbot understand language?”

Most juniors cannot.

---

## Suggested Module Breakdown (Concrete)

Here’s a **clean module progression** that fits your curriculum:

1. **Regex & Rule-Based Chatbots** ✅
2. **Text Preprocessing for NLP**
3. **Tokenization & Vectorization**
4. **Intro to PyTorch for Language Data**
5. **Word Embeddings & Semantic Meaning**
6. **Vector Similarity & Search**
7. **Retrieval-Based Chatbots**
8. **Transition to LLM-Powered Systems**

This creates a **natural narrative arc**:

> Rules → Patterns → Numbers → Meaning → Retrieval → AI

Lesson 1 — Intro to Chatbots & Environment

Lecture 1

What are chatbots?

Rule vs Retrieval vs Generative

Deterministic vs probabilistic systems

Lecture 2

Python + Jupyter setup

First toy rule-based chatbot (if/else)

Lesson 2 — Regex & Rule-Based Chatbots

Lecture 1

Python regex fundamentals

Pattern matching & entity extraction

Lecture 2

Building a rule-based chatbot with regex

Intent routing & fallbacks

Lesson 3 — Language as Data

Lecture 1

Text preprocessing pipeline

Tokenization, normalization, lemmatization (NLTK)

Lecture 2

Bag of Words

N-grams

Feature vectors intuition

Lesson 4 — Classical Retrieval-Based Chatbots

Lecture 1

Information retrieval concepts

TF-IDF

Cosine similarity

Lecture 2

Building a retrieval-based chatbot (TF-IDF)

Response ranking

Lesson 5 — ML for Intent Classification

Lecture 1

Intent detection as classification

Train/test splits

Scikit-learn models

Lecture 2

Neural intent classification with PyTorch

Dataset creation & training loop

Lesson 6 — Semantic Retrieval & System Design

Lecture 1

Why classical retrieval fails

Sentence embeddings

sentence-transformers

Lecture 2

Hybrid chatbots (rules + retrieval)

Limits of classic systems

Bridge to generative models (Hugging Face preview)