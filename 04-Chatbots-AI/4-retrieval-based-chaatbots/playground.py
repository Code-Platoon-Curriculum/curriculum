from utilities import preprocess_text

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