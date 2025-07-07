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