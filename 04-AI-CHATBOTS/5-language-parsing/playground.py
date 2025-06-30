import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import RegexpParser, Tree
from nltk.corpus import wordnet, stopwords
from nltk import pos_tag

f = open("./resources/sci_fi_story.txt")
text = f.read()
f.close()

stop_words = stopwords.words("English")
lemmatizer = WordNetLemmatizer()

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
        return wordnet.NOUN
    


tokenized_text = sent_tokenize(text)
tokenized_text = [word_tokenize(sent) for sent in tokenized_text]

def remove_stopwords(sent):
    return [w for w in sent if w not in stop_words]

tagged_words = [pos_tag(remove_stopwords(sent)) for sent in tokenized_text]

chunk_grammar = r"""
  NP: {<DT>?<JJ.*>*<NN.*>+}         # Noun Phrases
  PP: {<IN><NP>}                    # Prepositional Phrases
  VP: {<VB.*><NP|PP|CLAUSE>*}       # Verb Phrases
  ADJP: {<RB.*>*<JJ.*>}             # Adjective Phrases
  ADVP: {<RB.*>+}                   # Adverb Phrases
"""


noun_phrase = r"""
  NP: {<DT>?<JJ.*>*<NN.*>+}   # Noun Phrase pattern
"""

np_filter = """NP: {<.*>+}
                    }<VB.?|IN>+{"""


verb_phrase = r"VP: {<VB.*><DT>?<JJ>*<NN><RB.?>?}"

filter_parser = RegexpParser(np_filter)
parser = RegexpParser(noun_phrase)

chunk_tree = parser.parse(tagged_words[20])
filtered_tree = parser.parse(tagged_words[20])

results = [parser.parse(sent) for sent in tagged_words]

# print(list(chunk_tree.subtrees(filter=lambda t: t.label() == 'NP')))
# print(tagged_words[20])
Tree.fromstring(str(chunk_tree)).pretty_print()
Tree.fromstring(str(filtered_tree)).pretty_print()

from collections import Counter

# function that pulls chunks out of chunked sentence and finds the most common chunks
def chunk_counter(chunked_sentences, label):

    # create a list to hold chunks
    chunks = list()

    # for-loop through each chunked sentence to extract noun phrase chunks
    for chunked_sentence in chunked_sentences:
        for subtree in chunked_sentence.subtrees(filter=lambda t: t.label() == label):
            chunks.append(tuple(subtree))

    # create a Counter object
    chunk_counter = Counter()

    # for-loop through the list of chunks
    for chunk in chunks:
        # increase counter of specific chunk by 1
        chunk_counter[chunk] += 1

    # return 30 most frequent chunks
    return chunk_counter.most_common(30)

most_common_vp_chunks = chunk_counter(results, 'VP')
# print(most_common_vp_chunks)
