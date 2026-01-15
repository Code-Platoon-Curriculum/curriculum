# Intro to Regex

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

### Regex and NLP

Regular Expressions (regex) in Python are powerful tools used to search, match, and manipulate text. In NLP, regex is often used during the pre-processing stage to clean and extract useful patterns from text. It allows developers to identify and handle structures like emails, phone numbers, dates, or specific word patterns quickly and efficiently.

In rule-based chatbots, regex is often the primary mechanism used to interpret user input. Rather than “understanding” language, the chatbot matches patterns in text to predefined rules, allowing it to classify intent, validate input, and trigger responses.

### Why Regex?

Regex becomes extremely helpful in various text processing scenarios, such as:

* Detecting and extracting emails or phone numbers from user input
* Removing unwanted symbols or extra whitespaces
* Identifying patterns such as hashtags, mentions, or URLs in social media content
* Matching time formats, dates, or currency patterns
* Filtering out profane or restricted words from text

### How does it work?

Regex works by using a sequence of characters that defines a search pattern. When applied to a string, the regex engine reads the pattern and scans through the text to find matches. Each symbol or character in a regex pattern has a specific meaning—some match literal characters, while others serve as wildcards, quantifiers, or groups. The engine can perform a variety of tasks such as searching, replacing, splitting, or extracting substrings. Regex engines operate using state-based pattern matching, scanning text sequentially and transitioning between states until a match succeeds or fails, moving through a text one character at a time based on the defined rules until a match is found or the search ends.

## Applying Regex

### Character Matching

**Example Situation:** You want to validate whether an input contains only alphabetic characters.

**Why this utility is the right one for the situation:** Character matching allows you to match specific letters or characters within text, making it ideal for validation checks.

**Code Examples:**

```python
import re
re.match(r"^[a-zA-Z]+$", "Hello")  # Match only letters
re.match(r"^[a-z]+$", "world")       # Match only lowercase
re.match(r"^[A-Z]+$", "TEST")        # Match only uppercase
```

### Alternation

**Example Situation:** You want to accept either "yes" or "no" from user input.

**Why this utility is the right one for the situation:** Alternation lets you match one out of multiple possible patterns.

**Code Examples:**

```python
re.match(r"yes|no", "yes")
re.match(r"cat|dog|bird", "dog")
re.search(r"apple|orange|banana", "I like orange juice")
```

### Character Sets and Negated Character Sets

**Example Situation:** You want to detect any digit or symbol in a string.

**Why this utility is the right one for the situation:** Character sets allow you to match specific ranges or types of characters, while negated sets match everything *except* what's specified.

**Code Examples:**

```python
re.search(r"[0-9]", "My phone number is 555-1234")
re.search(r"[^a-zA-Z0-9]", "password!@#")
re.findall(r"[aeiou]", "education")
```

### Wild Cards

**Example Situation:** You want to match any character in a specific position.

**Why this utility is the right one for the situation:** The dot (`.`) wildcard matches any single character.

**Code Examples:**

```python
re.match(r"h.t", "hat")
re.match(r"c.r", "car")
re.search(r".at", "I have a cat")
```

> *Note:*

> re.match() checks for a pattern only at the beginning of a string, while re.search() scans the entire string for a match.

### Ranges

**Example Situation:** You want to match characters between a certain range like a–z or 0–9.

**Why this utility is the right one for the situation:** Ranges offer a concise way to represent multiple characters.

**Code Examples:**

```python
re.match(r"[a-z]", "g")
re.match(r"[A-Z]", "T")
re.search(r"[0-5]", "There are 3 items")
```

### Shorthand Character Classes

**Example Situation:** You want to quickly check if a string contains a digit, a word character, or whitespace.

**Why this utility is the right one for the situation:** Shorthand character classes simplify common character set patterns.

**Code Examples:**

```python
re.search(r"\d", "Room 101")     # Matches digit
re.search(r"\w", "hello_world") # Matches word character
re.search(r"\s", "hello world")  # Matches space

re.search(r"\D", "A1")           # Matches non-digit
re.search(r"\W", "abc!")         # Matches non-word character
re.search(r"\S", " 123")         # Matches non-whitespace
```

### Grouping

**Example Situation:** You want to extract both area code and phone number from a string.

**Why this utility is the right one for the situation:** Grouping lets you extract and operate on specific portions of a match.

**Code Examples:**

```python
re.match(r"(\d{3})-(\d{4})", "555-1234")
re.search(r"(Mr|Ms|Dr)\.\s\w+", "Dr. Smith")
re.findall(r"(\w+)@(\w+\.com)", "email@example.com")
```

### Quantifiers Fixed

**Example Situation:** You want to match a word with exactly 4 letters.

**Why this utility is the right one for the situation:** Fixed quantifiers ensure a precise number of matches.

**Code Examples:**

```python
re.match(r"^\w{4}$", "test")
re.match(r"\d{5}", "90210")
re.search(r"\w{3}\d{2}", "abc12")
```

### Quantifiers Optional

**Example Situation:** You want to match both "color" and "colour".

**Why this utility is the right one for the situation:** Optional quantifiers match the presence or absence of a character.

**Code Examples:**

```python
re.match(r"colou?r", "color")
re.match(r"colou?r", "colour")
re.search(r"Nov(ember)?", "November")
```

### Quantifiers One or More

**Example Situation:** You want to match a sequence of one or more digits.

**Why this utility is the right one for the situation:** This ensures there’s at least one match but allows for many.

**Code Examples:**

```python
re.match(r"\d+", "123")
re.search(r"[a-z]+", "hello")
re.findall(r"\w+", "Find all words in this sentence.")
```

### Anchors

**Example Situation:** You want to check if a string starts or ends with a specific word.

**Why this utility is the right one for the situation:** Anchors are used to match patterns at the start (^) or end (\$) of a string.

**Code Examples:**

```python
re.match(r"^Hello", "Hello world")
re.search(r"world$", "Hello world")
re.match(r"^\d+$", "12345")
```

### Additional Tools

Other useful regex tools include:

* **Lookaheads and Lookbehinds**: Match patterns based on what comes before or after without including it in the match.
* **Non-capturing groups**: Useful for grouping without saving memory.
* **Flags**: Such as `re.IGNORECASE`, `re.MULTILINE`, and `re.DOTALL` to alter matching behavior.

These tools provide even more flexibility when parsing complex language structures.

Here’s a concise and informative **summary** you can attach to the end of your `intro-to-nlp-and-regex.md` lecture:

## Conclusion

In this lecture, we introduced **Natural Language Processing (NLP)** as a critical component of chatbot development, enabling machines to understand and work with human language. We explored the key stages of **text pre-processing**, including noise removal, tokenization, and normalization techniques like stemming and lemmatization, which prepare raw text for intelligent analysis.

We then examined how **Regular Expressions (regex)** are used within NLP workflows to detect patterns, clean data, and extract meaningful elements from user input. With detailed examples, we covered the full spectrum of regex tools—from basic character matching and wildcards to powerful quantifiers, grouping, and anchors—equipping you with essential skills for building rule-based language systems.

Together, these concepts form the foundation of rule-based chatbot logic, where understanding structure, syntax, and pattern recognition is vital to creating accurate, flexible, and efficient conversational flows.
