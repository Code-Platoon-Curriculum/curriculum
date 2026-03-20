## What is NLP?

Natural Language Processing (NLP) is a subfield of artificial intelligence and linguistics that focuses on enabling computers to understand, interpret, generate, and respond to human languages in a valuable way. NLP bridges the gap between human communication and computer understanding by applying techniques from linguistics, machine learning, and statistics to analyze and process textual and spoken language data. From virtual assistants and ChatBots to language translation and sentiment analysis, NLP is foundational in helping machines interact with people using natural language.

### What is Text Pre-processing?

Text pre-processing is the essential first step in any NLP task. It involves cleaning and preparing raw textual data so that it can be efficiently analyzed by NLP algorithms. Since language data can be messy, inconsistent, or filled with irrelevant symbols, text pre-processing improves data quality and relevance for downstream tasks.

* **Noise Removal**
  Noise refers to unwanted characters or formatting in text such as HTML tags, punctuation, numbers, special characters, or extra whitespaces. Removing noise helps focus on the actual words and their meaning, improving the performance of text-based models.

* **Tokenization**
  Tokenization is the process of splitting text into individual units called tokens, which can be words, phrases, or symbols. This step allows NLP models to analyze language at a granular level, making it easier to process and extract patterns.

* **Normalization**
  Normalization transforms text into a more consistent format by lowering case, removing variations, or converting different forms of words into a base form.

    * **Stemming**
      Stemming is a process that cuts off word suffixes to reduce words to their root form. For example, "running" and "runner" might both be reduced to "run". Stemming is quick but can sometimes yield non-dictionary words.

    * **Lemmatization**
      Lemmatization reduces words to their base or dictionary form (lemma), taking into account the context and part of speech. For example, "was" becomes "be" and "better" becomes "good". This approach is more accurate than stemming, though computationally heavier.