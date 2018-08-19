import gensim
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from smart_open import smart_open
from collections import defaultdict
import logging
import json
from six import iteritems
from pprint import pprint  # pretty-printer
import os
import re
from sklearn.cluster import KMeans

TEMP_FOLDER = 'data/temp'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
tokenizer = RegexpTokenizer(r"\w+")
frequency = defaultdict(int)
# remove common words and tokenize
stopword_set = set(stopwords.words("english"))
stoplist = stopwords.words("english")
class MyCorpus(object):
    def __iter__(self):
        #store number of sentences of each revision
        with smart_open('data/processed/index', 'a') as sentence_index:
            sentence_num = 0
            for line in smart_open('data/unprocessed/input', 'rb'):
                # assume there's one document per line, tokens separated by whitespace
                line = json.loads(line)['text'].lower()
                for sentence in split_by_sentence(line):
                    sentence_num += 1
                    yield dictionary.doc2bow(sentence)
                sentence_index.write(str(sentence_num))
                sentence_index.write('\n')

def split_by_sentence(text):
    text = re.split('([\W])', text.lower())
    stop = ('...', '.', '?', '!', '!!!')
    seperator = (' ', '', "'", ',')
    sentence = []
    for word in text:
        if word in stop:
            yield sentence
            sentence = []
        elif word not in seperator:
            sentence.append(word)

def nlp_clean(data):
   new_data = []
   for d in data:
      new_str = d.lower()
      dlist = tokenizer.tokenize(new_str)
      dlist = list(set(dlist).difference(stopword_set))
      new_data.append(dlist)
   return new_data

if not os.path.isfile(os.path.join(TEMP_FOLDER, 'my.dict')):
    # collect statistics about all tokens
    dictionary = gensim.corpora.Dictionary()
    with smart_open('data/unprocessed/input', 'rb', encoding='utf-8') as alldata, smart_open('data/processed/raw', 'w') as output:
        for line_no, line in enumerate(alldata):
            line = json.loads(line)
            tokens = nlp_clean(gensim.utils.to_unicode(line['text']).split())
            dictionary.add_documents(tokens)
    once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
    # remove words that appear only once
    dictionary.filter_tokens(once_ids)
    dictionary.save(os.path.join(TEMP_FOLDER, 'my.dict'))  # store the dictionary, for future reference
else:
    dictionary = gensim.corpora.Dictionary.load(os.path.join(TEMP_FOLDER, 'my.dict'))

corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
# save corpus in Matrix Market format.
gensim.corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'compora.mm'), corpus_memory_friendly)

corpus = gensim.corpora.MmCorpus(os.path.join(TEMP_FOLDER, 'compora.mm'))

all_data = []
sentence_each_revision = {}
with smart_open('data/processed/index') as sentence_index:
    for revision_num, sentence_num in enumerate(sentence_index):
        sentence_each_revision[revision_num] = int(sentence_num)
    for sentence_num, sentence in enumerate(corpus):
        if sentence_num <= sentence_each_revision[3] and sentence_num > sentence_each_revision[0]:
            all_data.append(all_data)



