import re
from collections import OrderedDict

stop_words = set();
final_ngrams = {};

def split_desc_to_words(desc):
  res = "";
  res = re.sub(r"(([^a-zA-Z])+(')([^a-zA-Z])+|([^a-zA-Z])+(')|(')([^a-zA-Z])+|[^a-zA-Z']+)", " ", desc);
  res = re.sub(r"\\s+", " ", res);
  res = re.sub(r"(^(\\s+)|(\\s+)$)", "", res);
  res = res.lower();

  return res.split(" ");

def clean_word(word):
  res = "";
  res = re.sub(r"(([^a-zA-Z])+(')([^a-zA-Z])+|([^a-zA-Z])+(')|(')([^a-zA-Z])+|[^a-zA-Z']+)", " ", desc);
  res = re.sub(r"\\s+", " ", res);
  res = re.sub(r"(^(\\s+)|(\\s+)$)", "", res);
  res = res.lower();

  return res;

# read from in put and build a set of stopwords
def build_stop_words_set():
  src = open('stop_words', 'r');

  for line in src:
      stopword = line.rstrip('\n');
      stop_words.add(stopword);

  src.close()
  return;

def generate_ngram_keywords(keywords, mult):
  ngram_words = {};

  # one gram
  for i in range(0, len(keywords)):

    if (len(keywords[i]) <= 2):
      continue;

    # ignore one gram if its two gram is in stop words
    if (i < len(keywords)-1):
      two_gram_test = keywords[i] + ' ' + keywords[i+1];
      if two_gram_test in stop_words:
        continue;

    if (keywords[i] in ngram_words and keywords[i] not in stop_words):
      ngram_words[keywords[i]] += mult;
    else:
      ngram_words[keywords[i]] = mult;

  # two gram
  for i in range(0, len(keywords)-1):
    if (len(keywords[i]) <= 2 or len(keywords[i+1]) <= 2):
      continue;

    if (keywords[i] in stop_words or keywords[i+1] in stop_words):
      continue;
    two_gram_word = keywords[i] + ' ' + keywords[i+1];

    if (two_gram_word in stop_words):
      continue;

    if (two_gram_word in ngram_words):
      ngram_words[two_gram_word] += mult;
    else:
      ngram_words[two_gram_word] = mult;


  # three gram
  for i in range(0, len(keywords)-2):
    if (len(keywords[i]) <= 2 or len(keywords[i+1]) <= 2 or len(keywords[i+2]) <= 2):
      continue;

    if (keywords[i] in stop_words or keywords[i+1] in stop_words or keywords[i+2] in stop_words):
      continue;
    three_gram_word = keywords[i] + ' ' + keywords[i+1] + ' ' +keywords[i+2];

    if (three_gram_word in stop_words):
      continue;

    if (three_gram_word in ngram_words):
      ngram_words[three_gram_word] += mult;
    else:
      ngram_words[three_gram_word] = mult;

  # remove the ones that only appeared 1 time
  for key, value in ngram_words.items():
    if value >= 2:
      final_ngrams[key] = value;

  return; 

def generate_ngram_keywords_for_doc(doc):
  if (len(stop_words) == 0):
    build_stop_words_set();

  generate_ngram_keywords_from_desc(doc['description']);
  generate_ngram_keywords_from_title(doc['title']);
  generate_ngram_keywords_from_word_array(doc['tags']);
  generate_ngram_keywords_from_word_array(doc['types']);

  final_ngrams = OrderedDict(sorted(final_ngrams.items(), key=lambda x : x[1], reverse=True));
  return final_ngrams; 

def generate_ngram_keywords_from_desc(desc):
  if (len(stop_words) == 0):
    build_stop_words_set();

  words = split_desc_to_words(desc);
  generate_ngram_keywords(words, 1);

  return;

def generate_ngram_keywords_from_title(title):
  if (len(stop_words) == 0):
    build_stop_words_set();

  words = split_desc_to_words(title);
  generate_ngram_keywords(words, 5);

  return;

def generate_ngram_keywords_from_word_array(types):
  if (len(stop_words) == 0):
    build_stop_words_set();

  words = [];
  for t in types:
    words.append(clean_word(t));

  generate_ngram_keywords(words, 5);

  return;

if __name__ == "__main__":
  build_stop_words_set();
  keywords = split_desc_to_words(desc);
  generate_ngram_keywords(keywords, 1);
