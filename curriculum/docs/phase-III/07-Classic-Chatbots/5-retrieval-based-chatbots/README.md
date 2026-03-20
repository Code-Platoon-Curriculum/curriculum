# Retrieval-Based ChatBots

## What are we trying to accomplish?

In this lesson, students will learn how to move beyond rigid rule-based systems by building **retrieval-based chatbots** that select responses through similarity matching rather than predefined logic. Beginning with the conceptual shift from rule checking to semantic retrieval, students will explore how text is converted into numerical vectors using Bag of Words, TF-IDF, and word embeddings, and how **cosine similarity** is used to measure closeness between a user's message and known intent patterns. Students then apply these concepts by building a full retrieval pipeline powered by **Sentence-BERT** and **FAISS**, enabling the chatbot to understand paraphrased input and retrieve semantically relevant responses efficiently. By the end of this lesson, students will have implemented a functioning retrieval-based chatbot in Python and will understand how this architecture forms the foundation for modern Retrieval-Augmented Generation (RAG) systems.

---

## Lectures & Assignments

### Lectures

* [Lecture - Understanding Retrieval-Based ChatBots](./1-understanding-rbc.md)
* [Lecture - Building a Retrieval-Based ChatBot](./2-building-rbc.md)

### [Assignments](./assignments.md)

---

## TLO's (Terminal Learning Objectives)

* Explain the architectural difference between rule-based and retrieval-based chatbots
* Apply vectorization techniques to convert user input into comparable numerical representations
* Measure text similarity using cosine similarity to rank and retrieve relevant responses
* Build a retrieval-based chatbot using TF-IDF and cosine similarity
* Implement semantic retrieval using Sentence-BERT embeddings and a FAISS similarity index
* Construct an interactive chat loop that handles free-form user input against a JSON intent dataset

---

## ELO's (Enabling Learning Objectives)

* How retrieval-based chatbots differ from rule-based systems in logic, scalability, and flexibility
* What intents are and how they group semantically equivalent user messages
* Why rule-based intent matching becomes unscalable and how vectorization addresses its limitations
* How Bag of Words represents text as sparse frequency vectors across a vocabulary
* How TF-IDF improves on Bag of Words by weighting rare, informative words more heavily
* What word embeddings are and how they encode semantic meaning and word relationships as dense vectors
* How cosine similarity measures directional closeness between two vectors independent of magnitude
* What BERT is and why bidirectional contextual embeddings outperform classical text representations
* How FAISS enables fast nearest-neighbor search over large sets of sentence embeddings
* The end-to-end architecture of a retrieval pipeline: encode → search → match intent → return response
* How confidence thresholds, cross-encoders, and vector databases extend a basic retrieval chatbot
* How retrieval-based systems serve as the foundation for Retrieval-Augmented Generation (RAG)
