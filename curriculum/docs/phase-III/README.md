# Phase III – Artificial Intelligence & ChatBots

## Overview

Phase III transitions students from full-stack application development into the field of **artificial intelligence and conversational systems**. In this phase, students learn how machines process, interpret, and respond to human language—moving from hand-crafted rules to data-driven representations and, ultimately, toward machine learning-powered chatbot systems. The emphasis shifts from building connected web applications to understanding **how language itself can be treated as data** and transformed into structures that enable intelligent behavior.

By the end of Phase III, students will understand the full arc of classic chatbot development—from deterministic rule-based systems, through NLP preprocessing pipelines and numerical text representations, to retrieval-based and intent classification models. They will gain hands-on experience building chatbots in Python, implementing NLP preprocessing pipelines, applying vectorization techniques such as Bag of Words and TF-IDF, and training machine learning models for intent detection. This phase establishes the theoretical and practical foundation required for working with large language models and generative AI systems in later phases.

---

## Modules

### [Module 7 – Classic ChatBots](./07-Classic-Chatbots/README.md)

Module 7 introduces students to the history, architecture, and technical progression of conversational AI systems, beginning with a conceptual overview of what chatbots are and how they have evolved. Students explore the differences between rule-based, retrieval-based, and generative chatbots, and set up a Python-based machine learning development environment using virtual environments, Jupyter Notebook, and foundational libraries including PyTorch, scikit-learn, pandas, and NumPy.

The module then focuses on pattern matching as a foundation for conversational logic. Students learn regular expressions in depth—using `re` module tools to detect, extract, and validate patterns in free-form user input. This knowledge is applied directly to building rule-based chatbots in Python, where students design conversation loops, map input patterns to deterministic responses, and apply input normalization techniques such as lowercasing and whitespace stripping. By working through the power and limitations of rule-based systems, students develop the motivation for more sophisticated data-driven approaches.

From there, the module transitions into treating language as data. Students implement a complete NLP preprocessing pipeline covering tokenization, normalization, stopword removal, and lemmatization, then explore how processed text is converted into numerical feature vectors using Bag of Words, N-grams, and TF-IDF. These representations serve as the backbone for intent classification and retrieval-based chatbot systems. Students gain a concrete understanding of why this transformation layer exists and how it bridges rule-based logic and machine learning models.

The module continues into classical retrieval-based chatbot design, where students apply TF-IDF and cosine similarity to rank and return the most relevant responses to a user query. Intent classification is introduced through scikit-learn and PyTorch, where students build and train models to predict user intent from vectorized input. The module concludes with semantic retrieval using sentence embeddings, exposing the limitations of classical representations and preparing students for the transition to generative, LLM-powered systems.

---

## Technologies

Throughout Phase III, students work with the following tools and technologies:

<p align="left">

<a href="https://www.python.org/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/>
</a>

<a href="https://jupyter.org/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/jupyter/jupyter-original.svg" alt="jupyter" width="40" height="40"/>
</a>

<a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/>
</a>

<a href="https://numpy.org/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg" alt="numpy" width="40" height="40"/>
</a>

<a href="https://pytorch.org/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pytorch/pytorch-original.svg" alt="pytorch" width="40" height="40"/>
</a>

<a href="https://scikit-learn.org/" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scikitlearn/scikitlearn-original.svg" alt="scikit-learn" width="40" height="40"/>
</a>

</p>
