# Intro to Language Parsing

![dep_parse](./resources/parse_tree_depndncy_graph.jpeg)

## What is Language Parsing in NLP?

**Language parsing in Natural Language Processing (NLP)** refers to the process of analyzing and breaking down a text or sentence into its grammatical components to understand its structure and meaning. Parsing involves identifying the roles that individual words play (such as nouns, verbs, adjectives, etc.) and how they relate to one another within the sentence, typically by generating a syntactic representation like a parse tree or dependency graph. This structured representation helps machines interpret the hierarchical relationships and dependencies between words—such as which noun a verb is acting upon or how clauses are connected. Parsing is essential for many NLP tasks including machine translation, question answering, sentiment analysis, and chatbot intent detection, as it enables systems to move beyond simple word matching and towards understanding the syntax and, indirectly, the semantics of a sentence. There are different types of parsing approaches in NLP, such as **constituency parsing** (which focuses on dividing a sentence into nested sub-phrases) and **dependency parsing** (which focuses on the direct relationships between words). Accurate language parsing allows NLP systems to grasp the meaning and intent behind human language with greater precision, facilitating more natural and contextually appropriate responses.

## Reviewing Regex Methods

In this section we will review key methods of Python’s built-in `re` module, which help us search, match, and extract patterns from text. These tools are valuable for cleaning and analyzing large text files, like our science fiction story.

### `re.match`

`re.match()` checks if a pattern appears at the **very beginning** of a string. If it finds a match at the start, it returns a match object; otherwise, it returns `None`.

```python
import re

with open("./resources/sci_fi_story.txt", "r") as file:
    text = file.read()

# Check if the text starts with 'Title'
match_result = re.match(r"Title", text)

if match_result:
    print("Match found at start of text:", match_result.group())
else:
    print("No match found at start of text.")
```

### `re.search`

`re.search()` scans the **entire string** and returns a match object for the **first occurrence** of the pattern it finds, or `None` if no match exists.

```python
# Search for the first occurrence of 'machine'
search_result = re.search(r"machine", text)

if search_result:
    print(f"'machine' found at position {search_result.start()}: {search_result.group()}")
else:
    print("No occurrence of 'machine' found.")
```

### `re.findall`

`re.findall()` searches the full string and returns a **list of all non-overlapping matches** of the pattern.

```python
# Find all instances of 'Elara'
all_elara = re.findall(r"Elara", text)
print(f"'Elara' appears {len(all_elara)} times in the text.")
```

By mastering these methods, you can efficiently analyze, clean, and process textual data in your NLP projects.

## Part-of-Speech (POS) Tagging with NLTK

In traditional grammar and NLP, **Part of Speech (POS)** refers to the category a word belongs to based on its role in a sentence. While there are many fine-grained tags (like `NNP` or `VBG` in NLTK), they map to **9 core parts of speech** that form the foundation of English grammar. These are:

1. **Noun (N)** – Names a person, place, thing, or idea.
   *Example:* `cat`, `London`, `happiness`

2. **Pronoun (PRON)** – Replaces a noun to avoid repetition.
   *Example:* `he`, `she`, `they`, `it`

3. **Verb (V)** – Expresses action, state, or being.
   *Example:* `run`, `is`, `study`

4. **Adjective (ADJ)** – Describes or modifies a noun.
   *Example:* `happy`, `blue`, `large`

5. **Adverb (ADV)** – Modifies a verb, adjective, or other adverb, often showing how, when, where, or to what extent.
   *Example:* `quickly`, `very`, `happily`

6. **Preposition (PREP)** – Shows the relationship between a noun (or pronoun) and another word.
   *Example:* `on`, `in`, `at`, `by`

7. **Conjunction (CONJ)** – Connects words, phrases, or clauses.
   *Example:* `and`, `but`, `or`

8. **Interjection (INTJ)** – Expresses emotion or exclamation.
   *Example:* `Wow!`, `Oh!`, `Hey!`

9. **Determiner (DET)** – Introduces a noun and specifies it as known or unknown.
   *Example:* `the`, `a`, `this`, `those`

In **NLTK POS tagging**, these 9 core parts of speech are expanded into detailed tags (like `NN` for singular noun or `VBP` for plural verb) that offer more specific grammatical information.

**Part-of-Speech (POS) tagging** is the process of labeling each word in a sentence with its grammatical role—such as noun, verb, adjective, or adverb—based on its context and function within the sentence. This step is essential in NLP because it helps models understand the structure and meaning of text, supporting tasks like parsing, intent recognition, and lemmatization.

Let’s look at an example sentence and apply POS tagging using NLTK:

```python
from nltk.tokenize import word_tokenize
from nltk import pos_tag

sentence = "Wow! Ramona and her class are happily studying the new textbook she has on NLP."
tokens = word_tokenize(sentence)
tagged = pos_tag(tokens)

print(tagged)
```

The output might look like this:

```python
[('Wow', 'UH'),
 ('!', '.'),
 ('Ramona', 'NNP'),
 ('and', 'CC'),
 ('her', 'PRP$'),
 ('class', 'NN'),
 ('are', 'VBP'),
 ('happily', 'RB'),
 ('studying', 'VBG'),
 ('the', 'DT'),
 ('new', 'JJ'),
 ('textbook', 'NN'),
 ('she', 'PRP'),
 ('has', 'VBZ'),
 ('on', 'IN'),
 ('NLP', 'NNP'),
 ('.', '.')]
```

### Breakdown of POS Abbreviations

| **Tag** | **Part of Speech**                  | **Example from Sentence**                         |
| ------- | ----------------------------------- | ------------------------------------------------- |
| `UH`    | Interjection                        | `Wow` – shows surprise or emotion                 |
| `.`     | Punctuation                         | `!`, `.` – punctuation marks                      |
| `NNP`   | Proper Noun                         | `Ramona`, `NLP` – names of specific people/things |
| `CC`    | Coordinating Conjunction            | `and` – connects words or phrases                 |
| `PRP$`  | Possessive Pronoun                  | `her` – shows ownership                           |
| `NN`    | Noun (Singular)                     | `class`, `textbook` – names of things             |
| `VBP`   | Verb (Present, plural)              | `are` – plural present tense verb                 |
| `RB`    | Adverb                              | `happily` – modifies the verb `studying`          |
| `VBG`   | Verb (Gerund/Participle)            | `studying` – verb ending in -ing                  |
| `DT`    | Determiner                          | `the` – specifies a noun                          |
| `JJ`    | Adjective                           | `new` – describes the noun `textbook`             |
| `PRP`   | Personal Pronoun                    | `she` – refers to a person                        |
| `VBZ`   | Verb (Present, 3rd person singular) | `has` – present tense verb for `she`              |
| `IN`    | Preposition                         | `on` – shows relationship (e.g., `on NLP`)        |

POS tagging with NLTK assigns these tags automatically using built-in models trained on large corpora. The tags help define **how each word functions** in its sentence context, enabling deeper analysis like parsing, dependency resolution, or lemmatization based on grammar. This detailed labeling is fundamental in building NLP systems that can accurately interpret and generate human-like language.

## Chunking Techniques with NLTK's RegexParser

### What is chunking?

**Chunking** in NLP refers to the process of grouping individual tokens (usually words) into larger, meaningful units called **chunks**. These chunks typically represent **phrases**, such as noun phrases (NP), verb phrases (VP), or prepositional phrases (PP). While **part-of-speech (POS) tagging** labels each word with its grammatical role (e.g., noun, verb), chunking combines these POS-tagged tokens into coherent segments, like `"the new textbook"` → NP. In simple terms, chunking helps identify and extract small structures that represent parts of meaning within a sentence.

### Why is chunking an important step of NLP?

* It helps capture **phrase-level structures** rather than just word-level details, enabling deeper syntactic and semantic analysis.
* Many NLP tasks—such as **entity recognition**, **question answering**, and **relation extraction**—rely on phrase-level understanding.
* It reduces complexity by organizing sequences of tokens into higher-order units, making it easier for models to process relationships and patterns in text.
* By identifying key phrases (like subject noun phrases or object noun phrases), chunking improves downstream tasks like intent detection in chatbots or parsing for machine translation.

### Types of Chunking in NLP

| **Phrase Type**                | **Tag (Conventional)**                | **What It Represents**                                                  | **Example**                             |
| ------------------------------ | ------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------- |
| **Noun Phrase (NP)**           | `NP`                                  | A group centered around a noun, possibly with determiners or adjectives | *"the big spaceship"*                   |
| **Verb Phrase (VP)**           | `VP`                                  | A main verb plus its auxiliaries, adverbs, and objects                  | *"has been running quickly"*            |
| **Prepositional Phrase (PP)**  | `PP`                                  | A preposition followed by its object (usually a NP)                     | *"on the table"*, *"under the stars"*   |
| **Adjective Phrase (ADJP)**    | `ADJP`                                | A phrase with an adjective as its head, possibly modified               | *"very happy"*, *"extremely difficult"* |
| **Adverb Phrase (ADVP)**       | `ADVP`                                | A phrase with an adverb as its head, possibly modified                  | *"quite slowly"*, *"too fast"*          |
| **Determiner Phrase (DP)**     | `DP` (less common in shallow parsing) | A phrase centered around a determiner                                   | *"some of the"*                         |
| **Quantifier Phrase (QP)**     | `QP`                                  | A phrase expressing quantity                                            | *"many of these"*, *"all the books"*    |
| **Conjunction Phrase (CONJP)** | `CONJP`                               | A conjunction with modifiers                                            | *"as well as"*, *"but not"*             |

## Conclusion

Language parsing is a foundational skill in Natural Language Processing (NLP), enabling us to break down raw text into structured, meaningful components that machines can understand and work with. Throughout this lecture, we explored how parsing works—from identifying individual parts of speech to grouping words into higher-order chunks like noun phrases, verb phrases, and prepositional phrases. We saw how tools like **regular expressions**, **POS tagging**, and **chunking with NLTK's `RegexpParser`** help us systematically analyze sentence structure.

Parsing is more than just a technical step—it’s what allows NLP systems to move beyond simple word lists and begin to grasp the relationships between words, phrases, and ideas. Whether you're building a chatbot, performing information extraction, or preparing data for machine learning models, understanding parsing gives you the power to create systems that interact with language in a more natural, human-like way.

As you continue practicing with regex, POS tagging, and chunk filtering, remember: mastering parsing equips you to tackle a wide range of NLP tasks, from intent recognition to semantic analysis. It’s a critical bridge between raw language data and intelligent applications.
