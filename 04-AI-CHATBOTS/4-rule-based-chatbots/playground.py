from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import re

file = open("./resources/full-stack-quest.md")
text_from_file = file.read()
file.close()

clean_text = re.sub(r"[#|*|-|_|\U0001F525]", "", text_from_file)

story_tokenized_by_word = word_tokenize(clean_text)
# print(len(story_tokenized_by_word))

stop_words = set(stopwords.words("english"))
stopwords_removed = [word for word in story_tokenized_by_word if word not in stop_words]

# print(len(stopwords_removed))
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(w) for w in stopwords_removed]
# print(stemmed_words)

from nltk.stem import WordNetLemmatizer

from nltk import pos_tag
lemmatizer = WordNetLemmatizer()
# Tag each word with its part of speech
tagged_words = pos_tag(stopwords_removed)

from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):
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

lemmatized_words_with_pos = [
    lemmatizer.lemmatize(word, get_wordnet_pos(pos_tag))
    for word, pos_tag in tagged_words
]

print(lemmatized_words_with_pos)