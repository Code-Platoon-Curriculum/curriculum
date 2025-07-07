# Retrieval Based Chatbots

## Language Modeling

### BoW(Bag of Words) == The Unigram Model

“A bag-of-words is all you need,” some NLPers have decreed.

The model has many, many use cases including:

- determining topics in a song
- filtering spam from your inbox
- finding out if a tweet has positive or negative sentiment
- creating word clouds

#### How does it work

This should be done **AFTER** Language Pre-processing techniques like tokenization, and lemmatization.

It only cares about word count and how commonly words appear within a document. Doesn't care about patterns or any frequency only volume of words within the document.

ex: “Five fantastic fish flew off to find faraway functions. Maybe find another five fantastic fish?”

some models may highlight that all words start with the letter 'f' and that words that start with the letter 'f' may be important. Other models may recognize the word fish only appears after the word fantastic and take that into note. Bag of Words would only annotate that 'another' and 'fish' are commonly found and likely key words within this text.

#### Simple Implementation of a BOW

The easiest way to accomplish the BoW concept in Python iw by creating a dictionary that will create a key for each new word introduced to the dictionary with the value of 1 and increment said value every time the same word appears.

```python
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import re

def get_part_of_speech(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to noun if unknown


def preprocess_text(text):
    normalizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("English"))
    cleaned = re.sub(r'\W+', ' ', text).lower()
    tokenized = pos_tag(word_tokenize(cleaned))
    normalized = [normalizer.lemmatize(word, get_part_of_speech(tag)) for word, tag in tokenized if word not in stop_words]
    return normalized

def text_to_bow(some_text):
  bow_dictionary = {}
  tokens = preprocess_text(some_text)
  for word in tokens:
    if word in bow_dictionary:
      bow_dictionary[word] += 1
    else:
      bow_dictionary[word] = 1
  return bow_dictionary

print(text_to_bow("I love fantastic flying fish. These flying fish are just ok, so maybe I will find another few fantastic fish..."))
```

#### Efficient Feature Vector

##### What is a Feature Vector 

##### Why does it help improve the BOW Method

##### Building a Feature Vector in Python

### Term Frequency-Inverse Document Frequency (tf-idf)

### Word2Vec