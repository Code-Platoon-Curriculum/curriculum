# Vectorization

## Introduction

After text has been cleaned, normalized, and tokenized, we are still left with a critical problem:  
**computers cannot work with words—they work with numbers.**

Vectorization is the process that transforms structured text into numerical feature vectors so that mathematical operations can be performed on language. This step is what enables chatbots to compare messages, detect intent, retrieve responses, and learn from data.

In this lecture, we will explore classical vectorization techniques that form the foundation of many chatbot systems:
- Bag of Words
- N-grams
- TF-IDF

These methods do not attempt to understand language in a human sense. Instead, they represent text statistically—based on word occurrence and importance. While simple, these approaches are powerful enough to support real-world rule-based and retrieval-based chatbots.

Understanding vectorization at this level is essential before moving on to embeddings, neural networks, and transformer-based models.

## What does Vectorization do for a Chatbot

**Vectorization** is the process of converting human language (text) into **numerical representations** that a computer can understand and operate on. While earlier steps in text pre-processing—such as tokenization, stopword removal, stemming, and lemmatization—help clean and structure text, vectorization is the step that transforms this processed text into **numbers** that machine learning models can actually use.

Chatbots, whether rule-based, retrieval-based, or powered by deep learning, do not “understand” words the way humans do. Instead, they operate on vectors (arrays of numbers). Vectorization allows a chatbot to:
- Compare user inputs mathematically
- Measure similarity between messages
- Classify intent
- Retrieve relevant responses
- Feed text into machine learning and neural network models

Without vectorization, text remains symbolic and cannot be used for statistical analysis or learning. Vectorization is therefore the **bridge between language and machine intelligence**, enabling chatbots to make decisions based on patterns in text rather than hard-coded rules.

## Bag of Words (BoW)

The **Bag of Words** model is one of the simplest and most commonly taught vectorization techniques in NLP. It represents text by counting how often each word appears, completely ignoring grammar and word order. Each sentence or document becomes a vector where:
- Each position corresponds to a word in the vocabulary
- The value represents the frequency of that word

For chatbots, Bag of Words is useful for:
- Intent classification
- Keyword-based matching
- Simple retrieval systems
- Understanding *what* words are present, even if not *how* they are ordered

Although BoW does not capture context or meaning, it provides a clear and intuitive introduction to how text can be converted into numbers.

### Applying Bag of Words with Python

We’ll use `CountVectorizer` from `scikit-learn`, a standard tool for vectorization in NLP pipelines. You'll notice this class expects a list of sentences so we will have to join all of our sentences and then pass them through our *vectorizer* to see it provide us with both the amount of features it was able to identify and a numpy array that could be utilized for machine learning.

```python
from sklearn.feature_extraction.text import CountVectorizer
final_story = [" ".join(sent) for sent in lemmatized_story]
# Create the vectorizer
vectorizer = CountVectorizer()

# Fit and transform the text
bow_vectors = vectorizer.fit_transform(final_story)
print(vectorizer.get_feature_names_out())
print(bow_vectors.toarray())
```

---

### Why This Matters Before Deep Learning

Bag of Words may seem simple, but it introduces **core NLP ideas** that carry forward into more advanced models:

* Vocabulary construction
* Feature extraction
* Numerical representations of language
* Similarity and comparison of text

Modern deep learning models (including embeddings and transformers) build on these same principles—just in more sophisticated ways. By mastering vectorization at this level, students gain a strong mental model for how chatbots *interpret*, *compare*, and *reason about* language before moving into neural networks and PyTorch-based approaches.

## N-Grams Vectorization

While **Bag of Words** treats each word independently, **N-grams** extend this idea by capturing *sequences of words*. An **N-gram** is a contiguous group of `N` tokens:

* **Unigram (1-gram)** → `"chatbot"`
* **Bigram (2-gram)** → `"chat bot"`
* **Trigram (3-gram)** → `"build a chatbot"`

Instead of only asking *“what words appear?”*, N-grams help answer:

> *“What words appear **together**?”*

This makes N-grams especially useful for:

* Capturing short phrases and word relationships
* Improving intent detection (e.g. `"reset password"` vs `"reset"` and `"password"`)
* Disambiguating meaning that single words alone cannot express
* Slightly improving context awareness without using deep learning

N-grams still do **not** fully understand language or semantics, but they provide an important bridge between simple word counts and more advanced models.

---

### Applying N-Grams with Python

Just like Bag of Words, we’ll continue using `CountVectorizer`. The key difference is configuring the `ngram_range` parameter.

Because we already:

* Cleaned the text
* Tokenized sentences
* Applied POS-aware lemmatization
* Rejoined tokens into full sentences

We can reuse our existing `final_story` list directly.

```python
from sklearn.feature_extraction.text import CountVectorizer

# Create an N-gram vectorizer (bigrams in this example)
ngram_vectorizer = CountVectorizer(ngram_range=(2, 2))

# Fit and transform the text
ngram_vectors = ngram_vectorizer.fit_transform(final_story)

# Inspect learned features and vectors
print(ngram_vectorizer.get_feature_names_out())
print(ngram_vectors.toarray())
```

---

### Understanding `ngram_range`

The `ngram_range` parameter controls the size of word sequences extracted:

* `(1, 1)` → Unigrams (Bag of Words)
* `(2, 2)` → Bigrams only
* `(1, 2)` → Unigrams **and** bigrams
* `(2, 3)` → Bigrams and trigrams

Example:

```python
CountVectorizer(ngram_range=(1, 2))
```

This allows the model to learn both:

* Individual keywords
* Common word pairings

---

### Why N-Grams Matter for Chatbots

For chatbot systems, N-grams help bridge the gap between:

* **Keyword-based logic** (rule-based systems)
* **Intent classification** (machine learning models)

They allow the model to distinguish between:

* `"turn on"` vs `"turn"`
* `"log in"` vs `"log"`
* `"customer support"` vs `"customer"`

This additional structure often leads to **significantly better performance** than pure Bag of Words, while remaining simple enough to understand and debug.

## Feature Vectors Intuition

A **feature vector** is a numerical representation of text where each dimension corresponds to a specific feature—typically a word or phrase from the vocabulary.

In Bag of Words and N-gram models:
- Each sentence becomes a vector
- Each position in the vector represents a word or phrase
- Each value represents how often that feature appears

For example, given a vocabulary:

```python
["chatbot", "help", "reset", "password"]
```

The sentence:

```python
"reset password"
```

Might be represented as:

```python
[0, 0, 1, 1]
```


Even though this vector looks simple, it allows us to:
- Compare sentences using distance metrics
- Measure similarity using cosine similarity
- Train classifiers to detect intent
- Retrieve the closest matching response

### Sparse Representations

Most classical NLP vectorization techniques produce **sparse vectors**:
- The vocabulary may contain thousands of features
- Each sentence uses only a few of them
- Most values are zero

This sparsity makes classical models:
- Fast
- Memory-efficient
- Easy to debug

However, it also means they lack deep semantic understanding—an important limitation we will revisit later.

## TF-IDF (Term Frequency–Inverse Document Frequency)

While Bag of Words and N-grams count how often words appear, they treat **all words as equally important**. In practice, this is rarely true.

TF-IDF improves upon Bag of Words by weighting words based on:
- How frequently they appear in a document (**Term Frequency**)
- How rare they are across all documents (**Inverse Document Frequency**)

### Intuition Behind TF-IDF

TF-IDF answers a more useful question:

> *“How important is this word to this specific sentence, relative to the entire corpus?”*

Words that:
- Appear often in one sentence  
- But rarely across all sentences  

Receive **higher weights**.

Common words that appear everywhere (e.g. *“the”*, *“is”*, *“and”*) receive lower weights—even if they occur frequently.

---

### TF-IDF Formula (Conceptual)

TF-IDF is computed as:

```python
TF-IDF(word) = TF(word) × IDF(word)
```

Where:

- **TF (Term Frequency)** measures how often a word appears in a document
- **IDF (Inverse Document Frequency)** measures how rare the word is across documents

You do not need to compute this manually—libraries handle it for us—but understanding the intuition is critical.

---

### Applying TF-IDF with Python

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Create TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the text
tfidf_vectors = tfidf_vectorizer.fit_transform(final_story)

# Inspect features and vectors
print(tfidf_vectorizer.get_feature_names_out())
print(tfidf_vectors.toarray())
```

### Why TF-IDF Matters for Chatbots

TF-IDF is especially useful for:

- Retrieval-based chatbots
- FAQ systems
- Intent classification
- Similarity-based response matching

Compared to raw word counts, TF-IDF:

- Reduces the impact of common words
- Highlights distinguishing terms
- Often improves accuracy without increasing complexity

This makes it one of the most effective classical techniques for real-world chatbot systems.

## Conclusion

Vectorization is the step where text becomes actionable data. By converting language into numerical feature vectors, we enable chatbots to compare, classify, and retrieve information using mathematical methods rather than hard-coded rules.

In this lecture, we explored three foundational vectorization techniques:
- **Bag of Words**, which captures word presence and frequency
- **N-grams**, which add limited word order and phrase awareness
- **TF-IDF**, which weights words based on their importance across documents

These methods form the backbone of many classic chatbot systems. While they do not understand meaning or context, they are fast, interpretable, and highly effective for intent detection and retrieval tasks.

In the next lessons, we will build on these ideas to:
- Measure similarity between user inputs
- Implement retrieval-based chatbots
- Explore the limitations of classical vectorization
- Transition toward embeddings and modern NLP approaches

Mastering vectorization at this level gives you a clear mental model for how chatbots *process* language—before we teach them to *learn* from it.
