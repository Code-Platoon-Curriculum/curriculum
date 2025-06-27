from nltk.tokenize import sent_tokenize, word_tokenize
import re

file = open("./resources/full-stack-quest.md")
text_from_file = file.read()
file.close()

clean_text = re.sub(r'[#|*|-|_|\U0001F525]', '', text_from_file)

story_tokenized_by_word = word_tokenize(clean_text)
print(story_tokenized_by_word)