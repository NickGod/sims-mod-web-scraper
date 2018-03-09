import re
from collections import OrderedDict

stop_words = set();

def split_desc_to_words(desc):
  res = "";
  res = re.sub(r"(([^a-zA-Z])+(')([^a-zA-Z])+|([^a-zA-Z])+(')|(')([^a-zA-Z])+|[^a-zA-Z']+)", " ", desc);
  res = re.sub(r"\\s+", " ", res);
  res = re.sub(r"(^(\\s+)|(\\s+)$)", "", res);
  res = res.lower();

  return res.split(" ");

# read from in put and build a set of stopwords
def build_stop_words_set():
  src = open('stop_words', 'r');

  for line in src:
      stopword = line.rstrip('\n');
      stop_words.add(stopword);

  src.close()
  return;

def generate_ngram_keywords(keywords):
  ngram_words = {};
  final_ngrams = {};

  # one gram
  for i in range(0, len(keywords)):

    if (len(keywords[i]) < 2):
      continue;

    if (keywords[i] in ngram_words and keywords[i] not in stop_words):
      ngram_words[keywords[i]] += 1;
    else:
      ngram_words[keywords[i]] = 1;

  # two gram
  for i in range(0, len(keywords)-1):
    if (len(keywords[i]) < 2 and len(keywords[i+1]) < 2):
      continue;

    if (keywords[i] in stop_words and keywords[i+1] in stop_words):
      continue;
    two_gram_word = keywords[i] + ' ' + keywords[i+1];
    if (two_gram_word in ngram_words):
      ngram_words[two_gram_word] += 1;
    else:
      ngram_words[two_gram_word] = 1;


  # three gram
  for i in range(0, len(keywords)-2):
    if (len(keywords[i]) < 2 and len(keywords[i+1]) < 2 and len(keywords[i+2]) < 2):
      continue;

    if (keywords[i] in stop_words and keywords[i+1] in stop_words and keywords[i+2] in stop_words):
      continue;
    three_gram_word = keywords[i] + ' ' + keywords[i+1] + ' ' +keywords[i+2];
    if (three_gram_word in ngram_words):
      ngram_words[three_gram_word] += 1;
    else:
      ngram_words[three_gram_word] = 1;

  # remove the ones that only appeared 1 time
  for key, value in ngram_words.items():
    if value >= 2:
      final_ngrams[key] = value;

  final_ngrams = OrderedDict(sorted(final_ngrams.items(), key=lambda x : x[1], reverse=True));
  
  return final_ngrams; 

def generate_ngram_keywords_from_desc(desc):
  if (len(stop_words) == 0):
    build_stop_words_set();

  words = split_desc_to_words(desc);
  final_ngram_keywords = generate_ngram_keywords(words);

  return final_ngram_keywords;

if __name__ == "__main__":
  build_stop_words_set();
  keywords = split_desc_to_words(desc);
  ngram_keywords = generate_ngram_keywords(keywords);
